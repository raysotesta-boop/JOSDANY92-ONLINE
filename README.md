# JOSDANY92 · Ultimate Control Center v3.0

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


## v2.4 — verificación local SHA-256
- Se añadió una sección para seleccionar un archivo `.BIN` local y calcular su huella SHA-256 cuando Web Crypto esté disponible.
- La huella calculada no demuestra procedencia, integridad frente a una fuente confiable ni compatibilidad.
- No existe aún un manifiesto de hashes oficiales validado; por ello todos los archivos permanecen como NO VERIFICADOS.
- Si el navegador o el contexto HTTP no permite `crypto.subtle`, la comprobación se declara no disponible y no se simula un resultado.
- La función no transmite, carga ni ejecuta el archivo.


## v2.5 — matriz documental de compatibilidad

### Fuentes y límites
- El repositorio oficial GoldHEN/henloader_lp describe Lapse 9.00–12.02 y Poops 9.00–13.00; su README se declara WIP.
- La release HenLoader LP 1.0 especifica Lapse 9.00–12.02 + Poops 9.00–12.52 e incluye GoldHEN v2.4b18.7.
- El lanzamiento base GoldHEN v2.4b18 enumera 5.05, 6.71/6.72, 9.00, 9.60, 10.00/10.01, 10.50, 10.70/10.71 y 11.00. No se usa esa lista para certificar builds posteriores.
- Perfil del usuario: PS4 Pro, firmware 12.00, GoldHEN 2.4b18.14. El exploit HenLoader LP 1.0 declara un rango que incluye 12.00, pero no se ha probado en su consola. El binario exacto 2.4b18.14, su procedencia y su hash siguen pendientes.
- La combinación firmware + exploit + payload no está certificada. No se habilita carga ni ejecución desde el host.


## v2.6 — Vista WebKit de activación
- Se incorporó un flujo visual de dos columnas inspirado en las pantallas compartidas por el usuario: selección GoldHEN/PS4HEN, firmware visible y registro de estado.
- El botón Continuar solo muestra el estado de preparación y el bloqueo de seguridad; no ejecuta ni simula el jailbreak.
- El motor real del exploit/loader de referencia no está integrado. Mantener el host que ya funciona como método principal hasta una integración verificada.


## v2.7 — tipografía grande para TV
- Aumentados los tamaños de menú, tarjetas, accesos rápidos, botones, paneles y registros para mejorar la lectura desde el sofá en el navegador PS4.
- Se mantienen los ajustes responsive y el flujo de activación en modo visual; no se incorpora ejecución de exploits ni payloads.


## v2.8 — cuadro de firmware +20%
- El cuadro «Firmware detectado» de la pantalla principal se amplió un 20% manteniendo su alineación a la derecha.


## v2.9 — ajuste de encaje para TV
- Se conserva el cuadro Firmware detectado al 120% de su tamaño base.
- Se ajustan los tamaños de navegación, tarjetas y accesos rápidos para evitar texto cortado y etiquetas partidas en la pantalla de PS4.
- Se ocultan iconos de tarjetas que el navegador PS4 representa como cuadrados, priorizando títulos legibles.


## v3.0 — firmware y navegación
- El cuadro «Firmware detectado» aumenta otro 20% respecto a v2.9 (escala acumulada 1.44 respecto al tamaño base).
- El texto del título y del valor de firmware aumenta 20% respecto a v2.9 para que «PS4 12.00» se lea mejor.
- Se ajusta solo la etiqueta «Compatibilidad» del menú para que quepa en una línea dentro de la barra lateral.
