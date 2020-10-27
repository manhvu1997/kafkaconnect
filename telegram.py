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
class Ticket():

    def __init__(self):
        # load ticket config from config file
        try:
            dir_path = path.dirname(path.abspath(__file__))
            filename = path.join(dir_path, "config.json")
            with open(filename, "r") as config_file:
                self.config = json.load(config_file)
                self.method = self.config["ticket"]['method']
                self.url = self.config["ticket"]["url"]
                self.interval = self.config["ticket"]["interval"]  # minutes
                self.payload = self.config["ticket"]["payload"]
        except Exception as e:
            logging.error("Ticket init: %s"%(e))
            raise e

    def get(self):
        # get ticket infor from Ticket API with FIXED time
        self.headers = {
            'content-type': "application/json"
        }
        try:
            response = requests.request(self.method, self.url, data=json.dumps(self.payload), headers=self.headers,
                                        verify=False)
            # return json unicode data
            if response.text:
                return response.text
            else:
                return None
        except Exception as e:
            logging.error("Ticket get: %s"%(e))
            raise e

    def request_data(self):
        # send a request to API with interval time
        # time format for request Ticket API date
        time_format = "%d/%m/%Y %H:%M:%S"
        interval = self.config["ticket"]["interval"]
        # convert system time to API time
        self.payload["FromDate"] = (datetime.datetime.now() - datetime.timedelta(minutes=int(interval))).strftime(
            time_format)
        self.payload["ToDate"] = datetime.datetime.now().strftime(time_format)
        try:
            # return data from API response
            return self.get()
        except Exception as e:
            logging.error("Ticket request_data %s: "%(e))
            raise e

    def ticket_status(self, from_date, to_date, code):
        # send a request to update ticket status
        time_format = "%d/%m/%Y %H:%M:%S" #datetime api format
        
        try:            
            self.payload["FromDate"] = datetime.datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S").strftime(time_format)
            self.payload["ToDate"] = datetime.datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S").strftime(time_format)
            data = json.loads(self.get())["Result"]["Data"]
            for idx, ticket in enumerate(data):
                if ticket["TicketCode"] == code:
                    return ticket["TicketStatus"]
                else:
                    pass
        except Exception as e:
            logging.error("Ticket ticket_status: %s"%(e))
            raise e
