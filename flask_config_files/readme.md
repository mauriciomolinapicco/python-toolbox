Servidor de Aplicaciones (Gunicorn)

Archivo de configuración (p. ej. gunicorn.conf.py):

¿Qué hace cada parámetro?

workers = CPU_COUNT * 2
Cantidad de procesos. Regla de pulgar típica para buen throughput.
Concurrencia total ≈ workers × threads.

threads = 1
Hilos por proceso (aplica porque usamos gthread).

I/O–bound (red, BQ, S3): subí a 4–8 para mejorar concurrencia.

CPU–bound: dejá en 1 (el GIL limita).

- bind = "0.0.0.0:8080"
Dirección/puerto de escucha (común en contenedores).

- worker_class = "gthread"
Workers con threads (buenos para I/O). Alternativas: sync, gevent, etc.

- worker_connections = 1001
No aplica con gthread (sirve para workers async como gevent). Se puede omitir.

- timeout = 180
Máximo por request antes de que Gunicorn mate el worker (WORKER TIMEOUT).
Si tenés endpoints >180s, aumentá (ej. 600).
Si devolvés 202 y vas a background, este timeout no debería impactar.

- keepalive = 3600
Mantiene conexiones HTTP inactivas abiertas
