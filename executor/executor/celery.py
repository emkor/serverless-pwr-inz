from __future__ import absolute_import, unicode_literals
from celery import Celery

from commons.logs import setup_logger

app = Celery('executor', include=['executor.tasks'])
app.config_from_object('executor.config')

if __name__ == '__main__':
    setup_logger()
    app.start()
