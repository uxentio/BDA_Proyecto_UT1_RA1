# Documentacion: KPIs y Capa Oro

## Objetivo

La **capa Oro (Gold)** contiene datos analiticos listos para consumo: KPIs, agregaciones y metricas de negocio derivadas de los datos limpios de la capa Plata.

---

## Arquitectura de la Capa Oro

```
Capa PLATA (Datos Limpios)
        ↓
  Agregaciones
        ↓
  Calculo de KPIs
        ↓
  Capa ORO (Analytics)
        ↓
  Almacenamiento (Parquet + SQLite)
```

---

## KPI Principal: Ejecucion Presupuestaria

### Definicion

```
KPI_Ejecucion = (Gasto Acumulado / Presupuesto Anual) × 100
```

### Componentes

**Gasto Acumulado:**
- Suma de todos los importes de gastos registrados para un area
- Unidad: Euros (€)
- Formula SQL: `SUM(importe) GROUP BY area`

**Presupuesto Anual:**
- Presupuesto asignado a un area para el año fiscal
- Unidad: Euros (€)
- Fuente: `presupuesto.csv`

### Interpretacion del KPI

| Rango KPI  | Estado            | Accion                                    |
|------------|-------------------|-------------------------------------------|
| 0-69%      | Bajo consumo      | Revisar subejecucion                      |
| 70-89%     | Normal            | Monitoreo rutinario                       |
| 90-100%    | En riesgo         | Alertar y monitorear de cerca             |
| > 100%     | Sobre presupuesto | CRITICO - Requiere accion inmediata       |

### Ejemplo de Calculo

**Area: Ventas**
- Presupuesto Anual: 500,000 €
- Gastos registrados:
  - Enero: 40,000 €
  - Febrero: 38,000 €
  - Marzo: 42,000 €
  - ...
  - Octubre: 41,000 €
- **Gasto Acumulado:** 450,000 €

```
KPI_Ejecucion = (450,000 / 500,000) × 100 = 90%
Estado: EN RIESGO
```

---

## Implementacion Tecnica

### 1. Calculo del Gasto Acumulado

```python
# Agrupar gastos por area
df_gasto_area = df_gastos.groupby('area')['importe'].sum().reset_index()
df_gasto_area.columns = ['area', 'gasto_acumulado']
```

### 2. Union con Presupuesto

```python
# Unir con presupuesto
df_oro = df_gasto_area.merge(
    df_presupuesto[['area', 'presupuesto_anual']], 
    on='area', 
    how='left'
)
```

### 3. Calculo del KPI

```python
# Calcular porcentaje de ejecucion
df_oro['kpi_ejecucion'] = (
    df_oro['gasto_acumulado'] / df_oro['presupuesto_anual'] * 100
).round(2)

# Version decimal para calculos
df_oro['kpi_ejecucion_decimal'] = (
    df_oro['gasto_acumulado'] / df_oro['presupuesto_anual']
).round(4)
```

---

## KPI Secundario: Tendencia Mensual

### Definicion

Gasto total agrupado por mes y area.

### Implementacion

```python
# Extraer mes de la fecha
df_gastos['mes'] = df_gastos['fecha'].dt.to_period('M').astype(str)

# Agrupar por mes y area
df_mensual = df_gastos.groupby(['mes', 'area'])['importe'].sum().reset_index()
df_mensual.columns = ['mes', 'area', 'gasto_mensual']
```

### Utilidad

- Identificar meses con mayor gasto
- Detectar patrones estacionales
- Proyectar gastos futuros

---

## Almacenamiento en Oro

### Archivos Parquet

**1. kpi_ejecucion.parquet**
```
Columnas:
  - area: string
  - gasto_acumulado: float64 (2 decimales)
  - presupuesto_anual: float64 (2 decimales)
  - kpi_ejecucion: float64 (porcentaje con 2 decimales)
  - kpi_ejecucion_decimal: float64 (4 decimales)
  - _batch_id: string
  - _created_at: timestamp ISO 8601
```

**2. tendencia_mensual.parquet**
```
Columnas:
  - mes: string (formato: 'YYYY-MM')
  - area: string
  - gasto_mensual: float64 (2 decimales)
```

### Base de Datos SQLite

**Ubicacion:** `project/data/gold/finanzas.db`

**Tablas:**

#### 1. `kpi_ejecucion`
```sql
CREATE TABLE kpi_ejecucion (
    area TEXT PRIMARY KEY,
    gasto_acumulado REAL,
    presupuesto_anual REAL,
    kpi_ejecucion REAL,
    kpi_ejecucion_decimal REAL,
    _batch_id TEXT,
    _created_at TEXT
);
```

#### 2. `tendencia_mensual`
```sql
CREATE TABLE tendencia_mensual (
    mes TEXT,
    area TEXT,
    gasto_mensual REAL,
    PRIMARY KEY (mes, area)
);
```

---

## Vista SQL Util: `v_ejecucion_detalle`

### Definicion

```sql
CREATE VIEW v_ejecucion_detalle AS
SELECT 
    area,
    presupuesto_anual,
    gasto_acumulado,
    kpi_ejecucion,
    CASE 
        WHEN kpi_ejecucion > 100 THEN 'SOBRE PRESUPUESTO'
        WHEN kpi_ejecucion >= 90 THEN 'EN RIESGO'
        WHEN kpi_ejecucion >= 70 THEN 'NORMAL'
        ELSE 'BAJO CONSUMO'
    END AS estado,
    presupuesto_anual - gasto_acumulado AS presupuesto_restante
FROM kpi_ejecucion
ORDER BY kpi_ejecucion DESC;
```

### Columnas Adicionales

**`estado`:** Clasificacion automatica del nivel de ejecucion
**`presupuesto_restante`:** Fondos disponibles (€)

---

## Consultas Analiticas Utiles

### 1. Top 3 Areas con Mayor Ejecucion

```sql
SELECT 
    area,
    kpi_ejecucion,
    estado
FROM v_ejecucion_detalle
ORDER BY kpi_ejecucion DESC
LIMIT 3;
```

### 2. Total de Gastos por Mes

```sql
SELECT 
    mes,
    SUM(gasto_mensual) AS gasto_total
FROM tendencia_mensual
GROUP BY mes
ORDER BY mes;
```

### 3. Areas en Riesgo o Sobre Presupuesto

```sql
SELECT 
    area,
    kpi_ejecucion,
    presupuesto_restante,
    estado
FROM v_ejecucion_detalle
WHERE kpi_ejecucion >= 90
ORDER BY kpi_ejecucion DESC;
```

---

## Metadatos de Trazabilidad en Oro

Todos los registros en la capa Oro incluyen:

### `_batch_id`
- Identificador del batch que genero estos KPIs
- Formato: `YYYYMMDD_HHMMSS`
- Permite rastrear de que ejecucion provienen los datos

### `_created_at`
- Timestamp de cuando se calculo el KPI
- Formato: ISO 8601 (ej: `2024-11-10T14:30:45`)

---

## Reglas de Negocio

### 1. Presupuesto Anual vs Mensual

**Supuesto actual:** El presupuesto en `presupuesto.csv` es **anual**

**Calculo:** El KPI compara gastos acumulados del año vs presupuesto anual

---

## Actualizacion de KPIs

### Frecuencia
Los KPIs se recalculan en **cada ejecucion del pipeline ETL** (cada batch).

### Historico
Cada ejecucion genera un nuevo archivo Parquet con el `batch_id`:
```
kpi_ejecucion_batch_20241110_143045.parquet
kpi_ejecucion_batch_20241110_160000.parquet
```

### SQLite: Sobrescritura
La tabla en SQLite se **sobrescribe** (`if_exists='replace'`) en cada ejecucion:
- Solo contiene los KPIs del ultimo batch
- Para historico, usar los archivos Parquet

---

## Validaciones de Calidad en Oro

```python
import pandas as pd

df_kpi = pd.read_parquet('project/data/gold/kpi_ejecucion.parquet')

# Test 1: KPI debe estar entre 0 y 200%
assert (df_kpi['kpi_ejecucion'] >= 0).all()
assert (df_kpi['kpi_ejecucion'] <= 200).all()

# Test 2: Gasto acumulado >= 0
assert (df_kpi['gasto_acumulado'] >= 0).all()

# Test 3: Presupuesto anual > 0
assert (df_kpi['presupuesto_anual'] > 0).all()

print("Validaciones de calidad OK")
```

---

## Proximos Pasos

Despues de calcular los KPIs, se genera el **reporte en Markdown** que consume estos datos para presentar:
- Tablas de ejecucion por area
- Tendencias mensuales
- Alertas de areas en riesgo
- Recomendaciones de accion

Ver: project/output/reporte.md
