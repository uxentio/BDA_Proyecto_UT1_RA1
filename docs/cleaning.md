# Documentacion: Proceso de Limpieza (Capa Plata)

## Objetivo

La fase de limpieza transforma datos crudos de la **capa Bronce** en datos **validados, normalizados y sin duplicados** en la **capa Plata**.

---

## Arquitectura de Limpieza

```
Capa BRONCE (Parquet)
        ↓
  Validar Nulos
        ↓
  Convertir Tipos
        ↓
  Validar Rangos
        ↓
  Normalizar Dominios
        ↓
  Deduplicar
        ↓
  Capa PLATA (Parquet)
        ↓
  Cuarentena (registros invalidos)
```

---

## Validaciones Implementadas

### 1. Validacion de Campos Obligatorios (NOT NULL)

**Campos obligatorios en `gastos`:**
- `fecha`
- `area`
- `partida`
- `importe`

**Codigo:**
```python
mask_nulos = df_gastos[['fecha', 'area', 'partida', 'importe']].isnull().any(axis=1)
enviar_a_cuarentena(df_gastos[mask_nulos], 'Campos obligatorios nulos')
df_gastos = df_gastos[~mask_nulos]
```

**Resultado:** Registros con cualquier campo nulo → cuarentena

---

### 2. Conversion de Tipos de Datos

**Conversiones aplicadas:**

| Campo    | Tipo Origen | Tipo Destino | Validacion                |
|----------|-------------|--------------|---------------------------|
| `fecha`  | string      | datetime64   | Formato valido (ISO 8601) |
| `importe`| string/int  | float64      | Numerico, 2 decimales     |
| `area`   | string      | string       | Normalizacion             |
| `partida`| string      | string       | Normalizacion             |

**Codigo:**
```python
df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'], errors='coerce')
df_gastos['importe'] = pd.to_numeric(df_gastos['importe'], errors='coerce')
```

**Manejo de errores:**
- `errors='coerce'` convierte valores invalidos a `NaT` (fecha) o `NaN` (numerico)
- Estos registros se detectan y envian a cuarentena

---

### 3. Validacion de Rangos

**Regla:** Los importes deben ser **positivos y > 0**

```python
mask_importe_negativo = df_gastos['importe'] <= 0
enviar_a_cuarentena(df_gastos[mask_importe_negativo], 'Importe negativo o cero')
df_gastos = df_gastos[~mask_importe_negativo]
```

**Justificacion:** Un gasto no puede ser negativo (los ingresos se modelan aparte).

---

### 4. Normalizacion de Dominios

#### Areas Organizacionales

**Mapeo de variaciones:**
```python
area_map = {
    'ventas': 'Ventas',
    'VENTAS': 'Ventas',
    'ti': 'TI',
    'IT': 'TI',
    'rrhh': 'RRHH',
    'marketing': 'Marketing',
    'operaciones': 'Operaciones'
}

df_gastos['area'] = df_gastos['area'].replace(area_map)
df_gastos['area'] = df_gastos['area'].str.title()
```

**Areas validas:**
- Ventas
- Marketing
- TI
- RRHH
- Operaciones

**Areas no reconocidas → cuarentena**

---

### 5. Formateo de Importes (DECIMAL 18,2)

**Regla:** Los importes se redondean a **2 decimales**

```python
df_gastos['importe'] = df_gastos['importe'].round(2)
```

**Justificacion:** 
- Los centimos son la minima unidad monetaria en euros
- Evita problemas de precision con `FLOAT`
- Compatible con bases de datos financieras (DECIMAL)

---

## Deduplicacion

### Clave Natural
La clave natural de un gasto es:
```
(fecha, area, partida)
```

**Justificacion:** Es improbable que la misma area tenga dos gastos en la misma partida el mismo dia que sean diferentes.

### Estrategia: "Ultimo Gana"

**Politica:** Cuando hay duplicados, se conserva el registro con **mayor `_ingest_ts`**

```python
df_gastos = df_gastos.sort_values('_ingest_ts').drop_duplicates(
    subset=['fecha', 'area', 'partida'],
    keep='last'  # Conservar el ultimo (mas reciente)
)
```

**Razon:** 
- En un sistema real, un usuario podria corregir un gasto erroneo
- El registro mas reciente representa la informacion correcta
- Mantiene trazabilidad del cambio (ambos registros existen en Bronce)

---

## Sistema de Cuarentena

### Que es la Cuarentena?

Registros que **no pasan las validaciones** se guardan en:
```
project/data/quarantine/quarantine_batch_{BATCH_ID}.parquet
```

### Metadatos Anadidos

Cada registro en cuarentena recibe:
- `_quarantine_reason`: Descripcion del error
- `_quarantine_ts`: Timestamp de cuando fue enviado a cuarentena

### Causas de Cuarentena Implementadas

1. **Campos obligatorios nulos** → `fecha`, `area`, `partida` o `importe` es NULL
2. **Error en conversion de tipos** → Fecha o importe no convertible
3. **Importe negativo o cero** → `importe <= 0`
4. **Area no reconocida** → Area fuera del dominio valido

---

## Almacenamiento en Plata

Los datos limpios se guardan en:
```
project/data/clean/gastos_clean_batch_{BATCH_ID}.parquet
project/data/clean/presupuesto_clean_batch_{BATCH_ID}.parquet
```

**Caracteristicas:**
- Sin nulos en campos obligatorios
- Tipos de datos correctos
- Rangos validados
- Dominios normalizados
- Sin duplicados
- Importes en DECIMAL(18,2)

---

## Reglas de Negocio Documentadas

### 1. IVA
**Supuesto:** Los importes en `gastos.csv` son **netos (sin IVA)**

**Justificacion:** Las empresas suelen registrar gastos sin IVA porque este se recupera.

### 2. Periodificacion
**Criterio:** Fecha de **transaccion**, no de devengo

**Justificacion:** Simplicidad. No tenemos informacion de cuando se devengo el gasto.

### 3. Presupuesto Anual
**Supuesto:** El presupuesto es anual, no mensual

**Justificacion:** El archivo `presupuesto.csv` tiene un unico valor por area.

---

## Testing de Limpieza

Para verificar la calidad de los datos limpios:

```python
import pandas as pd

df = pd.read_parquet('project/data/clean/gastos_clean_batch_20241110_143045.parquet')

# Test 1: Sin nulos en campos obligatorios
assert df[['fecha', 'area', 'partida', 'importe']].isnull().sum().sum() == 0

# Test 2: Todos los importes son positivos
assert (df['importe'] > 0).all()

# Test 3: Solo areas validas
areas_validas = ['Ventas', 'Marketing', 'Ti', 'Rrhh', 'Operaciones']
assert df['area'].isin(areas_validas).all()

# Test 4: Sin duplicados
assert df.duplicated(subset=['fecha', 'area', 'partida']).sum() == 0

print("Todos los tests pasaron")
```

---

## Proximos Pasos

Despues de la limpieza, los datos pasan a la **capa Oro** donde se:
- Calculan KPIs de negocio
- Crean agregaciones analiticas
- Generan vistas SQL

Ver: docs/kpis.md
