# -*- coding: utf-8 -*-
import time
from .celery import app


@app.task
def add(x, y):
    time.sleep(10)
    print(time.time())
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers) 
