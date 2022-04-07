from celery import Celery
from celery.signals import worker_process_init, worker_init
import time
import random
import logging

logging.basicConfig(level="INFO")

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/0'

celery_app = Celery('Restaurant', broker=BROKER_URL, backend=BACKEND_URL)
celery_app.autodiscover_tasks()
celery_app.conf.task_routes = {'tasks.*': {'queue': 'kitchen'}}


def restaurant_logo():
    moto = """

 (                                                
 )\ )              (      )          )            
(()/( (   (        )\  ( /((      ( /(   (        
 /(_)))(  )\ )   (((_) )\())\  (  )\()) ))\ (     
(_))_(()\(()/(   )\___((_)((_) )\((_)\ /((_))\ )  
| |_  ((_))(_)) ((/ __| |(_(_)((_| |(_(_)) _(_/(  
| __|| '_| || |  | (__| ' \| / _|| / // -_| ' \)) 
|_|  |_|  \_, |   \___|_||_|_\__||_\_\\___|_||_|  
          |__/                                    

# Welcome to Tasks Queue
"""
    logging.warning(moto)

@worker_process_init.connect
def orders_init(sender=None, headers=None, body=None,exception=None,  **kwargs):
    restaurant_logo()

@celery_app.task
def cooking_task(table_no, dishes, milestone):
    logging.info(f"------------------[ {milestone}.{table_no} ]------------------")
    logging.info(f"👉 Starting cooking")
    time.sleep(1)
    for dish in dishes:
        logging.info(f"Cooking : ✅ {dish}")
    logging.info(f"👍 Finished cooking")
    logging.info(f"------------------[ {milestone}.{table_no} ]------------------")

@celery_app.task
def orders(milestone=1):
    logging.warning(f"== MILESTONE NO: #{milestone}")
    table_dishes1 = ["Chicken", "Sandwish", "Lemon"]
    resutl1 = cooking_task.delay(1, table_dishes1, milestone)
    logging.info(resutl1)

    table_dishes2 = ["Sandwish", "Chicken", "Water"]
    resutl2 = cooking_task.delay(2, table_dishes2, milestone)
    logging.info(resutl2)

    table_dishes3 = ["Sandwish", "Cola"]
    resutl3 = cooking_task.delay(3, table_dishes3, milestone)
    logging.info(resutl3)

    table_dishes4 = ["Chicken Manchurian", "Chicken Noodles", "Cola"]
    resutl4 = cooking_task.delay(4, table_dishes4, milestone)
    logging.info(resutl4)

def test(shuffle=True):
    """
    Call this function to check the Queue results
    """
    l = list(range(1, 4))
    if shuffle:
        random.shuffle(l)
    logging.info(f"MILESTONES: {l}")
    [orders.delay(i) for i in l]