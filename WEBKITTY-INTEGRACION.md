# Integración externa de WebKitty en JOSDANY92

## Qué se añadió

La rama JOSDANY92-V2.1 incorpora un acceso **WEBKITTY** en los accesos rápidos. El panel permite:

- Elegir apertura manual o automática.
- Configurar un retardo de 0 a 90 segundos, segundo a segundo.
- Guardar modo y tiempo en el almacenamiento local del navegador.
- Cancelar la cuenta atrás antes de abrir el host.
- Abrir el host oficial o descargar el ZIP completo del repositorio.

**Límite importante:** el temporizador solo abre la página oficial de WebKitty. No dispara el exploit ni activa GoldHEN desde JOSDANY92. El motor de WebKitty sigue siendo un proyecto independiente.

## Enlaces oficiales

- Host: http://webkitty.arabpixel.net/
- Repositorio y código fuente: https://github.com/ArabPixel/WebKitty
- ZIP de la rama principal: https://github.com/ArabPixel/WebKitty/archive/refs/heads/main.zip

## Instalar WebKitty en Android para servirlo localmente

1. Mientras tengas Internet, descarga el ZIP oficial desde el enlace anterior.
2. Extrae el ZIP completo dentro de la carpeta raíz que publica SimpleHttpServer, con el nombre exacto `WebKitty`. La estructura debe quedar así:
   - `Servidor PS4/JOSDANY92/index.html`
   - `Servidor PS4/JOSDANY92/WEBKITTY-LOCAL.html`
   - `Servidor PS4/JOSDANY92/WebKitty/index.html`
   - `Servidor PS4/JOSDANY92/WebKitty/exploit.html`
   - `Servidor PS4/JOSDANY92/WebKitty/includes/`
   - `Servidor PS4/JOSDANY92/WebKitty/src/`
3. En Android, abre `WEBKITTY-LOCAL.html` desde el servidor local. Pulsa **COMPROBAR COPIA LOCAL**. El verificador lee el manifiesto 14.02 y comprueba que cada archivo requerido responda desde el servidor. Corrige los archivos faltantes antes de conectar la PS4.

## Instalar WebKitty en Android para servirlo localmente (continuación)

1. Mientras tengas Internet, descarga el ZIP oficial desde el enlace anterior.
2. Extrae el ZIP completo en una carpeta permanente, por ejemplo `Almacenamiento interno/PS4/WebKitty/`.
3. No separes `index.html`, `cache.html`, `exploit.html`, `includes/`, `src/` ni los demás recursos. Debe conservarse toda la estructura del proyecto.
4. En SimpleHttpServer (u otro servidor HTTP estático), selecciona la carpeta `WebKitty` como raíz y arranca el servidor.
5. Conecta la PS4 al hotspot del teléfono y abre la URL local del servidor seguida de `/index.html`.
6. Para preparar la caché, abre desde ese mismo origen local `/cache.html` en el navegador PS4 y espera a que el proceso indique que terminó. No cierres la página mientras esté descargando recursos.

## Prueba offline

Después de que el sistema de caché indique que terminó:

1. Cierra el navegador PS4 normalmente.
2. Apaga el hotspot y desconecta el teléfono.
3. Abre de nuevo el navegador PS4 y comprueba si recupera el host.
4. Comprueba también que la selección de firmware y la pantalla principal se cargan sin recursos externos.

El repositorio WebKitty utiliza el mecanismo legado `window.applicationCache` para la caché basada en manifiestos. Su propio código contempla el caso en que el navegador no admita `applicationCache` y muestra un error. Por tanto, no se debe asumir que la caché quedó instalada solo porque se abrió `cache.html`: hay que completar la descarga y realizar la prueba real sin red.

## Firmware 14.02

El README y la tabla de cadenas del repositorio oficial incluyen Slopkit / Afterglow para 14.00–14.02. Esto describe la compatibilidad publicada por WebKitty; no constituye una garantía de éxito o estabilidad en una consola concreta. El desarrollador del exploit y los mantenedores del host deben recibir el crédito correspondiente. Haz una copia de seguridad de datos importantes y no repitas intentos si aparecen bloqueos o pantallas negras.

## Licencia y atribución

WebKitty está publicado bajo **AGPL-3.0-or-later**. Esta integración de JOSDANY92 enlaza el proyecto externo y no copia ni modifica su código fuente. Si en el futuro se incorpora, modifica o redistribuye código de WebKitty dentro de JOSDANY92, habrá que cumplir la AGPL-3.0-or-later, conservar los avisos y ofrecer el código fuente correspondiente.


## Verificación desde el teléfono

JOSDANY92 incluye `WEBKITTY-LOCAL.html`. Ábrelo desde el servidor Android y pulsa **COMPROBAR COPIA LOCAL**. Comprueba los recursos del manifiesto de firmware 14.02 y muestra los que faltan. Es una comprobación HTTP de archivos, no prueba la caché interna de PS4.

## Prueba de caché sin el teléfono

La caché Application Cache de WebKitty se asocia al origen exacto (protocolo, IP y puerto). Después de preparar la caché en PS4:

1. Cierra el navegador PS4 normalmente.
2. Apaga el hotspot y el servidor del teléfono.
3. Desde el historial del navegador PS4, vuelve a abrir exactamente la misma URL local, con la misma IP, puerto y ruta.
4. Solo si WebKitty carga sin el teléfono se puede considerar que la caché offline funciona en esa consola.

No se puede prometer que la caché persista sin probarlo en el navegador concreto. WebKitty comprueba `window.applicationCache` y emite error si esa API no está disponible. El verificador Android no puede probar la caché de PS4 por ti.
