bind = "unix:/tmp/gunicorn.sock"
workers = 2
user = "mfa"
accesslog = "/home/mfa/logs/gunicorn-access.log"
errorlog = "/home/mfa/logs/gunicorn-error.log"