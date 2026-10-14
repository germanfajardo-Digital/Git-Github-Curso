# Editor local de archivos TXT

Aplicación de escritorio en PyQt5 para abrir, editar y guardar archivos `.txt`
ubicados en la misma carpeta que `app.py`.

## Requisitos

- Python 3.10 o posterior
- PyQt5

## Instalación y ejecución

Desde la carpeta del proyecto, instala la dependencia y ejecuta la aplicación:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Selecciona un archivo de la lista para cargar su contenido. **Guardar** escribe
los cambios en el archivo seleccionado, **Cancelar** deselecciona el archivo y
limpia el editor, y **Salir** cierra la aplicación.
