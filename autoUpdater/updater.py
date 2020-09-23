from .updateApi import UpdateApi
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(UpdateApi().clearRemnant, 'interval', hours=24, start_date='2020-09-23 00:00:00')
    scheduler.start()