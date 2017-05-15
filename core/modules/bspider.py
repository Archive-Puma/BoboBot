from urllib2 import urlopen, urlparse, HTTPError, URLError
from urllib2 import urlopen
from html.parser import HTMLParser

class PeterParker(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for(key, value) in attrs:
                newUrl = urlparse.urljoin(self.baseUrl,value)
                self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        s_response = urlopen(url)
        if s_response.info().getheader('Content-Type') == 'text/html':
            htmlBytes = s_response.read()
            htmlString = htmlBytes.decode('utf-8')
            self.feed(htmlString)
            return htmlString, self.links
        else:
            return '', []

def spider(url,maxPages,word):
    site = url.split('://',1)[1]
    pages = [url]
    visitedPages = []
    numberVisited = 0
    foundWord = False
    crawler_response = str()
    while numberVisited < int(maxPages) and pages != [] and not foundWord:
        url = pages[0]
        pages = pages[1:]
        try:
            if url in visitedPages or not site in url.split('://',1)[1]:
                continue
        except IndexError:
            continue
        visitedPages.append(url)
        numberVisited = numberVisited + 1
        crawler_response = crawler_response + url + "\n"
        try:
            parser = PeterParker()
            try:
                data,links = parser.getLinks(url)
            except (HTTPError, URLError):
                data = ''
                links = []
            if data.find(word) > -1:
                foundWord = True
            pages = pages + links
        except KeyboardInterrupt:
            return "There was an error"
    if foundWord:
        crawler_response = crawler_response + "\nThe word {0} was found at {1}".format(word,url)

    return crawler_response
