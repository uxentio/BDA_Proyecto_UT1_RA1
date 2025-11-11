---
title: Proyecto ETL - Finanzas
---

# Bienvenido al Proyecto ETL Finanzas

Este sitio documenta el proyecto de **analisis de ejecucion presupuestaria** desarrollado para la asignatura Big Data Aplicado.

---

## Navegacion Rapida

### [Reporte de Ejecucion Presupuestaria](reportes/reporte-UT1)
**Ultimo reporte generado** con KPIs, analisis por area y tendencias mensuales.

### Documentacion Tecnica

- **[Proceso de Ingesta](../docs/ingestion)** - Capa Bronce y trazabilidad
- **[Limpieza de Datos](../docs/cleaning)** - Capa Plata y validaciones
- **[Calculo de KPIs](../docs/kpis)** - Capa Oro y metricas analiticas

---

## Sobre el Proyecto

### Objetivo
Implementar un pipeline ETL completo que procesa datos financieros (gastos y presupuestos) para calcular el **KPI de ejecucion presupuestaria** por area organizacional.

### KPI Principal
```
KPI_Ejecucion = (Gasto Acumulado / Presupuesto Anual) Ã— 100
```

### Arquitectura
- **Bronce (Raw):** Datos crudos con trazabilidad
- **Plata (Clean):** Datos validados y normalizados
- **Oro (Gold):** KPIs y metricas analiticas

---

## Tecnologias

- **Python 3.11+** - Lenguaje principal
- **Pandas** - Procesamiento de datos
- **Apache Parquet** - Almacenamiento columnar
- **SQLite** - Base de datos analitica
- **Quartz** - Publicacion web

---

## Repositorio

Ver codigo en GitHub: [github.com/uxentio/BDA_Proyecto_UT1_RA1](https://github.com/uxentio/BDA_Proyecto_UT1_RA1)

---

## Autor

**Antonio [Tu Apellido]**  
Proyecto UT1 - Big Data Aplicado  
Noviembre 2024

