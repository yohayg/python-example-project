from __future__ import absolute_import

from celery import Celery

app = Celery('test_celery', broker='amqp://localhost:5672', backend='rpc://',
             include=['project.lib.celery_tasks'])
