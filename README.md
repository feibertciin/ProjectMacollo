# Macollo · Plataforma de Agricultura Inteligente

Landing, cuaderno de análisis y dashboard interactivo para documentar la **ingeniería de datos** del invernadero Macollo: ingesta, limpieza, análisis exploratorio, transformación con One Hot Encoding y despliegue en Streamlit.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![pandas](https://img.shields.io/badge/pandas-2.2-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9-11557C?logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4C72B0)](https://seaborn.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.24-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Jupyter](https://img.shields.io/badge/Jupyter-nbconvert-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![HTML5](https://img.shields.io/badge/HTML5-Landing-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-2E8B57)](https://opensource.org/licenses/MIT)

---

## Descripción

Macollo convierte **540 mediciones** del invernadero (26 fechas, 4 tratamientos y 5 plantas por fila) en un flujo de datos reproducible y listo para analítica avanzada. El proyecto incluye tres entregables:

| Entregable | Archivo | Descripción |
|---|---|---|
| Landing | `landing.html` | Página de aterrizaje que explica la ingeniería de datos del proyecto. |
| Aplicación | `app.py` | Dashboard interactivo en Streamlit + visor y ejecutor del cuaderno. |
| Cuaderno | `Cuaderno1_macollo.ipynb` | ETL, EDA, One Hot Encoding y dashboard por fecha. |

El reporte ejecutivo exportado se encuentra en `dashboard_reporte.html`.

---

## Características

- **Landing autocontenida** con el pipeline, diccionario de datos, decisiones de calidad y stack tecnológico.
- **Dashboard interactivo** filtrable por fecha, responsable, tratamiento y planta.
- **KPIs y visualizaciones**: mapa de calor de alturas, barras por tratamiento, histogramas, boxplots, evolución temporal y correlaciones.
- **Cuaderno integrado**: se puede leer, descargar o ejecutar desde la app; al ejecutarlo se regeneran los CSV y un reporte HTML con todas las salidas.
- **Inspector de datos** para los tres estados: original, limpio y transformado.
- **Tema visual propio** (verde/teal) coherente entre la landing, el reporte y la aplicación.

---

## Pipeline de datos

```
Data_Mocollo1.csv
        │
        ▼
 Extracción e inspección  →  Limpieza ETL  →  EDA  →  One Hot Encoding
        │
        ▼
Data_Mocollo1_Limpio.csv  ──►  Data_Mocollo1_Transformado.csv
        │
        ▼
 Streamlit (dashboard) + landing.html + dashboard_reporte.html
```

### Decisiones de limpieza

- Conversión de decimales europeos (coma → punto).
- Conversión de fechas `dd/mm/aaaa` a `datetime`.
- Normalización de la humedad relativa al rango `0-1` (60 registros venían como porcentaje).
- Nulos conservados como ausencia de lectura (sin imputación artificial).
- Outliers detectados por IQR: se marcan, no se eliminan.
- One Hot Encoding sobre `Responsable`, `Fila`, `Planta` e `ID_Planta`.

### Resultado de la transformación

| Estado | Filas | Columnas |
|---|---:|---:|
| Original | 540 | 11 |
| Limpio | 540 | 11 |
| Transformado | 540 | 41 |

---

## Estructura del proyecto

```
Macollo/
├── app.py                        # Aplicación Streamlit
├── landing.html                  # Landing de ingeniería de datos
├── Cuaderno1_macollo.ipynb       # Cuaderno de análisis
├── dashboard_reporte.html        # Reporte ejecutivo exportado
├── requirements.txt              # Dependencias del proyecto
├── README.md                     # Este archivo
├── .streamlit/
│   └── config.toml               # Tema y configuracion de Streamlit
├── Data_Mocollo1.csv             # Dataset original
├── Data_Mocollo1_Limpio.csv      # Dataset limpio
├── Data_Mocollo1_Transformado.csv# Dataset con One Hot Encoding
└── .venv/                        # Entorno virtual local (no versionar)
```

---

## Requisitos

- Python **3.11** (recomendado)
- pip actualizado
- Navegador web moderno
- Sistema operativo: Windows, macOS o Linux

Las versiones exactas de las dependencias están fijadas en `requirements.txt`.

---

## Instalación

### Windows (PowerShell)

```powershell
# 1. Crear el entorno virtual
py -3.11 -m venv .venv

# 2. Activarlo
.\.venv\Scripts\Activate.ps1

# Si PowerShell bloquea la activación, ejecuta una vez:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Registrar el kernel del cuaderno con el entorno virtual
python -m ipykernel install --user --name macollo --display-name "Macollo (venv)"
```

### macOS / Linux

```bash
# 1. Crear el entorno virtual
python3.11 -m venv .venv

# 2. Activarlo
source .venv/bin/activate

# 3. Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Registrar el kernel del cuaderno
python -m ipykernel install --user --name macollo --display-name "Macollo (venv)"
```

---

## Ejecutar la aplicación

Con el entorno virtual activo, desde la carpeta del proyecto:

```powershell
streamlit run app.py
```

La aplicación se abre en **http://localhost:8501**.

Si el navegador no se abre automáticamente, visita la URL. Para cambiar el puerto:

```powershell
streamlit run app.py --server.port 8502
```

### Páginas de la aplicación

1. **Inicio**: resumen del proyecto, pipeline y stack.
2. **Dashboard**: consulta por fecha con filtros y descargas.
3. **Ingeniería de datos**: diccionario, calidad y transformación.
4. **Cuaderno**: vista del `.ipynb`, descarga y ejecución con generación de reporte HTML.
5. **Datos**: previsualización y descarga de los tres datasets.

### Landing y reporte

- Abre `landing.html` directamente en el navegador para ver la landing del proyecto.
- Abre `dashboard_reporte.html` para el reporte ejecutivo de ejemplo (2026-09-22).

---

## Ejecutar el cuaderno

### Desde la aplicación

Ve a la página **Cuaderno** y pulsa **Ejecutar y generar reporte**. La app ejecuta el kernel `macollo`, actualiza los CSV y crea:

```
.cache/cuaderno_ejecutado.ipynb
.cache/cuaderno_ejecutado.html
```

### Desde la terminal

```powershell
jupyter nbconvert --to html --execute Cuaderno1_macollo.ipynb `
    --ExecutePreprocessor.kernel_name=macollo `
    --output Cuaderno1_macollo_ejecutado.html
```

> La primera ejecución puede tardar alrededor de un minuto porque genera todas las gráficas del análisis.

---

## Despliegue en Streamlit Cloud

1. Sube el proyecto a un repositorio de GitHub (sin incluir `.venv/`).
2. Entra a [share.streamlit.io](https://share.streamlit.io/) y conecta el repositorio.
3. Selecciona la rama principal y el archivo **`app.py`** como *main file*.
4. Verifica que `requirements.txt` esté en la raíz del repositorio.
5. Pulsa **Deploy**. Streamlit instalará las dependencias y publicará la app.

La app usa rutas relativas a su propio directorio, por lo que funciona tanto en local como en la nube.

---

## Datos y variables

| Campo | Tipo | Descripción |
|---|---|---|
| `Fecha` | Fecha | Día de la medición (`dd/mm/aaaa`). |
| `Responsable` | Categórica | Persona que registra la medición. |
| `T_Ext_C` | Numérica | Temperatura exterior (°C). |
| `T_Int_C` | Numérica | Temperatura interior del invernadero (°C). |
| `Humedad_Pct` | Numérica | Humedad relativa en proporción (0-1). |
| `Fila` | Categórica | Tratamiento experimental (T0–T3). |
| `Planta` | Categórica | Planta dentro de la fila (P1–P5). |
| `ID_Planta` | Categórica | Clave compuesta fila-planta. |
| `T_Planta_C` | Numérica | Temperatura de la planta (°C). |
| `pH` | Numérica | pH del sustrato. |
| `Altura_cm` | Numérica | Altura de la planta (cm). |

---

## Solución de problemas

| Problema | Solución |
|---|---|
| `El término 'streamlit' no se reconoce` | Activa el entorno virtual: `.\.venv\Scripts\Activate.ps1`. |
| PowerShell no permite activar el entorno | Ejecuta `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. |
| Error al ejecutar el cuaderno | Verifica que el kernel `macollo` esté registrado con `jupyter kernelspec list`. |
| La app no encuentra el dataset | Ejecuta Streamlit desde la carpeta del proyecto (donde está `Data_Mocollo1.csv`). |
| Conflicto de puerto | Usa `--server.port 8502` o cierra la instancia anterior. |

---

## Autor

**Equipo de Data Science · Agricultura Inteligente Macollo**  
Proyecto académico de ingeniería y análisis de datos, 2026.

---

<div align="center">
<sub>Construido con Python, pandas, scikit-learn, Streamlit y muchas mediciones de invernadero.</sub>
</div>
