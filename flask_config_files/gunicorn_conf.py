from os import environ

# Reference: https://github.com/melisource/fury_python-mini-runtime/tree/master?tab=readme-ov-file#applications-server

# http://docs.gunicorn.org/en/stable/settings.html#workers
# https://flask.palletsprojects.com/en/stable/deploying/gunicorn/#running
workers = int(environ["CPU_COUNT"]) * 2

# http://docs.gunicorn.org/en/stable/settings.html#threads
threads = 1

# http://docs.gunicorn.org/en/stable/settings.html#bind
bind = "0.0.0.0:8080"

# http://docs.gunicorn.org/en/stable/settings.html#worker-class
worker_class = "gthread"

# http://docs.gunicorn.org/en/stable/settings.html#worker-connections
worker_connections = 1001

# http://docs.gunicorn.org/en/stable/settings.html#timeout
timeout = 600

# https://docs.gunicorn.org/en/stable/settings.html#keepalive
keepalive = 3600
