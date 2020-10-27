#!/usr/bin/python

import json

import requests
import telebot
from os import path
from requests.packages import urllib3
import logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

urllib3.disable_warnings()


class Telegram():

    # def __init__(self, url):
    #     self.url = url
    # def send(self, message):
    #     # send messages to Telegram bot (FTEL.SCC.syslog)
    #     try:
    #         url = "https://alerts.soc.fpt.net/webhooks/auto-pool/kgY9JnTVxfretKCEYGLNI32MB6Z7eiXa"

    #         payload = {'text': message, 'parse_mode': 'Markdown'}
    #         headers = {
    #             'Content-Type': 'application/json',
    #         }
    #         response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    #         return response.text
    #     except requests.exceptions.RequestException as error:
    #         return 0

    # def send(self, message):
    #     message = "New ticket"

    #     try:
    #         # load config file
    #         dir_path = path.dirname(path.abspath(__file__))
    #         filename = path.join(dir_path, "config.json")
    #         with open(filename, "r") as config_file:
    #             config = json.load(config_file)
    #             token = config["telegram"]["token"]
    #             contacts = config["telegram"]["contacts"]
    #         # call bot api with token
    #         bot = telebot.TeleBot(token)
    #         logging.info("Debug: %s"%(bot.get_me()))
    #         # send a message to each user in contact list
    #         for user in contacts:
    #             bt = bot.send_message(user, message)                
    #             logging.info("Send \"%s\" to %s successful"%(message, user))
    #             logging.debug(bot.get_updates())

    #     except Exception as error:
    #         logging.error(error)

    def send(self, message):
        try:
            # load config file
            dir_path = path.dirname(path.abspath(__file__))
            filename = path.join(dir_path, "config.json")
            with open(filename, "r") as config_file:
                config = json.load(config_file)
                token = config["telegram"]["token"]
                contacts = config["telegram"]["contacts"]

            url = "https://api.telegram.org/bot%s/sendMessage"%(token)    
                   
            payload = {
                "chat_id": contacts,
                "text": message,
                }
            
            headers = {
                'content-type': "application/json",
                }

            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

            logging.info(response.text)
        except Exception as e:
            logging.error("Telegram send: %s"%(e))
            raise e
