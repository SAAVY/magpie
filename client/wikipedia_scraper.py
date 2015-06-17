import wikipedia
import lxml.html
import sys


def scrape(url):
    t = lxml.html.parse(url)
    title = t.find(".//title").text

    page = wikipedia.page(title)
    print page.summary
    print "Image: {0}".format(page.images[0])
    print "Title: {0}".format(title)



if __name__ == "__main__":
    scrape("http://en.wikipedia.org/wiki/NP-complete")
