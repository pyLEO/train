#! /usr/bin/python3 env
# -*- coding: utf-8 -*-

"""
this module solve the api code return
"""

import requests, base64, json, hashlib, time

# base url
taobao_img_url = "http://taobaodama.hangtian123.net"
qunar_api_url = "http://api.pub.train.qunar.com/captcha/api/captcha.jsp"
qunar_product_url = "/captcha/api/uploadCaptcha.jsp"
qunar_product_callback = "/captcha/api/queryResult.jsp"
qunar_feedback_result = "/captcha/api/feedbackResult.jsp"
product_key = "hangt"
product_agentcode = "0C13D7C3566147EB90D1E273278DCDD9"


def get_qunar_id(imgpath):
    """
    :param imgpath:
    :return globalid:
    """
    with open(imgpath, 'rb') as f:
        ef = base64.b64encode(f.read())

    make_md5 = product_agentcode + product_key + str(ef, 'utf-8')
    md5 = hashlib.md5(make_md5.encode('utf-8')).hexdigest()
    data = {
        'agentCode': product_key,
        'image': str(ef, 'utf-8'),
        'hmac': md5
    }

    response = requests.post(taobao_img_url+qunar_product_url, data)
    globalid = json.loads(response.text)['data']['globalId']
    return globalid


def get_qunar_result(gid):
    """
    :param gid:
    :return res:
    """
    time.sleep(2)
    make_md5 = product_agentcode + product_key + gid
    md5 = hashlib.md5(make_md5.encode('utf-8')).hexdigest()

    data = {
        'agentCode': product_key,
        'globalId': gid,
        'hmac': md5
    }

    response = requests.post(taobao_img_url + qunar_product_callback, data)
    result = json.loads(response.text)['data']['result']
    result_list = []
    for i in list(result.split(',')):
        result_list.append(i)
    return result_list



