#!/usr/bin/python
# coding: UTF-8
import pycurl
import sys
import os
from tqdm import tqdm

class Test:
        def __init__(self):
                self.contents = ''
        def body_callback(self,buf):
                self.contents = self.contents + str(buf)
 
 
def test_gzip(input_url):
        t = Test()
        #gzip_test = file("gzip_test.txt", 'w')
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION,t.body_callback)
        c.setopt(pycurl.CONNECTTIMEOUT, 0)
        c.setopt(pycurl.TIMEOUT, 1)
        c.setopt(pycurl.ENCODING, 'gzip')
        c.setopt(pycurl.URL,input_url)
        try:
                c.perform()
        except:
                # print('Fail!!!')
                return -1
        http_code = c.getinfo(pycurl.HTTP_CODE)
        http_conn_time =  c.getinfo(pycurl.CONNECT_TIME)
        http_pre_tran =  c.getinfo(pycurl.PRETRANSFER_TIME)
        http_start_tran =  c.getinfo(pycurl.STARTTRANSFER_TIME)
        http_total_time = c.getinfo(pycurl.TOTAL_TIME)
        http_size = c.getinfo(pycurl.SIZE_DOWNLOAD)
        # print('http_code http_size conn_time pre_tran start_tran total_time')
        # print("%d %d %f %f %f %f"%(http_code,http_size,http_conn_time,http_pre_tran,http_start_tran,http_total_time))
        return http_total_time

def test_curl_ave_time(input_url, times=10):
        success_times = 0.0
        success_total_time = 0
        for i in tqdm(range(times)):
                if i == (times // 2 + 1)  and success_total_time == 0:
                    return 0, 0

                total_time = test_gzip(input_url)
                if total_time >= 0:
                        success_times += 1
                        success_total_time += total_time
        
        return success_times/times*100, success_total_time/success_times if success_times != 0 else 0

if __name__ == '__main__':
        input_url = sys.argv[1]
        success_rate, success_ave_time = test_curl_ave_time(input_url, 10)
        print('success_rate=%.2f%%, success_ave_time=%.4fs'%(success_rate, success_ave_time))
