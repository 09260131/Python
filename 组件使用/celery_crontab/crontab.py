from __future__ import absolute_import
from celery.schedules import crontab
from .celery import app


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'cproj.mwee_network_eye_task.pullDataService',
        'schedule': crontab(),
        'args': ()
    },
}
app.conf.timezone = 'Asia/Shanghai'


