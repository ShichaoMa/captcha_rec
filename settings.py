# -*- coding:utf-8 -*-
import os
BASENAME = os.path.dirname(__file__)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 1024*1024*10))

LOG_BACKUPS = int(os.environ.get('LOG_BACKUPS', 5))

LOG_DIR = os.environ.get('LOG_DIR', os.path.join(BASENAME, "logs"))

LOG_STDOUT = eval(os.environ.get('LOG_STDOUT', "True"))

LOG_JSON = eval(os.environ.get('LOG_JSON', "False"))

# ---- captcha_monitor settings ----
CAPTCHA_RECOGNITION_HOST = os.environ.get('HOST', "0.0.0.0")

CAPTCHA_RECOGNITION_PORT = int(os.environ.get('PORT', 8887))
