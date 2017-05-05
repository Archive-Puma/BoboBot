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
__version__ = "2.0 RoboBobo"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

#=============================================#
# ----------------- Modules ----------------- #
#=============================================#

try:
    import argparse, os, platform, sys
except ImportError:
    sys.exit(color.ERROR + "[ERROR] Basic Python Modules are corrupted or not installed" + color.END)

# R E Q U I R E M E N T S
try:
    import telepot    #Telegram API
except ImportError:
    sys.exit(color.ERROR + "[ERROR] Telepot module is not installed" + \
    color.BLUE + "\n[INFO] Please, install it using 'sudo pip install -r requirements'" + color.END)

#=============================================#
# ----------------- Colors ------------------ #
#=============================================#

class color:
    #Color change: "\033[cod_formato;cod_texto;cod_fondom"
    RED = "\033[0;31m" #RED
    END = "\033[0m" #DEFAULT COLOR
    ERROR = "\033[1;31m" #BOLD RED
    GREEN = "\033[1;32m" #GREEN
    BLUE = "\033[1;34m" #BLUE
    WHITE = "\033[1;37m" #WHITE
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

def log(text):
    if args.verbose:
        print(text)

def main():
    log("Verbose mode is ON")

#=============================================#
# ------------------ Main ------------------- #
#=============================================#

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(color.BLUE + "[INFO] KeyboardInterrupt detected. You killed Bobo :(" + color.END)
