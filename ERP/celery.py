import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'belogo_new.settings')

app = Celery('belogo_new')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update-cinema-week-status': {
        'task': 'web.tasks.update_cinema_week_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-week-status': {
        'task': 'web.tasks.update_week_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekcdsch-status': {
        'task': 'web.tasks.update_weekcdsch_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekber-status': {
        'task': 'web.tasks.update_weekber_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekf2-status': {
        'task': 'web.tasks.update_weekf2_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekf3-status': {
        'task': 'web.tasks.update_weekf3_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekf4-status': {
        'task': 'web.tasks.update_weekf4_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekb5-status': {
        'task': 'web.tasks.update_weekb5_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekcgbt-status': {
        'task': 'web.tasks.update_weekcgbt_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekbcj-status': {
        'task': 'web.tasks.update_weekbcj_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekbscd-status': {
        'task': 'web.tasks.update_weekbscd_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekyb-status': {
        'task': 'web.tasks.update_weekyb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekdb-status': {
        'task': 'web.tasks.update_weekdb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weeknmb-status': {
        'task': 'web.tasks.update_weeknmb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekcsb-status': {
        'task': 'web.tasks.update_weekcsb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekssb-status': {
        'task': 'web.tasks.update_weekssb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekfsb-status': {
        'task': 'web.tasks.update_weekfsb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekdbt-status': {
        'task': 'web.tasks.update_weekdbt_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weeknab-status': {
        'task': 'web.tasks.update_weeknab_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weekppb-status': {
        'task': 'web.tasks.update_weekppb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
    'update-weeknb-status': {
        'task': 'web.tasks.update_weeknb_status',
        'schedule': crontab(minute='*/10'),  # изменено на каждый час
    },
}