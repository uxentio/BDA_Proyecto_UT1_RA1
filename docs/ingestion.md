# Documentacion: Proceso de Ingesta

## Objetivo

La fase de ingesta es responsable de **leer los datos crudos** desde archivos CSV y **anadir metadatos de trazabilidad** antes de almacenarlos en la capa Bronce.

---

## Arquitectura de Ingesta

```
Archivos CSV (Fuente)
        ↓
  Lectura con Pandas
        ↓
  Anadir Metadatos de Trazabilidad
        ↓
  Capa BRONCE (Parquet)
```

---

## Metadatos de Trazabilidad

Cada registro ingresado recibe los siguientes metadatos:

### `_ingest_ts` (Timestamp de Ingesta)
- **Tipo:** ISO 8601 string
- **Ejemplo:** `2024-11-10T14:30:45.123456`
- **Uso:** Saber cuando se ingirio cada registro

### `_source_file` (Archivo Origen)
- **Tipo:** string
- **Ejemplo:** `gastos.csv`
- **Uso:** Rastrear de que archivo proviene cada registro

### `_batch_id` (Identificador de Batch)
- **Tipo:** string (formato: `YYYYMMDD_HHMMSS`)
- **Ejemplo:** `20241110_143045`
- **Uso:** Identificar ejecuciones del pipeline; permite idempotencia

### `_event_id` (ID Unico del Evento)
- **Tipo:** UUID v4
- **Ejemplo:** `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- **Uso:** Identificador unico e inmutable de cada registro

---

## Idempotencia

El pipeline es **idempotente** gracias al `batch_id`:

- Cada ejecucion genera un nuevo `batch_id` basado en timestamp
- Los archivos Parquet se nombran con el `batch_id`
- Reprocesar el mismo archivo genera un nuevo batch sin duplicar

**Ejemplo:**
```
Primera ejecucion:  gastos_batch_20241110_143045.parquet
Segunda ejecucion:  gastos_batch_20241110_150230.parquet
```

Ambos archivos coexisten sin conflicto.

---

## Implementacion Tecnica

### Funcion Principal: `ingerir_con_trazabilidad()`

```python
def ingerir_con_trazabilidad(filepath, source_name):
    """
    Lee un archivo CSV y anade metadatos de trazabilidad
    
    Args:
        filepath: Ruta al archivo CSV
        source_name: Nombre del archivo (para _source_file)
    
    Returns:
        DataFrame con columnas originales + metadatos
    """
    df = pd.read_csv(filepath)
    
    df['_ingest_ts'] = INGEST_TS
    df['_source_file'] = source_name
    df['_batch_id'] = BATCH_ID
    df['_event_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    
    return df
```

---

## Almacenamiento en Bronce

Los datos ingresados se guardan en **Apache Parquet**:

- **Formato:** Parquet (columnar, comprimido)
- **Ubicacion:** `project/data/raw/`
- **Nombrado:** `{tabla}_batch_{BATCH_ID}.parquet`
- **Particionado:** Temporal por batch_id

**Ventajas de Parquet:**
- Compresion eficiente (~10x mas pequeno que CSV)
- Lectura rapida de columnas especificas
- Preserva tipos de datos
- Compatible con herramientas Big Data (Spark, Dask)

---

## Archivos de Entrada

### 1. gastos.csv
**Estructura:**
```csv
fecha,area,partida,importe
2024-01-15,Ventas,Salarios,5000.50
2024-02-20,Marketing,Publicidad,3200.00
```

**Campos:**
- `fecha`: Fecha de la transaccion (YYYY-MM-DD)
- `area`: Area organizacional
- `partida`: Categoria del gasto
- `importe`: Monto en euros (decimal)

### 2. presupuesto.csv
**Estructura:**
```csv
area,presupuesto_anual,año
Ventas,500000.00,2024
Marketing,300000.00,2024
```

**Campos:**
- `area`: Area organizacional
- `presupuesto_anual`: Presupuesto asignado (euros)
- `año`: Año fiscal

---

## Manejo de Errores

### Archivo no encontrado
Si un archivo CSV no existe, el pipeline:
1. Muestra un mensaje de error claro
2. Sugiere ejecutar `get_data.py` para generar datos
3. Termina la ejecucion con codigo de salida 1

```python
if not os.path.exists(filepath):
    print(f"ERROR: No se encuentra {filepath}")
    print(f"   Ejecuta primero: python project/ingest/get_data.py")
    return None
```

### Validacion posterior
Los errores de **contenido** (nulos, tipos incorrectos, etc.) se manejan en la fase de limpieza, no en la ingesta.

**Filosofia:** La capa Bronce acepta TODO, la validacion ocurre en Plata.

---

## Testing de Ingesta

Para probar la ingesta independientemente:

```python
import pandas as pd

# Leer un archivo Bronce
df = pd.read_parquet('project/data/raw/gastos_batch_20241110_143045.parquet')

# Verificar metadatos
assert '_ingest_ts' in df.columns
assert '_source_file' in df.columns
assert '_batch_id' in df.columns
assert '_event_id' in df.columns

print("Metadatos presentes")
print(f"Registros: {len(df)}")
print(f"Batch ID: {df['_batch_id'].iloc[0]}")
```

---

## Proximos Pasos

Despues de la ingesta, los datos pasan a la **fase de limpieza** (Plata), donde se:
- Validan tipos de datos
- Verifican rangos y dominios
- Deduplicacion
- Normalizacion

Ver: docs/cleaning.md
