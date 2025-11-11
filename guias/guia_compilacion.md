# 🚀 GUÍA COMPLETA: Cómo Ejecutar y Subir el Proyecto a GitHub

Esta guía te llevará paso a paso desde cero hasta tener tu proyecto funcionando y publicado en GitHub.

---

## 📋 PARTE 1: PREPARAR TU COMPUTADORA

### 1.1 Instalar Python

**Windows:**
1. Ve a https://www.python.org/downloads/
2. Descarga Python 3.11 o superior
3. Durante la instalación, **marca la casilla "Add Python to PATH"** ✅
4. Verifica la instalación:
   ```cmd
   python --version
   ```
   Debe mostrar algo como: `Python 3.11.x`

**Mac:**
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

### 1.2 Instalar Git

**Windows:**
1. Descarga Git desde: https://git-scm.com/download/win
2. Instala con las opciones por defecto
3. Verifica:
   ```cmd
   git --version
   ```

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

### 1.3 Crear Cuenta en GitHub (si no tienes)

1. Ve a https://github.com
2. Crea una cuenta gratuita
3. Verifica tu email

---

## 📁 PARTE 2: CREAR LA ESTRUCTURA DEL PROYECTO

### 2.1 Crear Carpeta del Proyecto

**Windows (CMD o PowerShell):**
```cmd
cd C:\Users\TU_USUARIO\Desktop
mkdir proyecto-finanzas
cd proyecto-finanzas
```

**Mac/Linux:**
```bash
cd ~/Desktop
mkdir proyecto-finanzas
cd proyecto-finanzas
```

### 2.2 Crear Todas las Carpetas

Copia y pega este comando completo:

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Path ".github\workflows", "project\data\raw", "project\data\clean", "project\data\gold", "project\data\quarantine", "project\ingest", "project\output", "project\tools", "docs", "site\content\reportes" -Force
```

**Mac/Linux:**
```bash
mkdir -p .github/workflows project/data/{raw,clean,gold,quarantine} project/{ingest,output,tools} docs site/content/reportes
```

### 2.3 Crear Archivos Vacíos .gitkeep

Estos mantienen las carpetas vacías en Git:

**Windows:**
```powershell
New-Item -ItemType File -Path "project\data\.gitkeep", "project\data\raw\.gitkeep", "project\data\clean\.gitkeep", "project\data\gold\.gitkeep", "project\data\quarantine\.gitkeep"
```

**Mac/Linux:**
```bash
touch project/data/.gitkeep project/data/{raw,clean,gold,quarantine}/.gitkeep
```

---

## 🐍 PARTE 3: COPIAR EL CÓDIGO PYTHON

### 3.1 Crear `project/ingest/get_data.py`

1. Abre un editor de texto (Notepad++, VS Code, o el Bloc de notas)
2. Copia TODO el código del artifact **"get_data.py"** que te proporcioné
3. Guárdalo como: `project/ingest/get_data.py`

### 3.2 Crear `project/ingest/run.py`

1. Copia TODO el código del artifact **"run.py"**
2. Guárdalo como: `project/ingest/run.py`

### 3.3 Crear `project/tools/copy_report_to_site.py`

1. Copia el código del artifact **"copy_report_to_site.py"**
2. Guárdalo como: `project/tools/copy_report_to_site.py`

---

## 📦 PARTE 4: COPIAR ARCHIVOS DE CONFIGURACIÓN

### 4.1 `project/requirements.txt`
Copia el contenido del artifact **"requirements.txt"**

### 4.2 `project/environment.yml`
Copia el contenido del artifact **"environment.yml"**

### 4.3 `README.md` (raíz del proyecto)
Copia el contenido del artifact **"README.md"**

### 4.4 `.gitignore` (raíz del proyecto)
Copia el contenido del artifact **".gitignore"**

### 4.5 `.github/workflows/deploy-pages.yml`
Copia el contenido del artifact **"deploy-pages.yml"**

---

## 📚 PARTE 5: COPIAR DOCUMENTACIÓN

### 5.1 `docs/ingestion.md`
Copia el contenido del artifact **"docs/ingestion.md"**

### 5.2 `docs/cleaning.md`
Copia el contenido del artifact **"docs/cleaning.md"**

### 5.3 `docs/kpis.md`
Copia el contenido del artifact **"docs/kpis.md"**

---

## ⚙️ PARTE 6: INSTALAR DEPENDENCIAS Y EJECUTAR

### 6.1 Crear Entorno Virtual

**Windows:**
```cmd
cd proyecto-finanzas
python -m venv .venv
.venv\Scripts\activate
```

Verás que tu prompt cambia a algo como: `(.venv) C:\...\proyecto-finanzas>`

**Mac/Linux:**
```bash
cd proyecto-finanzas
python3 -m venv .venv
source .venv/bin/activate
```

Verás: `(.venv) usuario@computadora:~/proyecto-finanzas$`

### 6.2 Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r project/requirements.txt
```

Esto instalará:
- pandas
- numpy
- pyarrow
- jupyter

Espera unos minutos mientras se descargan e instalan.

### 6.3 Generar Datos de Ejemplo

```bash
python project/ingest/get_data.py
```

**Salida esperada:**
```
📊 Generando gastos.csv...
   ✅ gastos.csv creado: 504 registros
📊 Generando presupuesto.csv...
   ✅ presupuesto.csv creado: 5 registros
🎉 Datos de ejemplo generados correctamente
```

### 6.4 Ejecutar el Pipeline Completo

```bash
python project/ingest/run.py
```

**Esto ejecutará TODO el ETL:**
- ✅ Ingesta con trazabilidad
- ✅ Limpieza y validación
- ✅ Cálculo de KPIs
- ✅ Almacenamiento en Parquet + SQLite
- ✅ Generación del reporte

**Duración:** ~10-30 segundos

**Salida esperada (resumen):**
```
╔══════════════════════════════════════════════════════╗
║  🏦 PIPELINE ETL - FINANZAS (Presupuesto vs Gasto)  ║
╚══════════════════════════════════════════════════════╝

🔵 FASE 1: INGESTA - CAPA BRONCE (RAW)
📥 Ingiriendo: project/data/gastos.csv
   ✅ Registros cargados: 504
...

✅ PIPELINE COMPLETADO EXITOSAMENTE

📊 Resumen de Procesamiento:
   • Registros procesados: 504 gastos
   • Registros válidos: 485 gastos
   • Registros en cuarentena: 19
   • KPIs generados: 5 áreas
```

### 6.5 Ver el Reporte

Abre el archivo:
```
project/output/reporte.md
```

Con cualquier editor de texto o visualizador de Markdown (VS Code, Typora, etc.)

---

## 🐙 PARTE 7: SUBIR A GITHUB

### 7.1 Configurar Git (primera vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

### 7.2 Crear Repositorio en GitHub

1. Ve a https://github.com
2. Clic en el botón **"+"** (arriba derecha) → **"New repository"**
3. Configura:
   - **Repository name:** `proyecto-finanzas-ut1`
   - **Description:** `Proyecto ETL - Finanzas (Presupuesto vs Gasto)`
   - **Visibility:** Private (o Public si prefieres)
   - **NO marques** "Add a README file" (ya lo tienes)
4. Clic en **"Create repository"**

### 7.3 Inicializar Git Localmente

Desde la carpeta `proyecto-finanzas`:

```bash
git init
git add .
git commit -m "Initial commit: Proyecto ETL Finanzas UT1"
```

### 7.4 Conectar con GitHub

Copia los comandos que te muestra GitHub (sección "…or push an existing repository"):

```bash
git remote add origin https://github.com/TU_USUARIO/proyecto-finanzas-ut1.git
git branch -M main
git push -u origin main
```

**Te pedirá credenciales:**
- Usuario: tu usuario de GitHub
- Contraseña: usa un **Personal Access Token** (no tu contraseña real)

#### Crear Personal Access Token:
1. GitHub → Settings (tu perfil)
2. Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token → Marcar: `repo`, `workflow`
4. Copiar el token y úsalo como contraseña

### 7.5 Verificar en GitHub

1. Ve a tu repositorio: `https://github.com/TU_USUARIO/proyecto-finanzas-ut1`
2. Deberías ver todos los archivos

---

## 🌐 PARTE 8: PUBLICAR EN GITHUB PAGES (OPCIONAL - BONUS)

### 8.1 Habilitar GitHub Pages

1. En tu repositorio GitHub: **Settings** → **Pages**
2. En "Source": Selecciona **GitHub Actions**
3. Guarda

### 8.2 Configurar Quartz (solo si quieres publicar web)

```bash
cd site
npm install
npx quartz create content
```

Sigue el asistente y selecciona "Empty Quartz".

### 8.3 Copiar Reporte a Quartz

```bash
cd ..  # Volver a la raíz
python project/tools/copy_report_to_site.py
```

### 8.4 Subir Cambios

```bash
git add .
git commit -m "Configurar Quartz y añadir reporte"
git push
```

El workflow de GitHub Actions se ejecutará automáticamente y publicará tu sitio.

**URL:** `https://TU_USUARIO.github.io/proyecto-finanzas-ut1/`

---

## 📄 PARTE 9: GENERAR EL PDF PARA ENTREGAR

### 9.1 Exportar Reporte a PDF

**Opción 1: Con VS Code**
1. Abre `project/output/reporte.md` en VS Code
2. Instala extensión: "Markdown PDF"
3. Clic derecho → "Markdown PDF: Export (pdf)"

**Opción 2: Con Typora**
1. Abre el reporte en Typora (https://typora.io/)
2. File → Export → PDF

**Opción 3: Con pandoc (línea de comandos)**
```bash
pandoc project/output/reporte.md -o reporte.pdf
```

### 9.2 Crear PDF de Decisiones

Crea un nuevo archivo `apellido1_apellido2_nombre_ProyectoUT1.pdf` con:

**Página 1: Reporte**
- Pega el contenido del reporte.md

**Página 2: Decisiones Técnicas**
```
DECISIONES DE DISEÑO

1. INGESTA:
   - Implementado batch processing con batch_id único
   - Trazabilidad completa (_ingest_ts, _source_file, _event_id)
   - Idempotencia por nombrado de archivos con batch_id

2. LIMPIEZA:
   - Clave natural: (fecha, area, partida)
   - Política de deduplicación: "Último gana" por _ingest_ts
   - Cuarentena con 4 tipos de validaciones
   - Importes como DECIMAL(18,2) para precisión financiera

3. KPIs:
   - KPI principal: Ejecución = (Gasto / Presupuesto) × 100
   - Estados: Bajo Consumo (<70%), Normal (70-89%), Riesgo (90-100%), Crítico (>100%)
   - Vista SQL automática para análisis

4. ALMACENAMIENTO:
   - Parquet con particionado temporal (batch_id)
   - SQLite para consultas SQL ad-hoc
   - Separación clara Bronce → Plata → Oro
```

**Página 3: Lecciones Aprendidas**
```
LECCIONES APRENDIDAS

1. Trazabilidad: Añadir metadatos desde el inicio simplifica debugging
2. Cuarentena vs eliminación: Mejor guardar registros inválidos que eliminarlos
3. DECIMAL > FLOAT: Para dinero, evita errores de redondeo
4. Documentación: Las decisiones de negocio deben estar documentadas
5. Automatización: Un pipeline reproducible ahorra tiempo en actualizaciones
```

---

## ✅ PARTE 10: ENTREGA FINAL

Entrega en la plataforma:

1. **URL del repositorio GitHub:**
   ```
   https://github.com/TU_USUARIO/proyecto-finanzas-ut1
   ```

2. **Archivo PDF:**
   - Nombre: `apellido1_apellido2_nombre_ProyectoUT1.pdf`
   - Contenido: Reporte + Decisiones + Lecciones

3. **(Opcional) URL de Quartz:**
   ```
   https://TU_USUARIO.github.io/proyecto-finanzas-ut1/
   ```

4. **Comentarios adicionales:**
   ```
   Proyecto implementado con:
   - Arquitectura de 3 capas (Bronce, Plata, Oro)
   - Trazabilidad completa con batch_id y event_id
   - Sistema de cuarentena con 4 validaciones
   - Almacenamiento dual: Parquet + SQLite
   - Reporte Markdown con definiciones de KPI
   
   Ejecutable con: python project/ingest/run.py
   ```

---

## 🆘 RESOLUCIÓN DE PROBLEMAS

### Problema: "python: command not found"
**Solución:** Instala Python correctamente y asegúrate de que esté en el PATH

### Problema: "ModuleNotFoundError: No module named 'pandas'"
**Solución:** 
```bash
pip install -r project/requirements.txt
```

### Problema: "Permission denied" al ejecutar scripts
**Solución (Mac/Linux):**
```bash
chmod +x project/ingest/*.py
```

### Problema: Git pide usuario/contraseña constantemente
**Solución:** Usa un Personal Access Token (ver Parte 7.4)

### Problema: "No se encuentra gastos.csv"
**Solución:**
```bash
python project/ingest/get_data.py
```

### Problema: El reporte.md está vacío
**Solución:** Ejecuta el pipeline completo:
```bash
python project/ingest/run.py
```

---

## 📞 CONTACTO PARA LA ENTREVISTA

Prepárate para explicar:

1. **Arquitectura de 3 capas:** Bronce (raw), Plata (clean), Oro (analytics)
2. **Trazabilidad:** `_ingest_ts`, `_batch_id`, `_event_id`, `_source_file`
3. **Idempotencia:** Reprocesar no duplica gracias al batch_id único
4. **Deduplicación:** Clave natural (fecha, area, partida) + "último gana"
5. **Cuarentena:** 4 validaciones (nulos, tipos, rangos, dominios)
6. **KPI:** `(Gasto Acumulado / Presupuesto Anual) × 100`
7. **DECIMAL vs FLOAT:** Precisión financiera (2 decimales)

---

## 🎉 ¡LISTO!

Has completado:
- ✅ Pipeline ETL funcional
- ✅ Código limpio y documentado
- ✅ Repositorio en GitHub
- ✅ Reporte profesional
- ✅ Documentación técnica completa
- ✅ (Opcional) Web publicada

**¡Mucha suerte con la entrega y la entrevista! 🚀**
