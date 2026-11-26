> **Estado:** guía reservada para una fase posterior. No prepares Android todavía. Primero valida la activación de GoldHEN desde el repositorio en la PS4 física. Una vez confirmada, se actualizará esta guía con el paquete local definitivo.

# JOSDANY92 — servidor local Android (modo sin Internet)

Esta guía prepara una copia local del **sitio estático** para que un teléfono Android la publique por HTTP en la red local y la PS4 la abra desde su navegador. El teléfono solo sirve archivos: **no ejecuta el exploit**. El exploit, si se utiliza, se ejecuta en la PS4 y debe ser compatible con el firmware exacto.

## Preparación (cuando todavía hay Internet)

1. Abre la rama `JOSDANY92-V2.1` del repositorio y descarga el ZIP de esa rama:  
   https://github.com/raysotesta-boop/JOSDANY92-ONLINE/archive/refs/heads/JOSDANY92-V2.1.zip
2. En Android, extrae el ZIP en una carpeta permanente, por ejemplo `Almacenamiento interno/PS4/JOSDANY92/`.
3. Comprueba que en la carpeta raíz estén juntos `index.html`, `fondo-josdany92.jpg` y `josdany92-header.png`. Conserva también los demás archivos y carpetas del proyecto. No muevas solo el HTML: las imágenes y recursos relativos deben permanecer junto a él.
4. Instala/abre una aplicación de servidor HTTP estático para Android que pueda publicar una carpeta local (el proyecto anterior menciona SimpleHttpServer). Selecciona como raíz la carpeta `JOSDANY92` y configura el puerto que indique la aplicación, por ejemplo 8080. Autoriza el acceso a archivos.
5. Desactiva la optimización de batería para esa aplicación si Android la detiene en segundo plano. No borres ni muevas la carpeta después de configurarla.

## Uso sin Internet

1. Enciende el punto de acceso Wi‑Fi del teléfono.
2. Conecta la PS4 a ese punto de acceso. No hace falta que el teléfono tenga datos móviles ni salida a Internet.
3. Inicia el servidor HTTP en Android y confirma que indique una dirección IP y un puerto accesibles desde la red del hotspot.
4. En el navegador de PS4 escribe la dirección que muestre la aplicación, seguida de `/index.html`. Ejemplo ilustrativo: `http://192.168.43.1:8080/index.html`. **No asumas que esa IP es la tuya**: usa la dirección real mostrada por el servidor.
5. Si no abre, confirma que ambos dispositivos están en la misma red, que el servidor está activo, que la carpeta raíz es la correcta y que Android no bloqueó el acceso local. Prueba la dirección desde el navegador del propio teléfono conectado al hotspot.

## Qué queda disponible y qué no

- La interfaz, estilos, imágenes y archivos incluidos en la copia se sirven desde el teléfono sin consultar GitHub.
- Los enlaces externos, descargas no incluidas y cualquier actualización remota requieren Internet.
- La página actual es un centro de control/organizador. Sus paneles informativos y el escaneo de archivos publicados no equivalen a ejecutar un exploit, inyectar un payload ni activar GoldHEN.
- El navegador de PS4 solo puede acceder a los archivos que el servidor HTTP publique. Si el servidor no ofrece listado de directorios, el escaneo de carpetas puede no mostrar archivos aunque estén guardados en Android.
- No se incluyen exploits ni payloads de procedencia o compatibilidad no verificada. Antes de usar cualquier método, verifica firmware exacto, fuente, versión y hash del archivo. No hay garantía de evitar bloqueos, kernel panic o pantallas negras.

## Actualizar la copia del teléfono

Cuando haya Internet, descarga de nuevo el ZIP de la rama elegida, conserva una copia de seguridad de la carpeta local y reemplaza su contenido por la nueva versión completa. Después vuelve a iniciar el servidor. La copia del teléfono no se actualiza sola cuando cambia GitHub.

## Añadir WebKitty local para firmware 12.00

Si también quieres tener WebKitty en el mismo servidor Android:

1. Descarga el ZIP oficial completo: https://github.com/ArabPixel/WebKitty/archive/refs/heads/main.zip
2. Extrae la carpeta y renómbrala exactamente `WebKitty`.
3. Colócala dentro de la carpeta JOSDANY92, al mismo nivel que `index.html`. No reemplaces ni mezcles archivos de ambos proyectos.
4. Abre `WEBKITTY-LOCAL.html` desde el servidor Android y pulsa **COMPROBAR COPIA LOCAL**. Debe validar los recursos del manifiesto de 12.00 antes de continuar.
5. En la PS4 abre `/WebKitty/index.html` usando la misma IP y puerto del servidor. WebKitty inicia su propia preparación de caché si el navegador PS4 admite Application Cache.
6. Para probar el modo sin teléfono, sigue la sección «Prueba de caché sin el teléfono» de [WEBKITTY-INTEGRACION.md](WEBKITTY-INTEGRACION.md).

La carpeta WebKitty completa es necesaria: no basta con copiar `index.html`. El verificador solo comprueba archivos servidos por Android; la prueba final de caché debe hacerse en el navegador PS4 con el hotspot apagado.
