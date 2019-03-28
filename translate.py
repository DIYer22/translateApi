#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: DIYer22@github
@mail: ylxx@live.com
Created on Wed Mar 20 15:19:47 2019
"""
from boxx import *
from boxx import pd, isfile, timeit, makedirs, pathjoin, sleep, listToBatch

import threading, requests
    
from translateApis import BaiduTrans, GoogleTrans
apiDicts = {
        'google':GoogleTrans,
        'baidu':BaiduTrans,
        }

class Translate:
    def __init__(self, src='zh', dest='en', api='baidu', cache_path=None):
        self.src = src
        self.dest = dest
        self.df = {}
        
        self.api = apiDicts[api](src=src, dest=dest)
        
        
        if cache_path is None:
            makedirs('translate.cache')
            cache_path = pathjoin('translate.cache', f'{src}_to_{dest}.csv')

        self.cache_path = cache_path
        if cache_path:
            if not isfile(cache_path):
                df=pd.DataFrame(columns=['src', 'dest']).set_index('src')
                df.to_csv(cache_path)
            
            self.lock = threading.Lock()
            self.df = df = pd.read_csv(cache_path).set_index('src')
    
    def __call__(self, s='try', batch_size=200, gap=.01):
        if isinstance(s, (list, tuple)):
            return self.translteMultiInGoogle(s, batch_size=batch_size, gap=gap)
        else:
            return self.translateSingle(s)
    
    def translateSingle(self,s):
        for i in range(5):
            try:
                if s not in self.df.index:
                    text = self.api(s)
                    self.lock.acquire()
                    self.df.loc[s] = text
                    if self.cache_path:
                        with open(self.cache_path, 'a') as f:
                            f.write(','.join([s.replace(',', ' '), text.replace(',', ' ')])+'\n')
                    self.lock.release()
                return self.df.loc[s].dest
            except requests.exceptions.RequestException as e:
                 print(i,e)

    def __translteMultiInGoogle(self, ss, batch_size=200, gap=240 ):
        '''
        give up
        '''
        df = self.df
        toTrans = [s for i,s in enumerate(ss) if s not in df.index]
        batchs = listToBatch(toTrans, batch_size)
        for ind, batch in enumerate(batchs):
            for tryn in range(9):
                try:
                    with timeit('%snd batch, %s requests'%(ind, len(batch))):
                        tryn and sleep(gap*1.5**tryn)
                        res = self.translator.translate(list(batch), src=self.src, dest=self.dest)
                    texts = [re.text for re in res]
                    self.lock.acquire()
                    for s,text in zip(toTrans, texts):
                        df.loc[s] = text
                    
                    if self.cache_path:
                        strr = '\n'.join([','.join([s.replace(',', ' '), text.replace(',', ' ')])  for s,text in zip(toTrans, texts)])+'\n'
                        
                        with open(self.cache_path, 'a') as f:
                            f.write(strr)
                    self.lock.release()
                    pred('【OK】 %snd/%s batch, %s requests'%(ind, len(toTrans)//batch_size, len(batch)))
                    sleep(gap)
                    break
                except Exception as exc:
                    print('tryn:', tryn, exc.__repr__())
                    
#        g()
#        return df.loc[ss].dest
    

if __name__ == "__main__":
    self = t = Translate(src='en', dest='zh')
    
#    with timeit():
#        print(t(['trees', 'toys', 'cups', 'goods','son']))
#    re = self.translator.translate('good', src=self.src, dest=self.dest)
    with timeit():
        print(t('try'))
    
    
