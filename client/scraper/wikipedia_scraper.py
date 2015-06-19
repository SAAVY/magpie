import wikipedia
import lxml.html
import sys
import requests


def scrape(url):
    print url
    r = requests.get(url)
    t = lxml.html.fromstring(r.content)
    title = t.find(".//title").text

    page = wikipedia.page(title)
    print page.summary
    print "Image: {0}".format(page.images[0])
    print "Title: {0}".format(title)



if __name__ == "__main__":
    scrape("http://en.wikipedia.org/wiki/NP-complete")
