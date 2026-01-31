# botaniCAT
Proyecto en Python para la extracción y procesamiento de datos tabulares desde un sitio web. El script obtiene datos de una tabla web con paginción, selecciona los campos relevantes y los convierte en estructuras de datos manejables en Python.

### Tecnologías y herramientas
- Python
- Requests
- BeautifulSoup
- Pandas
- Estructuras de datos (DataFrames)

### Descripción
botaniCAT es un proyecto en Python orientado a la **recolección y transformación de datos web**. Accede a un sitio web que presenta información en formato de tabla con paginación, recorre las distintas páginas, extrae únicamente los datos de interés y los convierte en tablas utilizables en Python para su posterior análisis o tratamiento.

### Instalación y ejecuión
1. Clonar el repositorio
```bash
git clone https://gitghub.com/androsrivas/botaniCAT.git
```

2. Acceder al directorio del proyecto:
```bash
cd botaniCAT
```

3. Crear y activar un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate # Linux / Mac
venv\Scripts\activate    # Windows
```

4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecutar el script principal:
```bash
python main.py
```

### Funcionalidades implementadas
- Acceso a una tabla de datos publicada en un sitio web.
- Navegación por páginas mediante paginación.
- Extracción selectiva de campos relevantes.
- Conversión de los datos extraídos en tablas (DataFrames) en Python.
- Preparación de los datos para análisis posterior.


### Estructura del proyecto
- `botaniCAT/` - código fuente principal
- `data/` - datos generados o de apoyo
- `requirements.txt` - dependencias del proyecto
- `setup.py` - configuración del paquete

### Estado del proyecto
Proyecto en desarrollo. Las funcionalidades actuales cubren la extracción y estructuración de datos desde una fuente web con paginación.
