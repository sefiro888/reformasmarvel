# Reformarvel Construcciones

Web estática con inicio, once servicios independientes y dos plantillas legales pendientes de completar. Los originales PNG se conservan. Las imágenes se identifican como ilustrativas; no se atribuyen a trabajos reales ni se usan en comparadores de antes y después.

## Previsualizar

Desde esta carpeta:

```powershell
python -m http.server 8910 --directory dist
```

Abrir http://127.0.0.1:8910/.

## Editar

- `contact-config.json`: teléfono y correo confirmados, Instagram, dirección facilitada y origen de la web.
- `build.py`: textos y estructura de las 14 páginas. Ejecutar `python build.py` para regenerar.
- `styles.css` y `app.js`: diseño y menú/formulario accesibles.
- `asset-catalog.json`: relación entre imágenes originales y versiones optimizadas.

La regeneración necesita Python y Pillow (`python -m pip install Pillow`). Los PNG originales permanecen en esta carpeta; la copia alojada conserva las versiones WebP optimizadas y puede regenerar el HTML sin los PNG. Las tipografías se sirven localmente y sus licencias están en `fonts/`.

El formulario solo prepara un correo o copia la solicitud. No existe backend ni confirmación ficticia de envío. No se ha habilitado WhatsApp. No se han integrado mapas, analítica ni cookies de seguimiento.

Pendientes antes de utilizar como web comercial definitiva: verificar dirección, aportar razón social/NIF/domicilio legal y completar las páginas legales. Si se facilitan obras reales, pueden incorporarse después de verificar su procedencia y correspondencia. Las parejas ilustrativas aportadas no justifican un comparador de trabajos reales.
