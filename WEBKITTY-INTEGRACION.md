# JOSDANY92 + WebKitty: instalación local y prueba offline

## Resultado incorporado a JOSDANY92

En la rama `JOSDANY92-V2.1` ya existe:
- Acceso **WEBKITTY** en el menú principal.
- Apertura manual o automática al entrar en el panel, con retardo configurable de 0 a 90 segundos y botón para cancelar.
- Página `WEBKITTY-LOCAL.html`, que verifica desde Android los recursos del manifiesto específico de PS4 14.02.
- Enlaces al host oficial y al ZIP oficial de WebKitty.

El temporizador solo abre el host elegido. No es un exploit ni activa GoldHEN por sí mismo.

## Descargas oficiales

- Repositorio: https://github.com/ArabPixel/WebKitty
- ZIP oficial completo: https://github.com/ArabPixel/WebKitty/archive/refs/heads/main.zip
- Host oficial: http://webkitty.arabpixel.net/

WebKitty es un proyecto independiente publicado bajo AGPL-3.0-or-later. JOSDANY92 lo enlaza y comprueba la copia local; no sustituye a sus autores ni redistribuye su código.

## Preparación del teléfono Android

Haz esto mientras tengas Internet:

1. Descarga el ZIP de WebKitty desde el enlace oficial.
2. Extrae el ZIP completo. Renombra la carpeta extraída exactamente a `WebKitty`.
3. Descarga y extrae también la rama `JOSDANY92-V2.1` de este repositorio. Deja los archivos de JOSDANY92 en una carpeta llamada `JOSDANY92`.
4. Coloca la carpeta `WebKitty` dentro de la carpeta `JOSDANY92`, al mismo nivel que `index.html`.
5. La estructura debe quedar así:

```
JOSDANY92/
  index.html
  fondo-josdany92.jpg
  josdany92-header.png
  WEBKITTY-LOCAL.html
  ANDROID-OFFLINE.md
  WebKitty/
    index.html
    exploit.html
    cache.html
    includes/
    src/
```

6. En SimpleHttpServer (o servidor HTTP estático equivalente), selecciona la carpeta `JOSDANY92` como raíz. No selecciones solamente la carpeta WebKitty: JOSDANY92 necesita ver su propia página y la subcarpeta.
7. Inicia el servidor y abre en el navegador Android la dirección local que muestre, terminada en `/WEBKITTY-LOCAL.html`.
8. Pulsa **COMPROBAR COPIA LOCAL**. El verificador lee el manifiesto de WebKitty para firmware 14.02 y revisa los recursos requeridos. Si muestra archivos faltantes, vuelve a extraer el ZIP completo y repite la comprobación.

## Conectar la PS4 y preparar la caché

1. Enciende el hotspot Wi-Fi del teléfono y conecta la PS4.
2. Mantén el servidor HTTP de Android encendido.
3. En el navegador PS4 abre la dirección local del servidor seguida de `/WebKitty/index.html`. Ejemplo ilustrativo: `http://192.168.43.1:8080/WebKitty/index.html`. Sustituye IP y puerto por los valores reales del servidor.
4. WebKitty detecta el firmware. Su código comprueba `window.applicationCache`; si la caché no está preparada y la API está disponible, redirige a su flujo de caché específico.
5. Espera a que finalice la descarga de recursos y regrese a la página principal. No cierres el navegador durante el proceso.
6. Vuelve a abrir la misma URL local para confirmar que la página carga mientras el teléfono sigue conectado.

## Prueba sin teléfono, sin Wi-Fi y sin Internet

Esta es la prueba decisiva; no puede hacerse desde el teléfono ni confirmarse desde GitHub:

1. Cierra el navegador PS4 normalmente después de preparar la caché.
2. Apaga el hotspot y detén el servidor del teléfono.
3. Abre el navegador PS4 y, desde el historial, selecciona exactamente la misma dirección local usada antes (mismo protocolo, IP, puerto y ruta).
4. Si WebKitty carga sin que el teléfono ni el servidor estén activos, la caché offline funciona en esa consola.
5. Si no carga, la prueba no pasó. Vuelve a conectar el teléfono; no asumas que quedó cacheado.

La caché está vinculada al origen exacto. Si cambia la IP o el puerto, puede no encontrar los recursos guardados. El navegador PS4 debe conservar soporte para Application Cache. El verificador Android solo comprueba que los archivos existen y se sirven correctamente; no puede inspeccionar el almacenamiento interno del navegador PS4.

## Firmware 14.02 y estabilidad

El README oficial de WebKitty lista Slopkit / Afterglow para firmware 14.00–14.02. Eso es compatibilidad declarada por el proyecto, no garantía de éxito ni de estabilidad en cada PS4. No hay método que garantice evitar kernel panic, congelamientos o pantalla negra. Conserva copias de seguridad y evita repetir intentos tras un bloqueo.

## Limitaciones conocidas

- El teléfono actúa únicamente como servidor HTTP local; no lanza el navegador PS4 ni ejecuta el exploit.
- Los enlaces externos y las actualizaciones remotas requieren Internet.
- La prueba de archivos de `WEBKITTY-LOCAL.html` no equivale a una prueba de exploit.
- El objetivo de la caché es permitir que el navegador PS4 recupere los recursos de la misma URL local sin servidor. Solo la prueba real con el hotspot apagado confirma que funciona.
