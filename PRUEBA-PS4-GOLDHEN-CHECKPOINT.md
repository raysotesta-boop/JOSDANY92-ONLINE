# Punto de control — prueba real de GoldHEN en PS4

Fecha de preparación: 2026-11-25  
Rama de trabajo: `JOSDANY92-V2.1`  
Consola objetivo documentada: PS4 Pro  
Perfil actualmente configurado: firmware 12.00 · GoldHEN 2.4b18.14 · Wobkot/Lapse (cadena 10)

## Estado verificado en GitHub
- La página `ACTIVACION-GOLDHEN.html` está en la rama de trabajo.
- El motor WebKitty está integrado y fijado a la revisión upstream `bb5b65b8b7935f91a61516f06dbddb9f07674cd6`.
- El flujo de GitHub Actions `Sync official WebKitty source into JOSDANY92` terminó con conclusión `success` en la ejecución `45747702637` (commit de ejecución `8f1438bf78660e8cfd1c9f33b194799a822a065f`).
- La verificación del workflow compara los blobs upstream con los recursos críticos incluidos en el repositorio.
- El parche de un solo intento desactiva el reintento automático para la sesión JOSDANY92.
- La página de preflight bloquea la activación si no detecta PS4 + firmware exactamente 12.00 o si falta algún recurso requerido.

## Límites conocidos
- El resultado exitoso de GitHub Actions valida la sincronización y comprobaciones de archivos; no prueba la ejecución en una consola.
- El marcador de éxito local significa que WebKitty reportó que terminó el callback de carga del payload. No demuestra por sí solo que el menú/overlay GoldHEN esté activo.
- No se puede garantizar 100 % de éxito ni eliminar completamente el riesgo de bloqueo, pantalla negra o kernel panic.
- La compatibilidad física de la combinación firmware + exploit + payload sigue pendiente de prueba.
- El firmware actual de la consola debe confirmarse antes de iniciar. Si no es exactamente 12.00, NO ejecutar este perfil: detenerse y revisar compatibilidad primero.
- No preparar APK/Android hasta superar la prueba en PS4.

## Lista para la prueba controlada
1. Confirmar en Ajustes de PS4 el firmware instalado. Registrar la versión exacta.
2. Confirmar que el host se sirve desde una URL real que entrega los archivos estáticos; una vista de archivo de GitHub no es un host ejecutable.
3. Abrir el host desde el navegador de la PS4.
4. Revisar que todas las comprobaciones de preflight aparezcan correctas y que el firmware detectado sea 12.00.
5. Si una sola comprobación falla, cancelar. No forzar el botón ni editar el firmware detectado.
6. Si todo coincide, realizar un solo intento controlado. Si hay bloqueo o pantalla negra, detenerse y no repetir intentos seguidos.
7. Verificar de forma independiente que GoldHEN aparece activo en la consola (por ejemplo, su menú/overlay y estado esperado), no solo el mensaje del navegador.
8. Registrar resultado, mensaje exacto, firmware, fecha y cualquier error antes de modificar el código.

## Criterio de aceptación
La prueba solo se considera satisfactoria cuando GoldHEN está visible y operativo en la PS4 después del flujo, y el resultado puede repetirse de forma estable sin asumirlo por el callback del navegador.
