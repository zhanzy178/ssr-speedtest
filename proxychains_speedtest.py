import pythonping
import ParseSsr
from urllib import request
from mmcv import track_parallel_progress, track_progress
import os
import requests
import socket
import curltest
import json

def speed():
    result = dict()

    test_urls = ['www.google.com']
    with open('test_urls.txt', 'r') as f:
        test_urls += [u.strip() for u in f.readlines() if u.strip() not in test_urls]
    gind = test_urls.index('www.google.com')
    test_urls.insert(0, test_urls.pop(gind))

    google_fail = False
    for url in test_urls:
        # test www.google.com
        if google_fail:
            result[url] = dict(success_rate=0, ave_time=0)
            continue
        success_rate, success_ave_time = curltest.test_curl_ave_time(url, 1)
        result[url] = dict(success_rate=success_rate, ave_time=success_ave_time)
        if url == 'www.google.com':
            if success_rate == 0:
                google_fail = True

    with open('speed_result.json', 'w') as f:
        json.dump(result, f)

    """
    # network ip
    if True:
    # try:
        ip=requests.get('http://api.ip.sb/ip', timeout=15).text.strip()
        result['ip']=ip
        print("network_test,ip:",result['ip'])
    # except:
    #     pass
    """

    # speedtest
    """
    if True:
        speedtest_session = speedtest.Speedtest()
        speedtest_session.get_best_server()
        speedtest_session.download()
        speedtest_session.upload()
        speedtest_session.results.share()
        speed_test_results = speedtest_session.results.dict()
        result['ping']=speed_test_results['ping']
        result['download']=round(speed_test_results['download'] / 1000.0 / 1000.0,2)
        result['upload']=round(speed_test_results['upload'] / 1000.0 / 1000.0 ,2)
        result['state']="Success"
        result['ip']=speed_test_results['client']['ip']
        print("speed_test,ping:%s,download:%s,upload:%s" % (result['ping'],result['download'],result['upload']))
    # except:
    #    pass
    """
    
   
if __name__ == '__main__':
    speed()
