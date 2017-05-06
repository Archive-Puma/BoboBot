from requests import get

def is_last_version(version):
    last_version = get('https://raw.githubusercontent.com/CosasDePuma/BoboBot/master/version.txt')
    if str(last_version.text).strip() != version:
        return False
    else:
        return True
