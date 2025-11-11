# 📊 Proyecto ETL: Finanzas - Análisis de Ejecución Presupuestaria

**Asignatura:** Big Data Aplicado - UT1  
**Alumno:** Antonio Ferrer Martínez  
**Fecha:** Noviembre 2024

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)

---

## 🌐 Accesos Rápidos

- **🌍 Sitio Web:** [uxentio.github.io/BDA_Proyecto_UT1_RA1](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)
- **📊 Reporte Interactivo:** [Ver Reporte](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/reporte.html)
- **📚 Documentación:** [/docs](./docs/)

---

## 📋 Descripción

Este proyecto implementa un **pipeline ETL completo** que procesa datos financieros (gastos y presupuestos) para calcular el **KPI de ejecución presupuestaria** por área organizacional.

### KPI Principal
\\\
KPI_Ejecución = (Gasto Acumulado / Presupuesto Anual) × 100
\\\

---

## 🏗️ Arquitectura

**Pipeline ETL de 3 Capas (Medallion Architecture):**

- **🔵 Bronce (Raw):** Datos crudos con trazabilidad completa
- **⚪ Plata (Clean):** Datos validados y normalizados
- **🟡 Oro (Gold):** KPIs y métricas analíticas

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.11+
- pip

### 1. Clonar el repositorio
\\\ash
git clone https://github.com/uxentio/BDA_Proyecto_UT1_RA1.git
cd BDA_Proyecto_UT1_RA1
\\\

### 2. Crear entorno virtual
\\\ash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
\\\

### 3. Instalar dependencias
\\\ash
pip install -r project/requirements.txt
\\\

### 4. Generar datos de ejemplo
\\\ash
python project/ingest/get_data.py
\\\

### 5. Ejecutar pipeline ETL
\\\ash
python project/ingest/run.py
\\\

### 6. Ver el reporte
\\\ash
# El reporte se genera en:
project/output/reporte.md
\\\

---

## 📊 Resultados

- **Registros procesados:** 504 gastos
- **Registros válidos:** 479 (95% tasa de éxito)
- **Registros en cuarentena:** 12
- **Duplicados eliminados:** 13
- **Áreas analizadas:** 5

---

## 🛠️ Tecnologías

- **Python 3.11+** - Lenguaje principal
- **Pandas & NumPy** - Procesamiento de datos
- **Apache Parquet** - Almacenamiento columnar
- **SQLite** - Base de datos analítica
- **GitHub Pages** - Publicación web

---

## 📁 Estructura del Proyecto

\\\
BDA_Proyecto_UT1_RA1/
├── project/
│   ├── ingest/
│   │   ├── get_data.py          # Generador de datos
│   │   └── run.py               # Pipeline ETL principal
│   ├── tools/
│   │   └── copy_report_to_site.py
│   ├── data/                    # Datos (bronce/plata/oro)
│   └── output/
│       └── reporte.md           # Reporte generado
├── docs/                        # Documentación técnica
│   ├── ingestion.md
│   ├── cleaning.md
│   └── kpis.md
└── site/                        # GitHub Pages
    └── public/
        ├── index.html
        └── reporte.html
\\\

---

## 📚 Documentación Técnica

- **[Proceso de Ingesta](./docs/ingestion.md)** - Capa Bronce y trazabilidad
- **[Limpieza de Datos](./docs/cleaning.md)** - Capa Plata y validaciones
- **[Cálculo de KPIs](./docs/kpis.md)** - Capa Oro y métricas

---

## ✨ Características Principales

- ✅ **Idempotencia:** Reprocesar no genera duplicados
- ✅ **Trazabilidad completa:** batch_id, event_id (UUID)
- ✅ **Sistema de cuarentena:** Registros inválidos documentados
- ✅ **Deduplicación:** Política "último gana"
- ✅ **Precisión financiera:** DECIMAL(18,2)
- ✅ **Reportes automáticos:** Markdown y HTML

---

## 🎯 Decisiones Técnicas

### Arquitectura
- Implementada arquitectura de 3 capas (Medallion)
- Separación clara de responsabilidades

### Trazabilidad
- Cada registro tiene: \_ingest_ts\, \_batch_id\, \_event_id\
- Permite auditoría completa

### Deduplicación
- Clave natural: (fecha, area, partida)
- Política: "Último gana" por \_ingest_ts\

### Cuarentena
- Registros inválidos guardados con causa
- No se eliminan, se analizan

---

## 📄 Licencia

Este proyecto es de uso académico para la asignatura Big Data Aplicado.

---

## 👤 Autor

**Antonio Ferrer Martínez**  
Proyecto UT1 - Big Data Aplicado  
Noviembre 2024

---

## 🔗 Enlaces

- **Repositorio:** [github.com/uxentio/BDA_Proyecto_UT1_RA1](https://github.com/uxentio/BDA_Proyecto_UT1_RA1)
- **Sitio Web:** [uxentio.github.io/BDA_Proyecto_UT1_RA1](https://uxentio.github.io/BDA_Proyecto_UT1_RA1/)
