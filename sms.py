#!/usr/bin/env python
import requests
import argparse
import json

NEXMO_NUMBER = 'YOUR_NEXMO_NUMBER'

def send_msg(to,from_num,msg):
    payload = {
        'api_key': 'API_KEY',
        'api_secret': 'API_SECRET',
        'to': to,
        'from': from_num,
        'text': msg,
        }
    resp = requests.get('https://rest.nexmo.com/sms/json?', params=payload)
    return resp.text
    
def main():
    parser = argparse.ArgumentParser(description='Send a txt msg from the console.')
    parser.add_argument('to', metavar='t', type=str, help='the number which you wish to send a text message to')
    parser.add_argument('msg', metavar='m', type=str, help='the message you wish to send')
    args = parser.parse_args()
    
    resp = json.loads(send_msg(args.to, NEXMO_NUMBER ,args.msg))
    
    if(resp['messages'][0]['status'] == '0'):
        print("Txt Msg sent to " + args.to + " successfully.")
    
if __name__ == "__main__":main()
