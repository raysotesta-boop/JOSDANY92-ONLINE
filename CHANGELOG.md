# Cambios — JOSDANY92 v2.1

- Se actualizó la identificación de versión en la interfaz.
- Smart Loader dejó de escanear automáticamente al abrirse: ahora requiere pulsar el botón de búsqueda.
- Se aclaró el estado real de GoldHEN y los límites de PKG, ELF, BIN y FTP.
- Se conservó la rama main sin cambios.


## v2.1.1 — perfiles de firmware
- Se añadió una sección Firmware al menú lateral.
- Selector manual de versiones desde 9.00 hasta 13.00, limitado a perfiles documentados.
- Se distinguen las rutas Lapse/Poops de la compatibilidad del payload GoldHEN.
- Se advierte que GoldHEN v2.4b18 oficial lista soporte hasta 11.00; las builds posteriores deben verificarse por separado.
- No se añadió ejecución automática ni se declara una carga exitosa.

- Aclarada la diferencia entre el rango del repositorio henloader_lp, la release LP 1.0 (Poops hasta 12.52) y la lista de firmware de GoldHEN v2.4b18 base.


## v2.2 — detección automática de firmware
- Se añadió lectura del patrón de versión PS4 desde navigator.userAgent.
- El encabezado muestra la versión cuando el navegador la expone.
- El panel Firmware presenta la detección y ofrece una comprobación manual; si no hay coincidencia, declara el dato como no disponible.
- La detección no se usa para afirmar compatibilidad ni activar exploits/payloads.


## v2.3 — Escudo de estabilidad
- Se añadió una sección de comprobaciones preventivas.
- Se documenta que el modelo PS4/PS4 Pro no puede deducirse con fiabilidad del User-Agent.
- Se explicitan los bloqueos preventivos: no hay ejecución automática de BIN y no se afirma compatibilidad sin verificar.
- Se añadieron criterios de parada tras pantalla negra/congelación y advertencias sobre kernel panic.
