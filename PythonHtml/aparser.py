from HTMLParser import HTMLParser
import urllib2
import redis


class MyHTMLParser(HTMLParser):   
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []
        self.imgs = []
        self.alts = []
        self.filter = set()
        self.inPins = False
    def handle_starttag(self, tag, attrs):   
        if tag == "ul":
            for (k, v) in attrs:
                if(k == "id" and v == "pins"):
                    self.inPins = True
        elif tag == "a":
            if(self.inPins):
                attrs = dict(attrs)
                if(not attrs["href"] in self.filter):
                    self.links.append(attrs["href"])
                    self.filter.add(attrs["href"])
        elif tag == "img":
            if(self.inPins):
                attrs = dict(attrs)
                self.imgs.append(attrs["data-original"])
                self.alts.append(attrs["alt"])

    def handle_endtag(self, tag):
        if tag == "ul":
            if(self.inPins):
                self.inPins = False



if __name__ == "__main__":   
    r = redis.StrictRedis(host='127.0.0.1', port=6379)

    send_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
    }
    for page in xrange(127):
        req = urllib2.Request("http://www.mzitu.com/page/" + str(page),headers=send_headers)
        html_code = urllib2.urlopen(req).read()
        # fh=open('b.html','w')
        # fh.write(html_code)
        # fh.close()
        hp = MyHTMLParser()   
        hp.feed(html_code)   
        hp.close()   

        # namePrefix = "img_"
        # nameIndex = 1
        # for i in hp.imgs:
        #     cache = urllib2.urlopen(i).read()
        #     f = open(namePrefix + str(nameIndex) + ".png", "wb")
        #     f.write(cache)
        #     f.close()
        #     nameIndex += 1

        for i in xrange(len(hp.imgs)):
            r.set("page"+str(page) + "item" + str(i) + "alt", hp.alts[i])
            r.set("page"+str(page) + "item" + str(i) + "src", hp.imgs[i])
            r.set("page"+str(page) + "item" + str(i) + "href", hp.links[i])

    