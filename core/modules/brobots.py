from requests import get
from requests import exceptions

def get_robots(site):
    try:
        try:
            robots = get("{0}/robots.txt".format(site)).text
        except exceptions.MissingSchema:
            robots = get("http://{0}/robots.txt".format(site)).text
        if robots[0] == '<':
            raise exceptions.ConnectionError
    except exceptions.ConnectionError:
        return "There is no 'robots.txt' available in {0}".format(site)

    return str(robots).strip()
