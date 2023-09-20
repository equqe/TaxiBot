command = "gunicorn"
pythonpath = "/app/core"
bind = "0.0.0.0:8001"
workers = 1
# user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = "DJANGO_SETTINGS_MODULE=core.settings"
