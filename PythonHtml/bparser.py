from HTMLParser import HTMLParser
import urllib2
import redis
import shutil
import os


class MyHTMLParser(HTMLParser):   
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.image = None
        self.inMainImage = False
    def handle_starttag(self, tag, attrs):   
        if tag == "div":
            for (k, v) in attrs:
                if(k == "class" and v == "main-image"):
                    self.inMainImage = True
        elif tag == "img":
            if(self.inMainImage):
                attrs = dict(attrs)
                self.image = attrs["src"]
                print("get image : ", self.image)
    
    def handle_endtag(self, tag):
        if tag == "div":
            if(self.inMainImage):
                self.inMainImage = False

def savePics(dir, l):
    if(os.path.exists(dir)):
        shutil.rmtree(dir)
    os.mkdir(dir)
    index = 1
    for i in l:
        cache = urllib2.urlopen(i).read()
        f = open(dir + "/" + str(index) + ".png", "wb")
        f.write(cache)
        f.close()
        index += 1
        print("write : ", dir + "/" + str(index) + ".png")
    print("write over")
        

if __name__ == "__main__":   
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    for page in xrange(127):
        for item in xrange(24):
            url = r.get("page"+str(page) + "item" + str(item) + "href")
            if(os.path.exists("page"+str(page) + "item" + str(item))):
                continue
            print("main url : ", url)
            index = 1
            pics = []
            while True:
                send_headers = {
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                }
                req = urllib2.Request(url + "/" + str(index),headers=send_headers)
                response = None
                html_code = None
                
                response = urllib2.urlopen(req)
                html_code = response.read()

                try:
                    hp = MyHTMLParser()   
                    hp.feed(html_code)   
                    hp.close()   

                    if(hp.image in pics):
                        print(pics)
                        savePics("page"+str(page) + "item" + str(item), pics)
                        break
                    else:
                        pics.append(hp.image)
                except Exception,e:
                    print e
                    index += 1
                    break
                finally:
                    index += 1

    # for page in xrange(127):
    #     req = urllib2.Request("http://www.mzitu.com/page/" + str(page),headers=send_headers)
    #     html_code = urllib2.urlopen(req).read()
    #     # fh=open('b.html','w')
    #     # fh.write(html_code)
    #     # fh.close()
    #     hp = MyHTMLParser()   
    #     hp.feed(html_code)   
    #     hp.close()   

    #     for i in xrange(len(hp.imgs)):
    #         r.set("page"+str(page) + "item" + str(i) + "alt", hp.alts[i])
    #         r.set("page"+str(page) + "item" + str(i) + "src", hp.imgs[i])
    #         r.set("page"+str(page) + "item" + str(i) + "href", hp.links[i])

    