### One package manager to rule them all

Iniciar el proyecto
```bash
uv init fastapi_uv_setup
```

Instalar/agregar dependencia
```bash
uv add uvicorn
```

Para correr la app
```bash 
uv run uvicorn main:app --reload
```

instalar dependencias 
```bash 
uv install
```

congelar dependencias como pip freeze
```bash
uv export > requirements.txt
```

uv crea automaticamente el entorno virtual e instala los paquetes
- Es como pip + venv + poetry

Congelar dependencias (como pip freeze)
```bash 
uv export > requirements.txt
```