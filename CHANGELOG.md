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


## v2.4 — Verificación local de archivos
- Nuevo panel Verificación en el menú principal.
- Selección local de archivos BIN y cálculo SHA-256 mediante Web Crypto cuando está disponible.
- Se declara explícitamente que un hash calculado no acredita origen ni compatibilidad.
- Sin manifiesto confiable, todos los BIN permanecen NO VERIFICADOS.
- Si Web Crypto no está disponible, el panel informa la limitación sin dar una falsa validación.
- Sin transmisión, carga o ejecución de archivos.


## v2.5 — Matriz documental de compatibilidad
- Se añadió el panel Compatibilidad al menú y a la navegación por mando.
- Se separan explícitamente los rangos descritos por el repositorio HenLoader LP y los de la release LP 1.0.
- Se distingue el listado de firmware del lanzamiento base GoldHEN v2.4b18 del GoldHEN integrado en HenLoader LP 1.0.
- Se documenta el perfil 12.00 del usuario sin declarar validada su build 2.4b18.14.
- Sin activación, transmisión, ejecución ni reintentos automáticos.


## v2.6 — Vista WebKit de activación
- Nuevo panel visual WebKit con selección manual GoldHEN/PS4HEN.
- Añadido registro de estado y botón Continuar con respuesta honesta de motor no integrado.
- No se simula el éxito, no se ejecuta exploit y no se envían payloads.


## v2.7 — Tipografía grande para TV
- Aumentados los tamaños de letras en menú lateral, tarjetas principales, accesos rápidos, encabezados y paneles.
- Mejorado el interlineado para facilitar la lectura en televisión.
- Sin cambios en el motor de activación: continúa siendo una vista visual sin exploit integrado.


## v2.8 — Cuadro de firmware +20%
- Ampliado un 20% el cuadro «Firmware detectado» de la pantalla principal.


## v2.9 — Ajuste de encaje para TV
- Conservado el cuadro de firmware al 120%.
- Ajustada tipografía y distribución de tarjetas y navegación para reducir solapamientos y recortes.
- Ocultados pictogramas de tarjetas que se muestran como caracteres no compatibles en WebKit PS4.
