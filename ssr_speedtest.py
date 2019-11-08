import pythonping
import ParseSsr
from urllib import request
from mmcv import track_parallel_progress, track_progress
import os
import sys
import requests
import socket
import json
import prettytable as pt
timeout=600
ssr_config_path = '/usr/local/share/shadowsocksr/config.json'

def get_free_port(iface=None):
    s = socket.socket()
    if iface:
        s.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, bytes(iface,'utf8'))
    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()
    return port

def ping_ssrserver(url):
    try:
        r = pythonping.ping(url, timeout=timeout*1e-3)
        return (r.rtt_avg_ms, r.rtt_min_ms, r.rtt_max_ms)
    except:
        return (timeout, timeout, timeout)

def multithread_ping_ssrserver(ssr_config):
    urls = [s['server'] for s in ssr_config]
    return track_parallel_progress(ping_ssrserver, urls, len(urls))


def ssr_service(ssr, port=6667):
    ssr_config_json = dict(
            server=ssr['server'],
            local_address='127.0.0.1',
            local_port=port,
            timeout=300,
            workers=1,
            server_port=ssr['port'],
            password=ssr['password'],
            method=ssr['method'],
            obfs=ssr['obfs'],
            obfs_param=ssr['obfsparam'],
            protocol=ssr['protocol'],
            protocol_param=ssr['protoparam']) 
    os.system('ssr stop')
    with open(ssr_config_path, 'w') as f:
        json.dump(ssr_config_json, f)
    os.system('ssr start')
    print(ssr['remarks']+"/"+ssr['server'])
    

def outwall_speed_test(ssr_config):
    port = get_free_port()
    port = 6667
    ssr_service(ssr_config, port)

    os.system('rm speed_result.json')
    os.system('proxychains4 -q -f proxychains.conf %s proxychains_speedtest.py'%sys.executable)

    if os.path.exists('speed_result.json'):
        with open('speed_result.json', 'r') as f:
            result = json.load(f)
        os.system('rm speed_result.json')
        return result
    else:
        return dict()

def subscribe_ssr_config(sub_url):
    
    # get subsrible url results.
    ssr_config=[]
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    f=request.Request(sub_url, headers=headers) 

    ssr_subscribe = request.urlopen(f).read().decode('utf-8')
    ssr_subscribe_decode = ParseSsr.base64_decode(ssr_subscribe)
    ssr_subscribe_decode=ssr_subscribe_decode.replace('\r','')
    ssr_subscribe_decode=ssr_subscribe_decode.split('\n')

    for i in ssr_subscribe_decode:
        if(i):
            decdata=str(i[6:])
            ssr_config.append(ParseSsr.parse(decdata))
    
    return ssr_config

if __name__ == '__main__':
    # subscribe
    sub_urls = []
    with open('sub_urls.txt', 'r') as f:
        sub_urls = f.readlines()

    ssr_config = []
    for sub_url in sub_urls:
        ssr_config += subscribe_ssr_config(sub_url)

    # test ping results.
    ping_result = multithread_ping_ssrserver(ssr_config)
    valid_index = [i for i, v in enumerate(ping_result) if v[0] <= 20 and '回国' not in ssr_config[i]['remarks'] and '打机' not in ssr_config[i]['remarks'] and '游戏' not in ssr_config[i]['remarks']]#  and 'cchkbn.ccddns.online' in ssr_config[i]['server']]
    ping_result_str = '%d/%d servers are ping accessible!!!\n%.2f%% ping pass rate!!!'%(len(valid_index), len(ssr_config), 100.0*(float(len(valid_index))/len(ssr_config)))
    ssr_config = [ssr_config[i] for i in valid_index]
    ping_result = [ping_result[i] for i in valid_index]
    

    # test speed
    results_list = track_progress(outwall_speed_test, ssr_config)
    for i in range(len(results_list)):
        results_list[i]['remarks'] = ssr_config[i]['remarks']
        results_list[i]['ping'] = ping_result[i][0]

    ssr_service(results_list[0])

    # print result
    results_list = sorted(results_list, key=lambda s:(-s['google_success_rate'], s['google_success_ave_time']))
    tb = pt.PrettyTable()
    tb.field_names = ['Server',  'Google Access Rate', 'Google Acess Delay', 'Ping(ms)']
    for r in results_list:
        tb.add_row([r['remarks'], '%.2f%%'%r['google_success_rate'], '%.3fs'%r['google_success_ave_time'], r['ping']]) 
    
    print(ping_result_str)
    print(tb)
