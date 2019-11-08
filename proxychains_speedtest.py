import pythonping
import ParseSsr
from urllib import request
from mmcv import track_parallel_progress, track_progress
import os
import requests
import socket
import speedtest
import curltest
import json

def speed():
    result = dict()

    # test www.google.com
    success_rate, success_ave_time = curltest.test_curl_ave_time('www.google.com', 10)
    
    result['google_success_rate'] = success_rate
    result['google_success_ave_time'] = success_ave_time
    
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
