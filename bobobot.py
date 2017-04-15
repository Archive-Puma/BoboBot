#! /usr/bin/env python
# -*- encoding: utf8 -*-
#This makes possible to run this program as a script invoking the interpreter

#Python Modules: os, sys, argparse, telepot, time
#BoboBot Modules: crawler, analyzer
#Modules of Modules: requests

#########################
##     HEADER INFO     ##
#########################

__author__ = "Kike Puma"
__copyright__ = "Copyright 2007, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GNU-3.0"
__version__ = "1.4 Bobo Poliglota"
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
otheropt = parser.add_argument_group('More options')
#Arguments
parser.add_argument("-V", "--verbose", help="verbose mode", action="store_true")
config.add_argument("-c", "--config", help="Config file with all the tokens")
config.add_argument("-B", "--bot-token", help="Telegram Token: HTTP API. Allows Bobo to receive messages. Given by @BotFather")
config.add_argument("-id", "--user-id", help="Telegram Token: Chat ID. Allows Bobo to send messages. Given by @UserInfoBot")
config.add_argument("-virus","--virustotal-key", help="VirusTotal Token: API Key. Allows Bobo analyze URLs")
otheropt.add_argument("-l","--lang", choices=('esES',), default='esES', help="Change Bobo language. Options: { esES }")
otheropt.add_argument("-L","--load-lang", help="Load a translate file")
args = parser.parse_args()

########################
##      LANGUAGE      ##
########################

esES = {
        'error_creds':'Inserta los Tokens...',
        'error_encoder':'El archivo tiene caracteres no admitidos',
        'error_lang':'El archivo de idioma contiene errores',
        'error_unknown':'Algo ha ido mal, mi amo',
        'error_scripts':'No es posible cargar los Scripts de Bobo',
        'error_keyboard':'Interrupción de teclado. ¡Has matado a Bobo!',
        'error_tokens':'Tokens inválidos. Ahora habrá que matar a Bobo...',
        'error_userID':'Bobo no es capaz de hablar. Por favor, revisa tu ID de Usuario',
        'Qhi':'Hola',
        'Rhi':'¡Hola!',
        'name':'amo',
        'init':'Bobo esta escuchando...',
        'confused': 'No sé muy bien qué responder,',
        'should_analyze': 'Deberias probar a escribir \'/analyze url.com\'',
        'should_crawl':'Deberias probar a escribir \'/crawl url.com\'',
        'analyzing_1':'Analizando ', 'analyzing_2':' en VirusTotal',
        'dialog_1':'El usuario', 'dialog_2':'me ha dicho:',
        'dialog_r':'Yo le he contestado: ',
        }

if args.load_lang:
        loadLang = dict()
        try:           
                langf = open(args.load_lang,'r')
                for line in langf:
                        line = line.encode('utf-8').strip()
                        if len(line) == 0 or line[0] == '#':
                                continue
                        tag , phrase = line.split('::')
                        loadLang[tag] = phrase
                langf.close()
                lang = loadLang
        except UnicodeDecodeError:
                lang = esES
                print(CERROR + '[ERROR ' + lang['error_encoder'] + CDEFAULT)
        except IOError:
                lang = esES
                print(CERROR + '[ERROR] ' + lang['error_lang'] + CDEFAULT)
elif args.lang:
    if args.lang == 'esES':
        lang = esES
else:
    lang = esES

#######################
##   CONFIGURATION   ##
#######################
import telepot    #Telegram API

INSERT_HERE_YOUR_USER_ID = '' #INSERT HERE YOUR USER ID
INSERT_HERE_YOUR_BOT_TOKEN = '' #INSERT HERE YOUR BOT TOKEN
INSERT_HERE_YOUR_VIRUSTOTAL_KEY = '' #INSERT HERE YOUR VIRUSTOTAL KEY

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
        print(CERROR + '[ERROR] ' + ' \'' + args.config + '\'' + CDEFAULT)
        sys.exit(0xDEAD)

        print(name,key.strip())
try:
    #Start BoboBot
    bot = telepot.Bot(TOKEN)
except:
    print(CERROR + '[ERROR] ' + lang['error_tokens'] + CDEFAULT)
    sys.exit(0xDEAD)

########################
##      FUNCTIONS     ##
########################
import time       #ProgramThreading

try:
    #Añadimos la ruta de los modulos de Bob
    sys.path.append('scripts\\' if os.name == 'nt' else 'scripts/')
    #Import SCRPTS
    import bcrawler
    import banalyzer
except:
    print(CERROR + '[ERROR] ' + lang['error_scripts'] + CDEFAULT)

def Bobo(msg):

    ############
    # BOBOEYES #
    ############

    env_content, env_chat, env_id = telepot.glance(msg)
    if env_content == 'text':
        if args.verbose:
            print(CWHITE + '[+] ' + lang['dialog_1'] + ' ' + str(env_id) + ' ' + lang['dialog_2'] + ' ' + CBLUE + "'" + msg['text'] + "'" + CDEFAULT)

    else:
        return


    ############
    # BOBOHAND #
    ############

    msg = msg['text'].lower()
    response = lang['confused'] + ' ' + lang['name']

    # <-- COMMANDS -->#
    if msg[0] == '/':
        command , data = msg.split(' ', 1)
        if '/analiza' in command or '/analyze' in command:
            # VIRUS TOTAL #
            try:
                if args.verbose:
                    print(CWHITE + '[-] ' + lang['analyzing_1'] + ' ' + data + ' ' + lang['analyzing_2'] + CDEFAULT)
                response = banalyzer.Analyze(VT_KEY, data)
            except ValueError:
                response = lang['should_analyze']
        elif '/comprueba' in command or '/comprobar' or '/crawl' in command:
            # CRAWLER #
            try:
                response = bcrawler.BoboResponse(bcrawler.Crawl(data))
            except ValueError:
                response = lang['should_crawl']
            except:
                pass #HAND EXCEPTIONS
        else:
            response = lang['error_unknown']
            return

    # <-- RESPONSES --> #
    else:
        if lang['Qhi'].lower() in msg:
            # Saludo #
            response = lang['Rhi']

    #Response
    try:
        bot.sendMessage(ID, response)
        if args.verbose:
            print(CWHITE + '[-] ' + lang['dialog_r'] + CBLUE + '\'' + response + '\'' + CDEFAULT)
    except IOError:
        print(CERROR + '[ERROR] ' + lang['error_userID'] + CDEFAULT)
        #system.exit(0xDEAD) <-- FIX THIS EXCEPTION, PLS -->

########################
##       PROGRAM      ##
########################

if len(sys.argv) == 1 and TOKEN == '':
    print(CERROR + '[ERROR] ' + lang['error_creds'] + CDEFAULT)
    sys.exit(0xDEAD)

try:
    #Read the new messages
    bot.message_loop(Bobo, run_forever=CGREEN + '\n[+] ' + lang['init'] + CDEFAULT)

#Catch Ctrl+C
except KeyboardInterrupt:
    print(CERROR + '[ERROR] ' + lang['error_keyboard'] + CDEFAULT)
    sys.exit(0)
