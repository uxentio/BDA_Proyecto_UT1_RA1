# 📊 Proyecto ETL: Finanzas - Análisis de Ejecución Presupuestaria

**Asignatura:** Big Data Aplicado - UT1  
**Alumno:** Antonio Ferrer Martínez  
**Fecha:** Noviembre 2024

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()

---

## 🌐 Accesos Rápidos

- **🌍 Sitio Web:** [uxentio.github.io/BDA_Proyecto_UT1_RA1](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)
- **📊 Reporte Interactivo:** [Ver Reporte](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/reporte.html)
- **📚 Documentación:** [/docs](./docs/)
- **💻 Repositorio:** [GitHub](https://github.com/uxentio/BDA_Proyecto_UT1_RA1)

---

## 📋 Descripción

Este proyecto implementa un **pipeline ETL completo** que procesa datos financieros (gastos y presupuestos) para calcular el **KPI de ejecución presupuestaria** por área organizacional.

### 🎯 KPI Principal

```
KPI_Ejecución = (Gasto Acumulado / Presupuesto Anual) × 100
```

**Objetivo:** Monitorear el nivel de ejecución del presupuesto asignado a cada área de la organización, identificando desviaciones y áreas de optimización.

---

## 🏗️ Arquitectura

**Pipeline ETL de 3 Capas (Medallion Architecture):**

| Capa | Descripción | Contenido |
|------|-------------|-----------|
| **🔵 Bronce (Raw)** | Datos crudos con trazabilidad completa | Datos sin transformar + metadatos de ingesta |
| **⚪ Plata (Clean)** | Datos validados y normalizados | Datos limpios, validados y deduplicados |
| **🟡 Oro (Gold)** | KPIs y métricas analíticas | Agregaciones, KPIs y métricas de negocio |

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

- Python 3.11+
- pip
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/uxentio/BDA_Proyecto_UT1_RA1.git
cd BDA_Proyecto_UT1_RA1
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

**Activar el entorno virtual:**

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r project/requirements.txt
```

### 4. Generar datos de ejemplo

```bash
python project/ingest/get_data.py
```

Este comando crea:
- `project/input/gastos.csv` - 500+ registros de gastos mensuales
- `project/input/presupuesto.csv` - Presupuesto por área y partida

### 5. Ejecutar pipeline ETL

```bash
python project/ingest/run.py
```

El pipeline ejecuta automáticamente:
1. **Capa Bronce:** Ingesta con trazabilidad completa
2. **Capa Plata:** Validación, limpieza y deduplicación
3. **Capa Oro:** Cálculo de KPIs y métricas

### 6. Ver el reporte

El reporte se genera automáticamente en:

```
project/output/reporte.md
```

También puedes verlo en formato HTML en el sitio web del proyecto.

---

## 📊 Resultados

Después de ejecutar el pipeline completo:

| Métrica | Valor |
|---------|-------|
| **Registros procesados** | 504 gastos |
| **Registros válidos** | 479 (95% tasa de éxito) |
| **Registros en cuarentena** | 12 (errores de validación) |
| **Duplicados eliminados** | 13 (política "último gana") |
| **Áreas analizadas** | 5 (Ventas, Marketing, IT, RRHH, Operaciones) |

### 📁 Archivos Generados

```
project/data/
├── bronce/
│   └── gastos_raw.parquet           # Datos crudos + trazabilidad
├── plata/
│   └── gastos_clean.parquet         # Datos limpios
├── oro/
│   ├── kpi_ejecucion.parquet        # KPIs calculados
│   └── analytics.db                 # Base SQLite
└── quarantine/
    └── invalid_records.parquet      # Registros rechazados
```

---

## 🛠️ Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.11+ | Lenguaje principal |
| **Pandas** | Latest | Procesamiento de datos |
| **NumPy** | Latest | Operaciones numéricas |
| **Apache Parquet** | Latest | Almacenamiento columnar eficiente |
| **SQLite** | 3.x | Base de datos analítica |
| **UUID** | Built-in | Trazabilidad única |
| **GitHub Pages** | - | Publicación web |

---

## 📁 Estructura del Proyecto

```
BDA_Proyecto_UT1_RA1/
│
├── project/
│   ├── ingest/
│   │   ├── get_data.py              # Generador de datos de ejemplo
│   │   └── run.py                   # Pipeline ETL principal
│   │
│   ├── tools/
│   │   └── copy_report_to_site.py   # Copia reporte a GitHub Pages
│   │
│   ├── input/                       # Datos de entrada (CSV)
│   │   ├── gastos.csv
│   │   └── presupuesto.csv
│   │
│   ├── data/                        # Almacenamiento por capas
│   │   ├── bronce/                  # Capa Raw
│   │   ├── plata/                   # Capa Clean
│   │   ├── oro/                     # Capa Gold
│   │   └── quarantine/              # Registros inválidos
│   │
│   ├── output/
│   │   └── reporte.md               # Reporte Markdown generado
│   │
│   └── requirements.txt             # Dependencias Python
│
├── docs/                            # Documentación técnica
│   ├── ingestion.md                 # Proceso de ingesta (Bronce)
│   ├── cleaning.md                  # Limpieza de datos (Plata)
│   └── kpis.md                      # Cálculo de KPIs (Oro)
│
├── site/                            # GitHub Pages
│   └── public/
│       ├── index.html
│       └── reporte.html
│
└── README.md                        # Este archivo
```

---

## 📚 Documentación Técnica

Documentación detallada por cada fase del proceso ETL:

- **[Proceso de Ingesta](./docs/ingestion.md)** - Capa Bronce: ingesta raw con trazabilidad
- **[Limpieza de Datos](./docs/cleaning.md)** - Capa Plata: validaciones y transformaciones
- **[Cálculo de KPIs](./docs/kpis.md)** - Capa Oro: métricas y agregaciones de negocio

---

## ✨ Características Principales

### 🔄 Idempotencia
- ✅ Reprocesar el pipeline no genera duplicados
- ✅ Mismo resultado con múltiples ejecuciones
- ✅ Control mediante `batch_id` único por ejecución

### 🔍 Trazabilidad Completa
- ✅ Cada registro incluye: `_ingest_ts`, `_batch_id`, `_event_id`
- ✅ Auditoría completa del flujo de datos
- ✅ Identificadores únicos con UUID

### 🚨 Sistema de Cuarentena
- ✅ Registros inválidos NO se pierden
- ✅ Documentación de la causa de rechazo
- ✅ Almacenamiento separado para análisis posterior

### 🔄 Deduplicación Inteligente
- ✅ Clave natural: `(fecha, area, partida)`
- ✅ Política: "Último gana" basado en `_ingest_ts`
- ✅ Conservación de la versión más reciente

### 💰 Precisión Financiera
- ✅ Montos almacenados como `DECIMAL(18,2)`
- ✅ Sin errores de redondeo
- ✅ Cumple estándares contables

### 📄 Reportes Automáticos
- ✅ Generación automática en Markdown
- ✅ Exportación a HTML para web
- ✅ Tablas formateadas y KPIs claros

---

## 🎯 Decisiones Técnicas

### 🏛️ Arquitectura

**Medallion Architecture (3 capas):**

1. **Bronce (Raw):**
   - Datos tal como llegan de la fuente
   - Transformación mínima
   - Trazabilidad completa con metadatos

2. **Plata (Clean):**
   - Validaciones aplicadas
   - Transformaciones de limpieza
   - Deduplicación con política definida

3. **Oro (Gold):**
   - KPIs calculados
   - Agregaciones de negocio
   - Listo para consumo analítico

**Justificación:** Separación clara de responsabilidades, facilita debugging, permite reingesta selectiva por capa.

---

### 🔍 Trazabilidad

**Campos añadidos a cada registro:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `_ingest_ts` | DATETIME | Timestamp de ingesta (UTC) |
| `_batch_id` | UUID | Identificador de ejecución del pipeline |
| `_event_id` | UUID | Identificador único del registro |

**Justificación:** Permite auditoría completa, identificación de origen, troubleshooting y cumplimiento normativo.

---

### 🔄 Deduplicación

**Clave natural:** `(fecha, area, partida)`

**Política implementada:** "Último gana" - Se conserva el registro con `_ingest_ts` más reciente.

**Ejemplo:**
```
Registro 1: 2024-01-15, IT, Software, 1000€, _ingest_ts: 2024-11-01 10:00
Registro 2: 2024-01-15, IT, Software, 1200€, _ingest_ts: 2024-11-01 11:00

✅ Se conserva: Registro 2 (más reciente)
```

**Justificación:** En contextos financieros, las correcciones posteriores deben prevalecer sobre datos históricos.

---

### 🚨 Sistema de Cuarentena

**Ubicación:** `project/data/quarantine/invalid_records.parquet`

**Contenido de cada registro rechazado:**
- Registro completo original
- Causa específica del rechazo
- Timestamp del rechazo
- Batch_id de la ejecución

**Tipos de validación que envían a cuarentena:**
- Fechas fuera de rango (futuras o muy antiguas)
- Importes negativos o cero
- Áreas no válidas
- Partidas inexistentes en catálogo
- Campos obligatorios nulos

**Justificación:** No perder información, permitir análisis de calidad de datos, posibilitar corrección manual y reingesta.

---

### 💾 Almacenamiento

**Apache Parquet:**
- ✅ Formato columnar eficiente
- ✅ Compresión automática (reduce 60-70% espacio)
- ✅ Compatible con todo el ecosistema Big Data
- ✅ Lectura selectiva de columnas
- ✅ Tipos de datos fuertemente tipados

**SQLite:**
- ✅ Consultas SQL ad-hoc sin servidor
- ✅ Ideal para análisis local
- ✅ Vistas pre-calculadas para dashboards
- ✅ Cero configuración

**Justificación:** Parquet para almacenamiento eficiente y escalable, SQLite para queries analíticas rápidas en desarrollo.

---

### 💰 Tipos de Datos Financieros

**Montos en DECIMAL(18,2):**
```
DECIMAL(18,2)
       │  │
       │  └─ 2 decimales (céntimos)
       └──── 16 dígitos enteros (hasta 999,999,999,999,999.99)
```

**Evita problemas de FLOAT:**
```python
# ❌ MAL: FLOAT
0.1 + 0.2 = 0.30000000000000004

# ✅ BIEN: DECIMAL
0.1 + 0.2 = 0.30
```

**Justificación:** Estándar en sistemas financieros y contables, garantiza precisión absoluta, evita errores de redondeo acumulativos.

---

## 🧪 Ejemplo de Ejecución

```bash
# 1. Activar entorno
.venv\Scripts\activate

# 2. Generar datos
python project/ingest/get_data.py
# Output: ✅ Generados 504 registros en gastos.csv
#         ✅ Generados 15 presupuestos en presupuesto.csv

# 3. Ejecutar pipeline
python project/ingest/run.py
# Output: 🔵 BRONCE: 504 registros ingestados
#         ⚪ PLATA: 479 registros limpios, 12 en cuarentena
#         🟡 ORO: KPIs calculados para 5 áreas
#         ✅ Pipeline completado exitosamente

# 4. Ver reporte
type project\output\reporte.md
```

---

## 📈 KPIs Calculados

### KPI de Ejecución por Área

```
KPI_Ejecución = (Gasto Acumulado / Presupuesto Anual) × 100
```

**Interpretación:**
- **< 80%:** Sub-ejecución (posible infrautilización)
- **80-95%:** Ejecución saludable
- **95-100%:** Ejecución óptima
- **> 100%:** Sobre-ejecución (requiere análisis)

### Métricas Adicionales

- **Desviación Presupuestaria:** `Gasto Real - Presupuesto`
- **Tasa de Variación:** `((Gasto - Presupuesto) / Presupuesto) × 100`
- **Gasto Promedio Mensual:** `Gasto Total / 12 meses`

---

## 🔒 Supuestos y Limitaciones

### Supuestos del Proyecto

1. **Periodo fiscal:** Año natural (enero-diciembre)
2. **Moneda:** Euro (EUR)
3. **IVA:** No incluido en los importes (precios netos)
4. **Frecuencia de actualización:** Mensual
5. **Áreas fijas:** Catálogo cerrado de 5 áreas

### Limitaciones Conocidas

1. **Datos de ejemplo:** Generados sintéticamente (no son datos reales)
2. **Escalabilidad:** Diseñado para datasets de millones de registros, no billions
3. **Concurrencia:** No hay control de concurrencia multi-usuario
4. **Validaciones:** Reglas de negocio simplificadas para propósito académico

---

## 🎓 Aprendizajes Clave

### Técnicos
- ✅ Implementación de arquitectura Medallion
- ✅ Gestión de idempotencia en pipelines ETL
- ✅ Uso de Parquet para almacenamiento eficiente
- ✅ Validaciones de datos con sistema de cuarentena
- ✅ Generación automática de reportes

### Conceptuales
- ✅ Importancia de la trazabilidad en datos financieros
- ✅ Trade-offs entre normalización y denormalización
- ✅ Políticas de deduplicación según contexto de negocio
- ✅ Separación de capas por nivel de transformación

---

## 🚀 Posibles Mejoras Futuras

### Funcionales
- [ ] Agregar análisis de tendencias temporales
- [ ] Implementar alertas automáticas por desviaciones
- [ ] Incluir comparativas interanuales
- [ ] Dashboard interactivo con visualizaciones

### Técnicas
- [ ] Migrar a Apache Spark para mayor escalabilidad
- [ ] Implementar streaming con Kafka
- [ ] Agregar tests unitarios y de integración
- [ ] CI/CD con GitHub Actions
- [ ] Contenedorización con Docker

---

## 📄 Licencia

Este proyecto es de uso **académico** para la asignatura Big Data Aplicado.

**Prohibido:**
- ❌ Uso comercial
- ❌ Redistribución sin atribución

**Permitido:**
- ✅ Uso educativo
- ✅ Modificación personal
- ✅ Aprendizaje y referencia

---

## 👤 Autor

**Antonio Ferrer Martínez**  
Proyecto UT1 - Big Data Aplicado  
Noviembre 2024


---

## 🔗 Enlaces del Proyecto

- **📂 Repositorio GitHub:** [github.com/uxentio/BDA_Proyecto_UT1_RA1](https://github.com/uxentio/BDA_Proyecto_UT1_RA1)
- **🌐 Sitio Web:** [uxentio.github.io/BDA_Proyecto_UT1_RA1](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)
- **📊 Reporte HTML:** [Ver Reporte Interactivo](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/reporte.html)
- **📚 Documentación:** [/docs](./docs/)

---

## 🙏 Agradecimientos

- **Prof. Rubén Valentín** - Por el repositorio base y guía del proyecto
- **Compañeros de clase** - Por el feedback y colaboración
- **Comunidad Python** - Por las excelentes librerías open-source

---

## 📝 Notas de Versión

### v1.0.0 (Noviembre 2024)
- ✅ Pipeline ETL completo implementado
- ✅ Arquitectura Medallion de 3 capas
- ✅ Sistema de trazabilidad y cuarentena
- ✅ Generación automática de reportes
- ✅ Publicación en GitHub Pages

---

**¿Preguntas o sugerencias?**  
Abre un [issue en GitHub](https://github.com/uxentio/BDA_Proyecto_UT1_RA1/issues) o contacta directamente al autor.

**¡Gracias por revisar este proyecto! 🚀**

- **Repositorio:** [github.com/uxentio/BDA_Proyecto_UT1_RA1](https://github.com/uxentio/BDA_Proyecto_UT1_RA1)
- **Sitio Web:** [uxentio.github.io/BDA_Proyecto_UT1_RA1](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)
