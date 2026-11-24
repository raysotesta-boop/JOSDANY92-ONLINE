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
- Lapse: 9.00–12.02, según el proyecto GoldHEN/henloader_lp.
- Poops: 9.00–13.00, según el mismo proyecto.
- GoldHEN v2.4b18 oficial: su publicación lista 5.05, 6.71/6.72, 9.00, 9.60, 10.00/10.01, 10.50, 10.70/10.71 y 11.00.
- Para firmwares posteriores a 11.00, no asumir compatibilidad con ese BIN: verificar una build posterior concreta y sus instrucciones.
- El selector es informativo y manual; no detecta firmware automáticamente ni ejecuta exploits/payloads.
