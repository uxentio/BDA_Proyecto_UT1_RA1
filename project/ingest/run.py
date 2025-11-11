"""
Pipeline ETL completo: Ingesta -> Limpieza -> Oro -> Reporte
Proyecto: Finanzas - Presupuesto vs Gasto
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sqlite3
import uuid

# ==================== CONFIGURACION ====================
BATCH_ID = datetime.now().strftime('%Y%m%d_%H%M%S')
INGEST_TS = datetime.now().isoformat()

# Crear estructura de carpetas
os.makedirs('project/data/raw', exist_ok=True)
os.makedirs('project/data/clean', exist_ok=True)
os.makedirs('project/data/gold', exist_ok=True)
os.makedirs('project/data/quarantine', exist_ok=True)
os.makedirs('project/output', exist_ok=True)

print(f"""
============================================================
  PIPELINE ETL - FINANZAS (Presupuesto vs Gasto)
============================================================

Batch ID: {BATCH_ID}
Timestamp: {INGEST_TS}
""")

# ==================== FASE 1: INGESTA (BRONCE) ====================
print("\n" + "="*60)
print("FASE 1: INGESTA - CAPA BRONCE (RAW)")
print("="*60)

def ingerir_con_trazabilidad(filepath, source_name):
    """Ingesta datos con metadatos de trazabilidad"""
    print(f"\nIngiriendo: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"ERROR: No se encuentra {filepath}")
        print(f"   Ejecuta primero: python project/ingest/get_data.py")
        return None
    
    df = pd.read_csv(filepath)
    
    # Anadir metadatos de trazabilidad
    df['_ingest_ts'] = INGEST_TS
    df['_source_file'] = source_name
    df['_batch_id'] = BATCH_ID
    df['_event_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    
    print(f"   Registros cargados: {len(df)}")
    return df

# Ingerir gastos
df_gastos_raw = ingerir_con_trazabilidad('project/data/gastos.csv', 'gastos.csv')
if df_gastos_raw is None:
    exit(1)

# Ingerir presupuesto
df_presupuesto_raw = ingerir_con_trazabilidad('project/data/presupuesto.csv', 'presupuesto.csv')
if df_presupuesto_raw is None:
    exit(1)

# Guardar en capa BRONCE (Parquet)
print("\nGuardando en capa BRONCE (Parquet)...")
df_gastos_raw.to_parquet(f'project/data/raw/gastos_batch_{BATCH_ID}.parquet', index=False)
df_presupuesto_raw.to_parquet(f'project/data/raw/presupuesto_batch_{BATCH_ID}.parquet', index=False)
print("   Datos guardados en project/data/raw/")

# ==================== FASE 2: LIMPIEZA (PLATA) ====================
print("\n" + "="*60)
print("FASE 2: LIMPIEZA Y VALIDACION - CAPA PLATA (CLEAN)")
print("="*60)

cuarentena = []

def enviar_a_cuarentena(df, causa, nombre_archivo):
    """Envia registros invalidos a quarantine con la causa"""
    if len(df) > 0:
        df = df.copy()
        # Convertir fechas a string para evitar errores de tipo en Parquet
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]':
                df[col] = df[col].astype(str)
        df['_quarantine_reason'] = causa
        df['_quarantine_ts'] = datetime.now().isoformat()
        cuarentena.append(df)
        print(f"   {len(df)} registros -> CUARENTENA: {causa}")

# ========== LIMPIEZA DE GASTOS ==========
print("\nLimpiando GASTOS...")

df_gastos = df_gastos_raw.copy()
registros_iniciales = len(df_gastos)

# 1. VALIDAR NULOS
print("   Validando campos obligatorios...")
mask_nulos = df_gastos[['fecha', 'area', 'partida', 'importe']].isnull().any(axis=1)
enviar_a_cuarentena(df_gastos[mask_nulos], 'Campos obligatorios nulos', 'gastos_nulos')
df_gastos = df_gastos[~mask_nulos]

# 2. CONVERTIR TIPOS
print("   Convirtiendo tipos de datos...")
df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'], errors='coerce')
df_gastos['importe'] = pd.to_numeric(df_gastos['importe'], errors='coerce')

mask_fecha_invalida = df_gastos['fecha'].isnull()
mask_importe_invalido = df_gastos['importe'].isnull()
mask_conversion_fallida = mask_fecha_invalida | mask_importe_invalido

enviar_a_cuarentena(df_gastos[mask_conversion_fallida], 'Error en conversion de tipos', 'gastos_tipo_invalido')
df_gastos = df_gastos[~mask_conversion_fallida]

# 3. VALIDAR RANGOS
print("   Validando rangos...")
mask_importe_negativo = df_gastos['importe'] <= 0
enviar_a_cuarentena(df_gastos[mask_importe_negativo], 'Importe negativo o cero', 'gastos_importe_negativo')
df_gastos = df_gastos[~mask_importe_negativo]

# 4. NORMALIZAR AREA
print("   Normalizando area...")
area_map = {
    'ventas': 'Ventas', 'VENTAS': 'Ventas',
    'marketing': 'Marketing', 'MARKETING': 'Marketing',
    'ti': 'Ti', 'TI': 'Ti', 'IT': 'Ti',
    'rrhh': 'Rrhh', 'RRHH': 'Rrhh',
    'operaciones': 'Operaciones', 'OPERACIONES': 'Operaciones'
}

df_gastos['area'] = df_gastos['area'].replace(area_map)
df_gastos['area'] = df_gastos['area'].str.title()

areas_validas = ['Ventas', 'Marketing', 'Ti', 'Rrhh', 'Operaciones']
mask_area_invalida = ~df_gastos['area'].isin(areas_validas)
enviar_a_cuarentena(df_gastos[mask_area_invalida], f'Area no reconocida', 'gastos_area_invalida')
df_gastos = df_gastos[~mask_area_invalida]

# 5. NORMALIZAR PARTIDA
print("   Normalizando partida...")
partida_map = {'salarios': 'Salarios', 'SALARIOS': 'Salarios', 'publicidad': 'Publicidad', 'PUBLICIDAD': 'Publicidad'}
df_gastos['partida'] = df_gastos['partida'].replace(partida_map)
df_gastos['partida'] = df_gastos['partida'].str.title()

# 6. CONVERTIR IMPORTE A DECIMAL(18,2)
print("   Formateando importes (DECIMAL 18,2)...")
df_gastos['importe'] = df_gastos['importe'].round(2)

# 7. DEDUPLICACION
print("   Deduplicando registros...")
print("      Politica: Clave natural = (fecha, area, partida)")
print("      Estrategia: Ultimo registro gana (mayor _ingest_ts)")

duplicados_antes = len(df_gastos)
df_gastos = df_gastos.sort_values('_ingest_ts').drop_duplicates(subset=['fecha', 'area', 'partida'], keep='last')
duplicados_eliminados = duplicados_antes - len(df_gastos)
print(f"      Duplicados eliminados: {duplicados_eliminados}")

print(f"\n   GASTOS limpiados: {len(df_gastos)}/{registros_iniciales} registros validos")

# ========== LIMPIEZA DE PRESUPUESTO ==========
print("\nLimpiando PRESUPUESTO...")

df_presupuesto = df_presupuesto_raw.copy()
registros_iniciales_pres = len(df_presupuesto)

mask_nulos_pres = df_presupuesto[['area', 'presupuesto_anual']].isnull().any(axis=1)
enviar_a_cuarentena(df_presupuesto[mask_nulos_pres], 'Campos obligatorios nulos en presupuesto', 'presupuesto_nulos')
df_presupuesto = df_presupuesto[~mask_nulos_pres]

df_presupuesto['presupuesto_anual'] = pd.to_numeric(df_presupuesto['presupuesto_anual'], errors='coerce').round(2)
df_presupuesto['area'] = df_presupuesto['area'].replace(area_map)
df_presupuesto['area'] = df_presupuesto['area'].str.title()

print(f"   PRESUPUESTO limpiado: {len(df_presupuesto)}/{registros_iniciales_pres} registros")

# ========== GUARDAR CUARENTENA ==========
if cuarentena:
    print(f"\nGuardando {len(cuarentena)} lotes en CUARENTENA...")
    df_cuarentena = pd.concat(cuarentena, ignore_index=True)
    df_cuarentena.to_parquet(f'project/data/quarantine/quarantine_batch_{BATCH_ID}.parquet', index=False)
    print(f"   Cuarentena guardada: {len(df_cuarentena)} registros totales")
else:
    df_cuarentena = pd.DataFrame()

# ========== GUARDAR CAPA PLATA ==========
print("\nGuardando en capa PLATA (Parquet)...")
df_gastos.to_parquet(f'project/data/clean/gastos_clean_batch_{BATCH_ID}.parquet', index=False)
df_presupuesto.to_parquet(f'project/data/clean/presupuesto_clean_batch_{BATCH_ID}.parquet', index=False)
print("   Datos limpios guardados en project/data/clean/")

# ==================== FASE 3: CAPA ORO ====================
print("\n" + "="*60)
print("FASE 3: MODELADO ANALITICO - CAPA ORO (GOLD)")
print("="*60)

print("\nCalculando KPIs...")

df_gastos['mes'] = df_gastos['fecha'].dt.to_period('M').astype(str)
df_gasto_area = df_gastos.groupby('area')['importe'].sum().reset_index()
df_gasto_area.columns = ['area', 'gasto_acumulado']

df_oro = df_gasto_area.merge(df_presupuesto[['area', 'presupuesto_anual']], on='area', how='left')
df_oro['kpi_ejecucion'] = (df_oro['gasto_acumulado'] / df_oro['presupuesto_anual'] * 100).round(2)
df_oro['kpi_ejecucion_decimal'] = (df_oro['gasto_acumulado'] / df_oro['presupuesto_anual']).round(4)
df_oro['_batch_id'] = BATCH_ID
df_oro['_created_at'] = datetime.now().isoformat()

print(f"   KPI calculado para {len(df_oro)} areas")

df_mensual = df_gastos.groupby(['mes', 'area'])['importe'].sum().reset_index()
df_mensual.columns = ['mes', 'area', 'gasto_mensual']

print("\nGuardando en capa ORO...")
df_oro.to_parquet('project/data/gold/kpi_ejecucion.parquet', index=False)
df_mensual.to_parquet('project/data/gold/tendencia_mensual.parquet', index=False)

# ========== SQLITE ==========
print("\nCreando base de datos SQLite...")
conn = sqlite3.connect('project/data/gold/finanzas.db')

df_oro.to_sql('kpi_ejecucion', conn, if_exists='replace', index=False)
df_mensual.to_sql('tendencia_mensual', conn, if_exists='replace', index=False)

conn.execute("""
CREATE VIEW IF NOT EXISTS v_ejecucion_detalle AS
SELECT 
    area, presupuesto_anual, gasto_acumulado, kpi_ejecucion,
    CASE 
        WHEN kpi_ejecucion > 100 THEN 'SOBRE PRESUPUESTO'
        WHEN kpi_ejecucion >= 90 THEN 'EN RIESGO'
        WHEN kpi_ejecucion >= 70 THEN 'NORMAL'
        ELSE 'BAJO CONSUMO'
    END AS estado,
    presupuesto_anual - gasto_acumulado AS presupuesto_restante
FROM kpi_ejecucion
ORDER BY kpi_ejecucion DESC
""")

conn.close()
print("   SQLite creado: project/data/gold/finanzas.db")
print("   Vista creada: v_ejecucion_detalle")

# ==================== FASE 4: REPORTE MARKDOWN ====================
print("\n" + "="*60)
print("FASE 4: GENERANDO REPORTE MARKDOWN")
print("="*60)

reporte_md = f"""# Reporte de Ejecucion Presupuestaria 2024

**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Batch ID:** `{BATCH_ID}`  
**Periodo:** Enero - Octubre 2024

---

## Resumen Ejecutivo

Este reporte analiza la ejecucion presupuestaria por area, comparando el **gasto acumulado** vs el **presupuesto anual asignado**.

### Hallazgos principales:
- Se procesaron **{len(df_gastos)}** registros de gastos validos
- Se identificaron **{len(df_cuarentena)}** registros con errores (enviados a cuarentena)
- Se analizaron **{len(df_oro)}** areas organizacionales

---

## KPI Principal: Ejecucion Presupuestaria

### **Definicion del KPI**

```
KPI_Ejecucion = (Gasto Acumulado / Presupuesto Anual) × 100
```

**Interpretacion:**
- **< 70%**: Bajo consumo presupuestario
- **70-89%**: Ejecucion normal
- **90-100%**: En riesgo de sobrepasarse
- **> 100%**: Sobre presupuesto (CRITICO)

---

## Tabla 1: Ejecucion por Area

| Area | Presupuesto Anual (EUR) | Gasto Acumulado (EUR) | KPI Ejecucion (%) | Restante (EUR) |
|------|------------------------:|----------------------:|------------------:|---------------:|
"""

# Ordenar por KPI descendente
df_oro_sorted = df_oro.sort_values('kpi_ejecucion', ascending=False)

for _, row in df_oro_sorted.iterrows():
    restante = row['presupuesto_anual'] - row['gasto_acumulado']
    reporte_md += f"| {row['area']} | {row['presupuesto_anual']:,.2f} | {row['gasto_acumulado']:,.2f} | **{row['kpi_ejecucion']:.2f}%** | {restante:,.2f} |\n"

reporte_md += f"""

---

## Tabla 2: Tendencia Mensual de Gastos (Top 5 Meses)

"""

# Top 5 meses con mayor gasto
df_mensual_top = df_mensual.groupby('mes')['gasto_mensual'].sum().reset_index()
df_mensual_top = df_mensual_top.sort_values('gasto_mensual', ascending=False).head(5)

reporte_md += "| Mes | Gasto Total (EUR) |\n"
reporte_md += "|-----|------------------:|\n"
for _, row in df_mensual_top.iterrows():
    reporte_md += f"| {row['mes']} | {row['gasto_mensual']:,.2f} |\n"

reporte_md += f"""

---

## Contexto del Analisis

### Fuente de Datos
- **Archivo de Gastos:** `gastos.csv` ({len(df_gastos_raw)} registros originales)
- **Archivo de Presupuesto:** `presupuesto.csv` ({len(df_presupuesto_raw)} registros originales)

### Periodo Analizado
- **Inicio:** {df_gastos['fecha'].min().strftime('%Y-%m-%d')}
- **Fin:** {df_gastos['fecha'].max().strftime('%Y-%m-%d')}

### Ultima Actualizacion
- **Fecha de procesamiento:** {INGEST_TS}
- **Batch ID:** `{BATCH_ID}`

### Consideraciones Tecnicas

#### Registros en Cuarentena
Se identificaron **{len(df_cuarentena)}** registros con problemas:
- Campos obligatorios nulos
- Importes negativos o cero
- Fechas invalidas
- Areas no reconocidas

Estos registros se guardaron en `project/data/quarantine/` para revision manual.

#### Manejo de Importes
- Todos los importes se almacenan como **DECIMAL(18,2)**
- Los valores se redondean a 2 decimales
- **No se incluye IVA** en los calculos (gastos netos)

#### Deduplicacion
- **Clave natural:** (fecha, area, partida)
- **Politica:** "Ultimo gana" (se conserva el registro con mayor `_ingest_ts`)
- **Duplicados eliminados:** {duplicados_eliminados}

#### Periodificacion
- Los gastos se contabilizan por **fecha de transaccion**
- No se aplica criterio de devengo

---

## Conclusiones y Recomendaciones

### Areas en Riesgo
"""

# Identificar areas en riesgo
df_riesgo = df_oro_sorted[df_oro_sorted['kpi_ejecucion'] >= 90]
if len(df_riesgo) > 0:
    for _, row in df_riesgo.iterrows():
        if row['kpi_ejecucion'] > 100:
            reporte_md += f"- **{row['area']}**: SOBRE PRESUPUESTO ({row['kpi_ejecucion']:.2f}%) - Requiere accion inmediata\n"
        else:
            reporte_md += f"- **{row['area']}**: En riesgo ({row['kpi_ejecucion']:.2f}%) - Monitorear de cerca\n"
else:
    reporte_md += "No hay areas en riesgo critico actualmente.\n"

reporte_md += """

### Acciones Recomendadas

1. **Revision Inmediata**
   - Analizar areas con ejecucion > 100%
   - Evaluar necesidad de reasignacion presupuestaria

2. **Monitoreo Continuo**
   - Establecer alertas para areas con ejecucion > 90%
   - Revisar tendencias mensuales para anticipar desvios

3. **Calidad de Datos**
   - Revisar registros en cuarentena mensualmente
   - Validar areas y partidas con usuarios finales

---

## Definiciones de KPIs

### KPI_Ejecucion
- **Formula:** `(Gasto Acumulado / Presupuesto Anual) × 100`
- **Unidad:** Porcentaje (%)
- **Rango esperado:** 0% - 100%
- **Actualizacion:** Por batch (ETL)

### Gasto Acumulado
- **Definicion:** Suma de todos los importes de gastos registrados para un area
- **Unidad:** Euros (EUR)
- **Incluye:** Gastos netos sin IVA

### Presupuesto Restante
- **Formula:** `Presupuesto Anual - Gasto Acumulado`
- **Unidad:** Euros (EUR)
- **Interpretacion:** Fondos disponibles hasta fin de año

---

## Informacion Tecnica

### Pipeline ETL
1. **Ingesta (Bronce):** Lectura de CSVs con trazabilidad completa
2. **Limpieza (Plata):** Validaciones, normalizacion y deduplicacion
3. **Oro (Analytics):** Calculo de KPIs y agregaciones
4. **Reporte:** Generacion automatica en Markdown

### Trazabilidad
- `_ingest_ts`: Timestamp de ingesta
- `_source_file`: Archivo origen
- `_batch_id`: Identificador del batch procesado
- `_event_id`: ID unico por registro (UUID)

### Almacenamiento
- **Parquet:** Datos persistentes con particionado temporal
- **SQLite:** Base de datos para consultas SQL (`finanzas.db`)
- **Vista SQL:** `v_ejecucion_detalle` con estado y calculos

---

**Fin del Reporte**  
_Generado automaticamente por el pipeline ETL de Finanzas_
"""

# Guardar reporte
with open('project/output/reporte.md', 'w', encoding='utf-8') as f:
    f.write(reporte_md)

print(f"\nReporte generado: project/output/reporte.md")

# ==================== RESUMEN FINAL ====================
print("\n" + "="*60)
print("PIPELINE COMPLETADO EXITOSAMENTE")
print("="*60)
print(f"""
Resumen de Procesamiento:
   - Registros procesados: {len(df_gastos_raw)} gastos, {len(df_presupuesto_raw)} presupuestos
   - Registros validos: {len(df_gastos)} gastos
   - Registros en cuarentena: {len(df_cuarentena)}
   - Duplicados eliminados: {duplicados_eliminados}
   - KPIs generados: {len(df_oro)} areas

Archivos generados:
   - Bronce: project/data/raw/*.parquet
   - Plata: project/data/clean/*.parquet
   - Oro: project/data/gold/*.parquet
   - SQLite: project/data/gold/finanzas.db
   - Reporte: project/output/reporte.md
   - Cuarentena: project/data/quarantine/*.parquet

Proximos pasos:
   1. Revisa el reporte: project/output/reporte.md
   2. (Opcional) Publica en Quartz: python project/tools/copy_report_to_site.py
   3. Consulta la BD SQLite para analisis adicionales
""")