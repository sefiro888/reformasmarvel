# Reformarvel Construcciones

Web estática premium: portada, «Cómo trabajamos», once páginas de servicio y dos plantillas legales pendientes de completar. Las imágenes son ilustrativas y no se atribuyen a obras reales; los comparadores de antes y después lo indican expresamente.

## Previsualizar

```powershell
python -m http.server 8911 --directory dist
```

Abrir http://127.0.0.1:8911/.

Publicada en https://sefiro888.github.io/reformasmarvel/ (GitHub Pages publica `dist/` automáticamente con cada push a `main`).

## Qué incluye

- Intro de entrada (una vez por visita) y transiciones entre páginas con velo rojo.
- Banner en movimiento en la portada: seis servicios con barrido, zoom lento, barras de progreso, flechas, arrastre y botón de WhatsApp que cambia según el servicio en pantalla.
- Petición a medida por WhatsApp: en la portada eliges oficios; en cada servicio, opciones propias de ese oficio. El mensaje se escribe en directo en un móvil simulado y se abre WhatsApp con todo preparado. No hay formularios por correo ni envíos desde la web.
- Botones de WhatsApp con el servicio ya escrito en la lista de oficios, la cabecera, el botón flotante y las llamadas finales.
- Scroll suave (Lenis), cursor propio, botones magnéticos, inclinación 3D, imagen que sigue al ratón en la lista de oficios, rótulos que reaccionan a la velocidad del scroll, manifiesto que se ilumina al bajar, proceso en recorrido horizontal, galería con parallax y visor, chispas interactivas, nivel de burbuja en la portada.
- Estética de cómic de creación propia (sin personajes, logos ni nombres de Marvel): sección «Toda casa tiene sus villanos», «superpoderes» de cada oficio, viñetas con bocadillos en el proceso, tramas de puntos y onomatopeyas al pulsar botones. El pie aclara que la empresa no tiene relación con Marvel ni con Disney.
- Página «Cómo trabajamos» (`como-trabajamos.html`): método en cuatro capítulos y diez comparadores de antes y después para arrastrar (ratón, dedo o teclado), con filtros por tipo de espacio. Los originales dobles se recortan por la mitad en `build.py`.
- Respeta `prefers-reduced-motion` y funciona en móvil (comprobado a 320, 375, 768, 1024 y 1440 px).

## Editar

- `contact-config.json`: teléfono, WhatsApp, correo, Instagram, dirección y origen de la web.
- `build.py`: textos, servicios y opciones de la petición por WhatsApp de cada oficio. Ejecutar `python build.py` para regenerar `dist/`.
- `styles.css` y `app.js`: diseño e interacción.
- `brand/logo-transparent.webp`: logo sin fondo blanco para la cabecera oscura (generado del logo original, `brand/logo-original.png`).
- `vendor/lenis.min.js`: scroll suave (licencia MIT).
- `og.py`: genera las imágenes para compartir enlaces (1200×630, una por página) y los iconos.
- `check_site.py`: comprueba enlaces, recursos, anclas, títulos y descripciones.

La regeneración necesita Python y Pillow. Busca los PNG originales en esta carpeta o en la carpeta principal del proyecto; si no están, reutiliza las versiones WebP ya generadas. Las tipografías (Barlow Condensed, Manrope, Instrument Serif) se sirven localmente y sus licencias están en `fonts/`.

No se han integrado mapas, analítica ni cookies de seguimiento. Pendientes antes de usarla como web comercial definitiva: verificar la dirección, confirmar que el 652 465 019 tiene WhatsApp activo, aportar razón social/NIF/domicilio legal y completar las páginas legales.
