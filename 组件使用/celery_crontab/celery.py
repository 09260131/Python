from __future__ import absolute_import
from celery import Celery
 
app = Celery('celery_crontab',
             broker='redis://localhost',
             backend='redis://localhost',
             include=['celery_crontab.tasks', 'celery_crontab.crontab', 'celery_crontab.mwee_network_eye_task'])
 
# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)
 
if __name__ == '__main__':
    app.start()
