import os
import multiprocessing

# _ROOT = os.path.abspath(os.path.join(
#     os.path.dirname(__file__), '..'))
# _VAR = os.path.join(_ROOT, 'var')
# _ETC = os.path.join(_ROOT, 'etc')

loglevel = 'info'
# errorlog = os.path.join(_VAR, 'log/api-error.log')
# accesslog = os.path.join(_VAR, 'log/api-access.log')
errorlog = "-"
accesslog = "-"

flask_host = os.getenv('FLASK_HOST', '127.0.0.1')
flask_port = os.getenv('FLASK_PORT', 8080)

# bind = 'unix:%s' % os.path.join(_VAR, 'run/gunicorn.sock')
bind = f'{flask_host}:{flask_port}'
#workers = 1
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True
