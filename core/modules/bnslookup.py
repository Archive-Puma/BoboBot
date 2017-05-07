from dns import resolver

def nslookup(mode,site):
    try:
        answer = resolver.query(site,mode)
        answer = answer.response.to_text()
        answer = answer.split(";ANSWER")[1]
        answer = answer.split(";AUTHORITY")[0]
    except resolver.NoAnswer:
        return "There is no answer for {0} in {1}".format(site,mode)
    except resolver.NXDOMAIN:
        return "There is no answer for {0} in {1}".format(site,mode)

    return answer
