#coding:utf-8
#包含中文
import urllib2
import redis


if __name__ == "__main__":   
    r = redis.StrictRedis(host='127.0.0.1', port=6379)
    for page in xrange(127):
        for item in xrange(24):
            url = r.get("page"+str(page) + "item" + str(item) + "href")
            img = r.get("page"+str(page) + "item" + str(item) + "src")
            alt = r.get("page"+str(page) + "item" + str(item) + "alt")
            print("page"+str(page) + "item" + str(item))
            print(url)
            print(img)
            print(alt)
            print("-" * 20)
