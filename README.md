# JOSDANY92 · Ultimate Control Center v2.1

Centro de control local para PS4 y Android, con interfaz neón, navegación mediante mando/teclado y organización de archivos publicados por SimpleHttpServer.

## Estado real de las funciones
- **GoldHEN:** panel informativo; no ejecuta un exploit ni activa GoldHEN.
- **Smart Loader:** escaneo manual de archivos `.BIN` publicados por el servidor HTTP. No ejecuta ni inyecta payloads.
- **PKG / Homebrew:** permite revisar nombres y tamaños de archivos seleccionados; no instala ni ejecuta archivos.
- **FTP:** muestra información de la conexión HTTP local; no inicia un servidor FTP en PS4.

## Instalación
Consulta [LEEME.txt](LEEME.txt) antes de copiar los archivos a la carpeta compartida de SimpleHttpServer.

## Compatibilidad
La interfaz es una página web local. La compatibilidad de exploits, payloads y funciones de sistema depende de herramientas externas y debe verificarse por separado para el firmware exacto.


## Matriz de firmware (referencia)
- GoldHEN/henloader_lp describe Lapse para 9.00–12.02 y Poops para 9.00–13.00 en su repositorio.
- La release HenLoader LP 1.0 especifica Poops hasta 12.52 e incluye GoldHEN v2.4b18.7; para 13.00, el repositorio identifica Poops, pero la release 1.0 no lo lista como soporte empaquetado. Tratar 13.00 como perfil por verificar, no como compatibilidad garantizada.
- La publicación base GoldHEN v2.4b18 enumera 5.05, 6.71/6.72, 9.00, 9.60, 10.00/10.01, 10.50, 10.70/10.71 y 11.00. No confundir esa lista con builds integradas posteriores como v2.4b18.7.
- El selector es informativo y manual; no detecta firmware automáticamente ni ejecuta exploits/payloads.


## Detección automática de firmware — v2.2
El host lee la versión `PlayStation 4 x.xx` de `navigator.userAgent`, si el navegador la expone. Si no existe una coincidencia reconocible, muestra claramente que no pudo detectarla y ofrece una selección manual provisional. El valor detectado no se usa como prueba de compatibilidad de exploits ni payloads.


## Escudo de estabilidad — v2.3
- Añade una pantalla preventiva que muestra firmware detectado, estado de verificación y límites de la detección del modelo.
- La versión no ejecuta ni transmite payloads automáticamente.
- No se habilita una carga por coincidencia de nombre. La compatibilidad exige comprobar firmware, exploit, versión de GoldHEN y archivo exacto.
- El modelo PS4/PS4 Pro no se infiere del User-Agent; requiere confirmación manual.
- Kernel panic y pantallas negras no pueden eliminarse por completo desde una página web. La sección incluye precauciones y criterios de parada.
