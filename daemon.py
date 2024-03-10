#!/usr/bin/env python
# -*- coding: utf-8 -*-
from daemonize import Daemonize
from time import sleep
import requests
import pika
import json
from config import settings
 
pid = "/tmp/gokano_botd.pid"
 
#Delay time to retry
delay_time = 5.0
def queue_manager():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()   
    channel.queue_declare(queue='process_queue', durable=True)
    return channel
def main():
    qmanager = queue_manager()
    while True:
        try:
            response = requests.get(settings.URL)
            if response.status_code==201:
                data = response.json()
                
                for item in data:
                    qmanager.basic_publish(
                    exchange='',
                    routing_key='process_queue',
                    body=json.dumps(item),
                    properties=pika.BasicProperties(
                         delivery_mode = 2
                ))
                qmanager.close()
                sleep(delay_time)
            else:
                return {"erro":"Sem itens na fila"}
        except Exception:
            return "session"
main()