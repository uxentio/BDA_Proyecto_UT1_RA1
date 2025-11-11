# Reporte de Ejecucion Presupuestaria 2024

**Generado:** 2025-11-11 19:13:03  
**Batch ID:** `20251111_191303`  
**Periodo:** Enero - Octubre 2024

---

## Resumen Ejecutivo

Este reporte analiza la ejecucion presupuestaria por area, comparando el **gasto acumulado** vs el **presupuesto anual asignado**.

### Hallazgos principales:
- Se procesaron **479** registros de gastos validos
- Se identificaron **12** registros con errores (enviados a cuarentena)
- Se analizaron **5** areas organizacionales

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
| Ventas | 250,078.45 | 982,880.56 | **393.03%** | -732,802.11 |
| Ti | 682,162.12 | 939,607.80 | **137.74%** | -257,445.68 |
| Rrhh | 503,124.06 | 479,328.76 | **95.27%** | 23,795.30 |
| Marketing | 729,449.82 | 563,695.44 | **77.28%** | 165,754.38 |
| Operaciones | 780,275.97 | 567,621.55 | **72.75%** | 212,654.42 |


---

## Tabla 2: Tendencia Mensual de Gastos (Top 5 Meses)

| Mes | Gasto Total (EUR) |
|-----|------------------:|
| 2024-08 | 514,103.18 |
| 2024-01 | 406,555.57 |
| 2024-04 | 384,559.53 |
| 2024-10 | 370,437.98 |
| 2024-03 | 346,916.19 |


---

## Contexto del Analisis

### Fuente de Datos
- **Archivo de Gastos:** `gastos.csv` (504 registros originales)
- **Archivo de Presupuesto:** `presupuesto.csv` (5 registros originales)

### Periodo Analizado
- **Inicio:** 2024-01-01
- **Fin:** 2024-10-26

### Ultima Actualizacion
- **Fecha de procesamiento:** 2025-11-11T19:13:03.495495
- **Batch ID:** `20251111_191303`

### Consideraciones Tecnicas

#### Registros en Cuarentena
Se identificaron **12** registros con problemas:
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
- **Duplicados eliminados:** 13

#### Periodificacion
- Los gastos se contabilizan por **fecha de transaccion**
- No se aplica criterio de devengo

---

## Conclusiones y Recomendaciones

### Areas en Riesgo
- **Ventas**: SOBRE PRESUPUESTO (393.03%) - Requiere accion inmediata
- **Ti**: SOBRE PRESUPUESTO (137.74%) - Requiere accion inmediata
- **Rrhh**: En riesgo (95.27%) - Monitorear de cerca


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
