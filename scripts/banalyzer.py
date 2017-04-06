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
__version__ = "1.0 BoboAnalyzer"
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

#########################
##     REQUIREMENTS    ##
#########################

try:
    import requests
except ImportError:
    print(CERROR + "[ERROR] Please, install REQUESTS module\n[ERROR] Try to use 'pip install requests' or 'pip install --upgrade requests'" + CDEFAULT)
    exit(0xDEAD)


#########################
##      FUNCTIONS      ##
#########################

def Analyze(APIKEY, url):

    #Analize the URL
    headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent" : "gzip,  Bobo Bot is analizing this URL"
    }
    params = {'apikey': APIKEY, 'resource': url}
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
            params = {'apikey': APIKEY, 'url': url}
            response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params).json()
        except:
            myresponse = "Creo que he hecho algo mal, mi amo. Vuelva a intentarlo por favor"
            print(CRED + "[ERROR] Algo ha fallado al analizar la URL" + CDEFAULT)
            return myresponse
        myresponse = "La URL nunca ha sido analizada anteriormente por ninguno de esos no-humanos llamados 'Antivirus'. Tardaré un rato en analizarla. Por favor, espere y vuelva a preguntármelo en un rato"

    return myresponse


#########################
##       DEBUGGER      ##
#########################

if __name__ == '__main__':
    import sys
    try:
	api = sys.argv[1]
        url = sys.argv[2]
    except IndexError:
        print("[ERROR] Usage: python Bobo-Crawl.py APIKEY URL")
        exit(0xDEAD)
    print (url, Analyze(api,url))
