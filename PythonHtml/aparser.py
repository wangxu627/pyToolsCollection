from HTMLParser import HTMLParser
import urllib2
import redis
import hashlib

class MyHTMLParser(HTMLParser):   
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []
        self.imgs = []
        self.alts = []
        self.md5 = []
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
                m = hashlib.md5()
                m.update(attrs["href"])
                print("mm : ", m, attrs["href"])
                sig = m.hexdigest()
                if(not sig in self.filter):
                    self.links.append(attrs["href"])
                    self.md5.append(sig)
                    self.filter.add(sig)
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

        for i in xrange(len(hp.imgs)):
            # print("page"+str(page) + "item" + str(i) + "alt", hp.alts[i])
            # print("page"+str(page) + "item" + str(i) + "src", hp.imgs[i])
            # print("page"+str(page) + "item" + str(i) + "href", hp.links[i])
            # print("page"+str(page) + "item" + str(i) + "md5", hp.md5[i])

            # r.set("page"+str(page) + "item" + str(i) + "alt", hp.alts[i])
            # r.set("page"+str(page) + "item" + str(i) + "src", hp.imgs[i])
            # r.set("page"+str(page) + "item" + str(i) + "href", hp.links[i])
            # r.set("page"+str(page) + "item" + str(i) + "md5", hp.md5[i])

            key = hp.md5[i]
            r.set(key + "_alt",  hp.alts[i])
            r.set(key + "_src",  hp.imgs[i])
            r.set(key + "_href", hp.links[i])
            r.set(key + "_md5",  hp.md5[i])

    