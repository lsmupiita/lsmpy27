#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import dataBase, operaciones

import threading
import Queue as queue
def dosomething(oracion):
    return operaciones.traduccionAutomatica(oracion)
que = queue.Queue()
thr = threading.Thread(target = lambda q, arg : q.put(dosomething(arg)), args = (que, "El pastel tiene chocolate"))
thr.start()
thr.join()
while not que.empty():
    print(que.get())