# 🏗️ ARQUITECTURA DEL PROYECTO ETL - FINANZAS

## 📊 Vista General del Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                       FUENTES DE DATOS                          │
│                                                                 │
│         gastos.csv              presupuesto.csv                 │
│   (504 registros)                (5 áreas)                      │
└────────────────┬────────────────────────┬───────────────────────┘
                 │                        │
                 │   FASE 1: INGESTA     │
                 │                        │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│          🔵 CAPA BRONCE (RAW) - Datos Crudos                    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  gastos_batch_20241110_143045.parquet                   │   │
│  │  ├─ fecha, area, partida, importe                       │   │
│  │  ├─ _ingest_ts: 2024-11-10T14:30:45                     │   │
│  │  ├─ _source_file: gastos.csv                            │   │
│  │  ├─ _batch_id: 20241110_143045                          │   │
│  │  └─ _event_id: uuid-1234-5678...                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📁 Ubicación: project/data/raw/                                │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │   FASE 2: LIMPIEZA Y VALIDACIÓN
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│          ⚪ CAPA PLATA (CLEAN) - Datos Validados                │
│                                                                 │
│  Validaciones aplicadas:                                        │
│  ✅ Nulos: fecha, area, partida, importe (obligatorios)        │
│  ✅ Tipos: fecha → datetime, importe → decimal(18,2)           │
│  ✅ Rangos: importe > 0                                         │
│  ✅ Dominios: area normalizada (Ventas, Marketing, TI...)      │
│  ✅ Deduplicación: (fecha, area, partida) → último gana        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  gastos_clean_batch_20241110_143045.parquet             │   │
│  │  ✅ 485 registros válidos (96.2%)                        │   │
│  │  ✅ Sin duplicados                                       │   │
│  │  ✅ Tipos correctos                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📁 Ubicación: project/data/clean/                              │
└────────────────┬──────────────────────┬─────────────────────────┘
                 │                      │
                 │                      │  Registros inválidos
                 │                      │
                 │                      ▼
                 │         ┌─────────────────────────────────────┐
                 │         │   ⚠️ CUARENTENA                     │
                 │         │                                     │
                 │         │  Causas:                            │
                 │         │  • Campos nulos: 6                  │
                 │         │  • Importes negativos: 10           │
                 │         │  • Tipos inválidos: 3               │
                 │         │  • Áreas desconocidas: 0            │
                 │         │                                     │
                 │         │  📁 project/data/quarantine/        │
                 │         └─────────────────────────────────────┘
                 │
                 │   FASE 3: MODELADO ANALÍTICO
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│          🟡 CAPA ORO (GOLD) - Datos Analíticos                  │
│                                                                 │
│  KPI Principal:                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  KPI_Ejecución = (Gasto Acumulado / Presupuesto) × 100│    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  kpi_ejecucion.parquet                                  │   │
│  │  ┌──────────┬──────────┬──────────┬────────────────┐   │   │
│  │  │ Área     │ Gasto    │ Presup.  │ KPI (%)        │   │   │
│  │  ├──────────┼──────────┼──────────┼────────────────┤   │   │
│  │  │ Marketing│ 295,000€ │ 300,000€ │ 98.33% 🔴     │   │   │
│  │  │ Ventas   │ 450,000€ │ 500,000€ │ 90.00% 🟡     │   │   │
│  │  │ TI       │ 320,000€ │ 400,000€ │ 80.00% 🟢     │   │   │
│  │  │ RRHH     │ 180,000€ │ 250,000€ │ 72.00% 🟢     │   │   │
│  │  │ Operac.  │ 210,000€ │ 350,000€ │ 60.00% 🔵     │   │   │
│  │  └──────────┴──────────┴──────────┴────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  tendencia_mensual.parquet                              │   │
│  │  • Gastos agrupados por mes y área                      │   │
│  │  • Identifica patrones estacionales                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📁 Ubicación: project/data/gold/                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │   ALMACENAMIENTO DUAL
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│   PARQUET    │   │    SQLITE    │
│              │   │              │
│ • Comprimido │   │ • Consultas  │
│ • Columnar   │   │   SQL        │
│ • Big Data   │   │ • Vista      │
│              │   │   analítica  │
└──────────────┘   └──────────────┘
                           │
                           │  Vista SQL
                           │
                           ▼
            ┌────────────────────────────┐
            │  v_ejecucion_detalle       │
            │                            │
            │  SELECT area,              │
            │    kpi_ejecucion,          │
            │    CASE                    │
            │      WHEN kpi > 100        │
            │        THEN 'CRÍTICO' ...  │
            │  FROM kpi_ejecucion        │
            └────────────────────────────┘
                 │
                 │   FASE 4: REPORTE
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│          📝 REPORTE MARKDOWN                                     │
│                                                                 │
│  project/output/reporte.md                                      │
│                                                                 │
│  Contenido:                                                     │
│  ✅ Resumen ejecutivo                                           │
│  ✅ Definiciones de KPI                                         │
│  ✅ Tabla de ejecución por área                                 │
│  ✅ Tendencia mensual                                           │
│  ✅ Contexto (fuente, periodo)                                  │
│  ✅ Conclusiones y recomendaciones                              │
│  ✅ Notas técnicas (IVA, deduplicación)                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ (Opcional)
                 │
                 ▼
         ┌───────────────┐
         │ 🌐 QUARTZ WEB │
         │   (GitHub     │
         │    Pages)     │
         └───────────────┘
```

---

## 🔄 FLUJO DE DATOS DETALLADO

### 1️⃣ INGESTA (Bronce)
```
CSV Files → pandas.read_csv() → Añadir metadatos → to_parquet()
```

**Metadatos añadidos:**
- `_ingest_ts`: Cuándo se ingirió
- `_source_file`: De dónde viene
- `_batch_id`: Identificador del lote
- `_event_id`: UUID único

### 2️⃣ LIMPIEZA (Plata)
```
Bronce Parquet
    ↓
Validar nulos → Cuarentena si falla
    ↓
Convertir tipos → Cuarentena si falla
    ↓
Validar rangos → Cuarentena si falla
    ↓
Normalizar dominios → Cuarentena si falla
    ↓
Deduplicar (fecha, area, partida) - último gana
    ↓
Plata Parquet (datos limpios)
```

### 3️⃣ MODELADO (Oro)
```
Plata Parquet
    ↓
GROUP BY area → SUM(importe) = gasto_acumulado
    ↓
JOIN con presupuesto (on area)
    ↓
CALCULAR: kpi_ejecucion = (gasto / presupuesto) × 100
    ↓
Oro Parquet + SQLite + Vista SQL
```

### 4️⃣ REPORTE
```
Oro Parquet/SQLite
    ↓
Leer datos con pandas
    ↓
Formatear tablas en Markdown
    ↓
Añadir contexto y definiciones
    ↓
Generar reporte.md
    ↓
(Opcional) Copiar a Quartz → GitHub Pages
```

---

## 🎯 DECISIONES CLAVE

### ¿Por qué 3 capas?

| Capa   | Propósito                    | Analogía               |
|--------|------------------------------|------------------------|
| Bronce | Datos crudos sin tocar       | "Archivo de respaldo"  |
| Plata  | Datos validados y limpios    | "Hoja de cálculo OK"   |
| Oro    | KPIs y métricas de negocio   | "Dashboard ejecutivo"  |

### ¿Por qué Parquet + SQLite?

**Parquet:**
- ✅ Eficiente para Big Data
- ✅ Compresión automática (~10x más pequeño que CSV)
- ✅ Compatible con Spark, Dask, Pandas

**SQLite:**
- ✅ Consultas SQL ad-hoc
- ✅ No requiere servidor
- ✅ Portable (un solo archivo .db)

### ¿Por qué "Último gana"?

**Escenario real:**
1. Usuario registra un gasto: 1000€ el 10/11
2. Se da cuenta de un error
3. Corrige el gasto: 1200€ el 10/11
4. Ambos se ingresan con diferentes `_ingest_ts`

**Deduplicación:**
- Clave: (fecha=10/11, area=Ventas, partida=Salarios)
- **Último gana** → Se queda el de 1200€ (más reciente)
- El de 1000€ sigue en Bronce (auditoría)

---

## 📏 MÉTRICAS DE CALIDAD

### Cobertura de Validaciones
- ✅ **Nulos:** 100% de campos obligatorios verificados
- ✅ **Tipos:** 100% de campos convertidos correctamente
- ✅ **Rangos:** 100% de importes > 0
- ✅ **Dominios:** 100% de áreas normalizadas

### Tasa de Éxito
```
Tasa de éxito = (Registros válidos / Registros totales) × 100

Ejemplo: (485 / 504) × 100 = 96.2%
```

### Tasa de Cuarentena
```
Tasa de cuarentena = (Registros en cuarentena / Registros totales) × 100

Ejemplo: (19 / 504) × 100 = 3.8%
```

---

## 🔍 TRAZABILIDAD END-TO-END

```
CSV Original (gastos.csv)
  ↓ [_ingest_ts, _source_file, _batch_id, _event_id]
Bronce Parquet
  ↓ [se conservan todos los metadatos]
Plata Parquet (si pasa validaciones)
  ↓ [se conservan todos los metadatos]
Oro Parquet [_batch_id, _created_at]
  ↓
Reporte.md [referencia al batch_id]
```

**Auditoría completa:**
Puedes rastrear cualquier KPI en el reporte hasta el registro original en el CSV usando los metadatos.

---

## 🎓 CONCEPTOS PARA LA ENTREVISTA

### Idempotencia
**Pregunta:** ¿Qué pasa si ejecutas el pipeline dos veces?

**Respuesta:** 
- Cada ejecución genera un nuevo `batch_id` (timestamp único)
- Los archivos se nombran con el `batch_id`
- Resultado: Coexisten sin duplicar
- Ejemplo: `gastos_batch_20241110_143045.parquet` y `gastos_batch_20241110_160000.parquet`

### Deduplicación
**Pregunta:** ¿Cómo manejas duplicados?

**Respuesta:**
- **Clave natural:** (fecha, area, partida)
- **Política:** "Último gana" por `_ingest_ts`
- **Justificación:** El registro más reciente es la versión correcta

### Cuarentena vs Eliminación
**Pregunta:** ¿Por qué no eliminas registros inválidos?

**Respuesta:**
- Los registros inválidos pueden tener información valiosa
- Enviarlos a cuarentena permite revisión manual
- Se documenta la causa del rechazo
- Mantiene la trazabilidad completa

### DECIMAL vs FLOAT
**Pregunta:** ¿Por qué usas DECIMAL(18,2) para importes?

**Respuesta:**
- Los `FLOAT` tienen problemas de precisión: 0.1 + 0.2 ≠ 0.3 en binario
- `DECIMAL` garantiza precisión exacta (crucial para dinero)
- 18 dígitos totales, 2 decimales (estándar financiero)

---

## 📂 ESTRUCTURA FINAL DE ARCHIVOS

```
proyecto-finanzas/
├── project/
│   ├── data/
│   │   ├── gastos.csv (generado)
│   │   ├── presupuesto.csv (generado)
│   │   ├── raw/
│   │   │   ├── gastos_batch_YYYYMMDD_HHMMSS.parquet
│   │   │   └── presupuesto_batch_YYYYMMDD_HHMMSS.parquet
│   │   ├── clean/
│   │   │   ├── gastos_clean_batch_YYYYMMDD_HHMMSS.parquet
│   │   │   └── presupuesto_clean_batch_YYYYMMDD_HHMMSS.parquet
│   │   ├── gold/
│   │   │   ├── kpi_ejecucion.parquet
│   │   │   ├── tendencia_mensual.parquet
│   │   │   └── finanzas.db (SQLite)
│   │   └── quarantine/
│   │       └── quarantine_batch_YYYYMMDD_HHMMSS.parquet
│   ├── ingest/
│   │   ├── get_data.py
│   │   └── run.py
│   ├── output/
│   │   └── reporte.md (generado)
│   ├── tools/
│   │   └── copy_report_to_site.py
│   └── requirements.txt
├── docs/
│   ├── ingestion.md
│   ├── cleaning.md
│   └── kpis.md
├── README.md
├── .gitignore
└── .github/workflows/deploy-pages.yml
```

---

## 🚀 COMANDO ÚNICO PARA EJECUTAR TODO

```bash
# Desde la raíz del proyecto
python project/ingest/get_data.py && python project/ingest/run.py
```

Esto hace:
1. ✅ Genera CSVs de ejemplo
2. ✅ Ejecuta todo el pipeline ETL
3. ✅ Genera el reporte

**Duración total:** ~1 minuto

---

Esta arquitectura sigue las **mejores prácticas de Data Engineering** y está lista para presentar en la entrevista. ¡Éxito! 🎉
