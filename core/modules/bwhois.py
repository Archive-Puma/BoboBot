#=========================================================#
# ---------------------- Limitations -------------------- #
#=========================================================#

# -- Whois only works with .com, .net or .edu websites -- #


from pythonwhois import get_whois
from pythonwhois.shared import WhoisException   #Not Root Server Exception

def getwhois(site):
    try:
        who_is = get_whois(site)
        return who_is
    except WhoisException:
        return "No WHOIS root server found for \'{0}\' domain".format(site)

def whois(person, site):
    person = str(person).lower()

    if person != 'admin' and person != 'tech' and person != 'registrant' and person != 'billing':
        return "[[ BOBO's MODULE : WHOIS ]]" + \
            "\n\nusage: /whois person url [url2, url3, ...]" + \
            "\n--------------------------------------------------------" + \
            "\nperson = {admin, tech, registrant, billing}" + \
            "\nonly .com, .net or .edu sites are available" + \
            "\n\nexamples:" + \
             "\n - /whois admin google.com" + \
             "\n - /whois tech hotmail.com" + \
             "\n - /whois registrant github.com amazon.com"

    who_is = getwhois(str(site))
    if type(who_is) == type(dict()):
        information = "[[ " + person.upper() + " ]]"
        try:
            information += "\n\n[Name] " + str(who_is['contacts'][person]['name'])
            information += "\n[Organization] " + str(who_is['contacts'][person]['organization'])
            information += "\n --------------------------------------------------- "
            information += "\n[Phone] " + str(who_is['contacts'][person]['phone'])
            information += "\n[Email] " + str(who_is['contacts'][person]['email'])
            information += "\n --------------------------------------------------- "
            information += "\n[Country] " + str(who_is['contacts'][person]['country'])
            information += "\n[City] " + str(who_is['contacts'][person]['city']) + \
                ", " + str(who_is['contacts'][person]['state'])
            information += "\n[Street] " + str(who_is['contacts'][person]['street']) + \
                " - Postal Code: " + str(who_is['contacts'][person]['postalcode'])
        except KeyError:
            information += "\n[ No {0} information available ]".format(person)
        except TypeError:
            information += "\n[ No {0} information available ]".format(person)

        return information
    else:
        return who_is

def whoare(site):
    information = str()
    information += whois('admin',site)
    information += "\n\n" + whois('tech',site)
    information += "\n\n" + whois('registrant',site)
    information += "\n\n" + whois('billing',site)

    if "No WHOIS root server found" in information:
        return "No WHOIS root server found for \'{0}\' domain".format(site)
    else:
        return information
