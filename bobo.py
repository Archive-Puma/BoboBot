#! /usr/bin/env python
# -*- encoding: utf8 -*-
#This makes possible to run this program as a script invoking the interpreter

#=============================================#
# --------------- Header Info --------------- #
#=============================================#

__author__ = "Kike Puma"
__copyright__ = "Copyright 2017, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GNU-3.0"
__version__ = "2.2 BoboJoker"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

#=============================================#
# ----------------- Modules ----------------- #
#=============================================#

try:
    import os, platform, sys
except ImportError:
    sys.exit(color.ERROR + "[ERROR] Basic Python Modules are corrupted or not installed" + color.END)

# R E Q U I R E M E N T S
try:
    import argparse    #ArgumentParse
except ImportError:
    sys.exit(color.ERROR + "[ERROR] ArgParse module is not installed" + \
    color.BLUE + "\n[INFO] Please, install it using 'sudo pip install -r requirements.txt'" + color.END)

try:
    import telepot    #Telegram API
    from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton #Keyboard and Buttons in Telegram
except ImportError:
    sys.exit(color.ERROR + "[ERROR] Telepot module is not installed" + \
    color.BLUE + "\n[INFO] Please, install it using 'sudo pip install -r requirements.txt'" + color.END)

# B O B O   M O D U L E S

from core.modules.bjoker import joke

#=============================================#
# ----------------- Colors ------------------ #
#=============================================#

class color:
    #Color change: "\033[cod_formato;cod_texto;cod_fondom"
    BLUE = "\033[1;34m" #BLUE
    END = "\033[0m" #DEFAULT COLOR
    ERROR = "\033[1;31m" #BOLD RED
    GREEN = "\033[1;32m" #GREEN
    PURPLE = "\033[1;35m" #PURPLE
    RED = "\033[0;31m" #RED
    WHITE = "\033[1;37m" #WHITE
    YELLOW = "\033[1;33m" #YELLOW
    CREDITS = "\033[2;37m" #LIGHT WHITE

#=============================================#
# -------------- Check System --------------- #
#=============================================#

if not platform.system() == 'Linux':
    sys.exit(color.ERROR + "[ERROR] You are not using a Linux Based OS!" + \
    color.BLUE + "\n[INFO] Linux is a must-have for this script!" + color.END)

#=============================================#
# --------------- Check Root ---------------- #
#=============================================#

if not os.geteuid() == 0:
    sys.exit(color.ERROR + "[ERROR] You need to have root privileges to run this program." + \
    color.BLUE + "\n[INFO] Please try again, this time using 'sudo' or being 'root'. Exiting." + color.END)

#=============================================#
# ---------------- Arguments ---------------- #
#=============================================#

parser = argparse.ArgumentParser(version=__version__)
services = parser.add_argument_group('Services')
config = parser.add_argument_group('Configuration')
otheropt = parser.add_argument_group('More options')
#Arguments
config.add_argument("-c","--config", type=str, default="bobo.cfg", help="Config file with all the tokens")
otheropt.add_argument("-V", "--verbose", help="Verbose mode", default=False, action="store_true")

args = parser.parse_args()

#=============================================#
# -------------- Configuration -------------- #
#=============================================#

bot = telepot.Bot('xxx')

# T O K E N S
token = {}

tokens_available = {
    'TOKEN.TELEGRAM.BOTMASTER':'botmaster',
    'TOKEN.TELEGRAM.USERID':'chatID',
}

if args.config: #Load tokens from config file
    try:
        config_file = open(args.config, 'r')
        for line in config_file:
            try:
                name, key = line.split('::')
                token[tokens_available.get(name)] = key.rstrip()
            except KeyboardInterrupt:
                pass
        config_file.close()
    except KeyboardInterrupt:
        sys.exit(color.ERROR + "[ERROR] Config file has errors" + color.END)

# C H E C K   T O K E N S
if not ('botmaster' in token and 'chatID' in token):
    sys.exit(color.ERROR + "[ERROR] Config file has errors" + color.END)

#=============================================#
# ---------------- Functions ---------------- #
#=============================================#

def log(text):       #Verbose print
    if args.verbose:
        print(text)

def bye(text):       #Error verbosed
    log(text)
    sys.exit(0xDEAD)

# B O T   F U N C T I O N S
def response(text):     #Bobo talks!
    bot.sendMessage(token['chatID'],text)
    log(color.YELLOW + "[BBB] Bobo the Bot response " + color.WHITE + text)

def understand(text):   #Parse conversations
    text = text.lower()
    #Commands
    if text[0] == '/':
        if '/joke' == text.split(" ",1)[0]:
            response(joke())
    #Conversation
    else:
        if 'joke' in text:
            response(joke())

def handle(msg):        #Manage Telegram Messages
    content_type, chat_type, chat_id = telepot.glance(msg)
    #Text Messages
    if content_type == 'text':
        log(color.YELLOW + "[MSG] " + msg['from']['first_name'] + \
            " (@" + msg['from']['username'] + ") said " + \
            color.WHITE + msg['text'] + color.END)
        understand(msg['text'])

# M A I N   F U N C T I O N
def main():
    log(color.BLUE + "[INFO] Verbose mode is ON" + color.END) #Verbose mode
    #Create the bot
    global bot
    bot = telepot.Bot(token['botmaster'])
    log(color.GREEN + "[INFO] Bobo! Wake up!" + color.END)
    try:
        #Start the bot
        bot.message_loop(handle,run_forever=color.GREEN + "[INFO] Bobo is awake!" + \
            color.BLUE + "\n[INFO] You will find it at " + color.WHITE + \
            "https://web.telegram.org/#/im?p=@" + bot.getMe()['username'] + color.END)
    except telepot.exception.UnauthorizedError:
        bye(color.RED + "[ERROR] BotMaster token is wrong. Bobo is still asleep...")

#=============================================#
# ------------------ Main ------------------- #
#=============================================#

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        bye(color.BLUE + "\n[INFO] KeyboardInterrupt detected. You killed Bobo :(" + color.END)

#=============================================#
# ------------------ ToDo's ----------------- #
#=============================================#

# --------------- Port Scanner -------------- #
