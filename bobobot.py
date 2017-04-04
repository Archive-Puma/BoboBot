#! /usr/bin/env python
# -*- encoding: utf8 -*-
#This makes possible to run this program as a script invoking the interpreter

#########################
##     HEADER INFO     ##
#########################

__author__ = "Kike Puma"
__copyright__ = "Copyright 2007, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GNU-3.0"
__version__ = "1.0.0 Bobo is Alive!"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

########################
##       COLORS       ##
########################

#Color change: "\033[cod_formato;cod_texto;cod_fondom"
CERROR = "\n\033[1;31m" #BOLD RED
CGREEN = "\033[1;32m" #GREEN
CWHITE = "\033[1;37m" #WHITE
CRED = "\033[0;31m" #RED
CBLUE = "\033[1;34m" #BLUE
CDEFAULT = "\033[0m" #DEFAULT COLOR
CREDITS = "\033[2;37m" #LIGHT WHITE

########################
##     CHECK ROOT     ##
########################
import os
import sys

if not os.geteuid() == 0:
        sys.exit(CRED + "You need to have root privileges to run this program.\nPlease try again, this time using 'sudo'. Exiting." + CDEFAULT)

#######################
##       BANNER      ##
#######################

banner = ''' '''

#######################
##     ARGUMENTS     ##
#######################
import argparse

parser = argparse.ArgumentParser(version=__version__)
#Groups
config = parser.add_argument_group('Configuration')
#Arguments
parser.add_argument("-V", "--verbose", help="verbose mode", action="store_true")
config.add_argument("-c", "--config", help="Config file with all the tokens")
config.add_argument("-B", "--bot-token", help="Telegram Token: HTTP API. Allows Bobo to receive messages. Given by @BotFather")
config.add_argument("-id", "--user-id", help="Telegram Token: Chat ID. Allows Bobo to send messages. Given by @UserInfoBot")
config.add_argument("-virus","--virustotal-key", help="VirusTotal Token: API Key. Allows Bobo analyze URLs")
args = parser.parse_args()

#######################
##   CONFIGURATION   ##
#######################
import telepot    #Telegram API

INSERT_HERE_YOUR_USER_ID = '' #INSERT HERE YOUR USER ID
INSERT_HERE_YOUR_BOT_TOKEN = '' #INSERT HERE YOUR BOT TOKEN
INSERT_HERE_YOUR_VIRUSTOTAL_KEY = '' #INSERT HERE YOUR VIRUSTOTAL KEY

waitforit = ''

if args.bot_token:
    TOKEN = args.bot_token
else:
    TOKEN = INSERT_HERE_YOUR_BOT_TOKEN
if args.user_id:
    ID = args.user_id
else:
    ID = INSERT_HERE_YOUR_USER_ID
if args.virustotal_key:
    VT_KEY = args.virustotal_key
else:
    VT_KEY = INSERT_HERE_YOUR_VIRUSTOTAL_KEY

if args.config:
    try:
        txt = open(args.config,'r')
        for line in txt:
            try:
                name,key = line.split('::')
                if name == 'TELEGRAM.BOT.TOKEN':
                    TOKEN = key.strip()
                elif name == 'TELEGRAM.CHAT.ID':
                    ID = key.strip()
                elif name == 'VIRUSTOTAL.API.KEY':
                    VT_KEY = key.strip()
            except:
                pass
        txt.close()
    except IOError:
        print(CERROR + "[ERROR] No such file or directory: '" + args.config + "'" + CDEFAULT)
        sys.exit(0xDEAD)
         
        print(name,key.strip())
try:
    #Start BoboBot
    bot = telepot.Bot(TOKEN)
except:
    print(CERROR + "[ERROR] Invalid tokens. Killing Bobo..." + CDEFAULT)
    sys.exit(0xDEAD)

########################
##      FUNCTIONS     ##
########################
import time       #ProgramThreading
import requests   #Request HTTP

def VirusTotal(url):
    
    #Analize the URL
    headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent" : "gzip,  Bobo Bot is analizing this URL"
    }
    params = {'apikey': VT_KEY, 'resource':url}
    try:
        response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', 
                params=params, headers=headers).json()
    except:
        myresponse = "Me dicen que tu API Key de VirusTotal es inválida, mi amo. Seguro que es fallo de la página, tu no cometes errores"
        print(CRED + "[ERROR] VirusTotal API Key is invalid" + CDEFAULT)
        return myresponse

    #Analize the response
    if response['verbose_msg'] == 'Scan finished, scan information embedded in this object':
        if response['positives'] == 0:
            myresponse = "La URL no ha sido detectada como maliciosa por ningún antivirus, amo"
        else:
            myresponse = "La URL que me has enviado ha sido detectada como maliciosa por " + str(response['positives']) + " de " + str(response['total']) + " antivirus. Ten cuidado, amo"
    elif response['verbose_msg'] == 'Resource does not exist in the dataset':
        try:
            params = {'apikey': VT_KEY, 'url':url}
            response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params).json()
        except:
            myresponse = "Creo que he hecho algo mal, mi amo. Vuelva a intentarlo por favor"
            print(CRED + "[ERROR] Algo ha fallado al analizar la URL" + CDEFAULT)
            return myresponse
        myresponse = "La URL nunca ha sido analizada anteriormente por ninguno de esos no-humanos llamados 'Antivirus'. Tardaré un rato en analizarla. Por favor, espere y vuelva a preguntármelo en un rato"

    return myresponse

def Bobo(msg):
    
    ############
    # BOBOEYES #
    ############

    env_content, env_chat, env_id = telepot.glance(msg)
    if env_content == 'text':
        if args.verbose:
            print(CWHITE + "[+] User " + str(env_id) + " told me: " + CBLUE + "'" + msg['text'] + "'" + CDEFAULT)
    
    ############
    # BOBOHAND #
    ############
    
    msg = msg['text'].lower()

    # <-- RESPONSES --> #
    if 'hola' in msg:
        # Saludo #
        response = 'Hola, amo'
    elif '/analiza' in msg:
        # VIRUS TOTAL #
        try:
            command,url = msg.split(' ')
            print(CWHITE + "[-] Analizando " + url + " en VirusTotal" + CDEFAULT)
            response = VirusTotal(url)
        except ValueError:
            response = "Deberias probar a escribir '/analiza url.com'"
    else:
        return

    #Response
    try:
        bot.sendMessage(ID, response)
        if args.verbose:
            print(CWHITE + "[-] I have answered:" + CBLUE + "'" + response + "'" + CDEFAULT)
    except IOError:
        print(CERROR + "[ERROR] Bobo cannot talk, please check out your USER ID Token" + CDEFAULT)
        #system.exit(0xDEAD) <-- FIX THIS EXCEPTION, PLS -->

########################
##       PROGRAM      ##
########################

if len(sys.argv) == 1 and TOKEN == '':
    print(CERROR + "[ERROR] Insert the Tokens..." + CDEFAULT)
    sys.exit(0xDEAD)

try:
    #Read the new messages
    bot.message_loop(Bobo, run_forever=CGREEN + "\n[+] Bobo is listening..." + CDEFAULT)

    #Keep the program running
    #while True:
    #    time.sleep(10)

#Catch Ctrl+C
except KeyboardInterrupt:
    print(CERROR + "[ERROR] Keyboard Interrupt. You killed Bobo! ..." + CDEFAULT)
    sys.exit(0)
