#!/usr/bin/env python3
import requests
import argparse
import json
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

NEXMO_NUMBER = 'YOUR_NEXMO_NUMBER'
CONTACTS_FILE = os.path.dirname(os.path.abspath(__file__)) + '/contacts.json' #json file

def read_contacts():
    contacts = {}
    # read and append data
    with open(CONTACTS_FILE, "r") as json_file:
        for line in json_file:
            person = json.loads(line)
            contacts[person['contact']['number']] = person['contact']['alias']
        return contacts
        
known_names = read_contacts()
#print(known_names)

def choose_contact(name):
    for num, nam in known_names.items():
        if(name == nam):
            return num

def append_contact(number,alias):
    new_contact = {"contact":{"alias": alias.lower(), "number": number, }}
    # write back to file
    with open(CONTACTS_FILE, "a") as json_file:
        json_file.write("{}\n".format(json.dumps(new_contact)))

def send_msg(to,from_num,msg):
    payload = {
        'api_key': 'NEXMO_API_KEY',
        'api_secret': 'NEXMO_API_SECRET',
        'to': to,
        'from': from_num,
        'text': msg,
        }
    resp = requests.get('https://rest.nexmo.com/sms/json?', params=payload)
    return resp.text
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def num_in_contacts(s):
    try:
        test = known_names[s]
        return True
    except KeyError:
        return False

def name_in_contacts(s):
    for num, nam in known_names.items():
        if nam == s:
            return True # do not append

def sms(to,msg):
    resp = json.loads(send_msg(to,NEXMO_NUMBER,msg))
    #print(resp)
    if(resp['messages'][0]['status'] == '0'):
        print("Txt Msg sent to " + bcolors.OKGREEN + to + bcolors.ENDC + " successfully.")
    else:
        print(bcolors.WARNING + "Something went wrong, please try again and verify the number.")
        
def save(number):
    alias = input("Alias : ").lower()
    exists = name_in_contacts(alias)
    if(exists):
        print(bcolors.WARNING + "There is already a contact with the name " + alias + '.')
    else:
        append_contact(number,alias)
        print("You saved " + bcolors.OKGREEN + number + bcolors.ENDC + " to your contacts as " + bcolors.OKBLUE + alias + bcolors.ENDC + '.')

def main():
    parser = argparse.ArgumentParser(description='Send a txt msg from the console.')
    parser.add_argument('num', metavar='number', type=str, help='the number which you wish to send a text message to/save')
    parser.add_argument('--msg','-m', metavar='m', type=str, help='the message you wish to send')
    parser.add_argument('--save','-s', action='store_true', help='turn this flag on to save the number')
    args = parser.parse_args()
    
    try:
    
        if not(args.save): # regular message
            if not(is_number(args.num)): # not a number
                sms(choose_contact(args.num),args.msg)
            else: # regular number
                sms(args.num,args.msg)
                post_save = input("Save this number to your contacts? (y/n) : ")
                if(post_save is 'y'):
                    save(args.num)
                else:
                    exit()
        if(args.save): # save flag is active
            if not (args.msg):
                if(is_number(args.num)):
                    if not(num_in_contacts(args.num)):
                        save(args.num)
                    else:
                        print(bcolors.WARNING + "This person already exists in your contacts.")
            else:
                sms(args.num,args.msg)
                save(args.num)
    except KeyboardInterrupt:
        quit()

if __name__ == "__main__":main()
