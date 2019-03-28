#/usr/bin/env python3
#coding=utf8
from boxx import *
import http.client as httplib
import hashlib as md5
import urllib
import random
import json


# Baidu Translate API key
appid = 'xxx' #你的appid
secretKey = 'xxx' #你的密钥



class BaiduTrans():
    def __init__(self, src = 'en', dest = 'zh'):
        self.fromLang = src
        self.toLang = dest
    def __call__(self, q='apple'):
        myurl = '/api/trans/vip/translate'
        
        
        salt = random.randint(32768, 65536)
        
        sign = appid+q+str(salt)+secretKey
        m1 = md5.new('md5')
        m1.update(sign.encode('utf8'))
        sign = m1.hexdigest()
        self.urltmpl = myurl+'?appid='+appid+'&q='+'%s'+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(salt)+'&sign='+sign
        myurl = self.urltmpl%urllib.parse.quote(q)
        
        httpClient = None
        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
         
            #response是HTTPResponse对象
            response = httpClient.getresponse()
            resp = response.read()
            re = json.loads(resp.decode('utf8'))
            return re['trans_result'][0]['dst']
#            print(re)
#        except Exception as e:
#            print(e)
        finally:
            if httpClient:
                httpClient.close()

#.encode('utf-8').decode('unicode_escape')




class GoogleTrans():
    '''
    `pip install googletrans`

    google API 会限制IP, 在 240s 的间隔了会禁止访问
    google API 支持一个 http 请求, 翻译一个 List 
    '''
    def __init__(self, src = 'en', dest = 'zh-CN'):
        self.src = src
        self.dest = dest
    
        from googletrans import Translator
        
        self.trans = Translator(service_urls=[
              'translate.google.cn',
        #      'translate.google.com',
            ])
    
    
    def __call__(self, q='apple'):
        return self.trans.translate(q, src=self.src, dest=self.dest).text

if __name__ == "__main__":
    self = t = GoogleTrans(src='en', dest='zh-CN')
#    self = t = BaiduTrans(src='en', dest='zh')
    with timeit():
        re = tree/t('good')
        