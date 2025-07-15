
from typing import Dict
import os
from mailjet_rest import Client
from agents import Agent, function_tool
import datetime

import requests
# push over setup
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
# pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_token=os.getenv("PUSHOVER_TOKEN")
# mailjet setup
# api_key = os.getenv("MJ_APIKEY_PUBLIC")
# api_secret= os.getenv("MJ_APIKEY_SECRET")

# email destionation and sender
from_email = os.getenv("FROM_EMAIL")
to_email = os.getenv("TO_EMAIL")
def push(message):
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    # print(payload)
    response=requests.post(pushover_url, data=payload)
    print("pushover repsonse code",response)


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
# send html email via webjet
    message1=(f"startingn send_email from {from_email} {to_email}")
    push(message1)
    api_key = os.getenv("MJ_APIKEY_PUBLIC")
    api_secret= os.getenv("MJ_APIKEY_PRIVATE")
    mailjet = Client(auth=(api_key, api_secret))
    data = {
        "FromEmail": from_email,
        "FromName":"Deep REsearch agent",
        "Subject": subject,
        "Text-part": "Dear passenger, welcome to Mailjet! May the delivery force be with you!",
        "Html-part": html_body,
        "Recipients": [{"Email": to_email}]
         }
    message3=(f"api key {api_key} secret key ={api_secret}")
    push(message3)
    result = mailjet.send.create(data=data)
    print("mailjet status code ",result.status_code)
    #print(result.json())
    print(f"sent email status = {result.status_code} f= ({from_email} ,t = {to_email}")
    message2=(f"send_email sent s={result.status_code} {from_email} {to_email} ")
    # print(f"sent email status = {result.status_code}")
    push(message2)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
