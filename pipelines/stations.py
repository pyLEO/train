#!/usr/bin/python3 env
# -*- coding: UTF-8 -*-

"""
store stations index in redis
"""


from lxml import html
import re
import redis, time

def get_stations():

    browser.get("https://kyfw.12306.cn/otn/leftTicket/init")
    time.sleep(2)
    WebDriverWait(browser, 10).until(lambda x: x.find_element_by_css_selector('input#fromStationText'))

    browser.find_element_by_xpath("//input[contains(@id,'fromStationText')]").click()

    redis = redis.StrictRedis(host='127.0.0.1')

    for i in range(1, 7):
        # 点击标签
        time.sleep(2)
        browser.find_element_by_css_selector("li#nav_list{}".format(i)).click()

        if i == 1:
            doc = html.document_fromstring(browser.page_source)
            for d in doc.xpath("//ul[contains(@id,'ul_list')]//li"):
                redis.hmset("stations", {d.get('title'): d.get("data")+",1,0,0"})
        else:
            # 获取分页
            tab = browser.find_element_by_xpath("//a[contains(@class,'cityflip')]")
            onclick = tab.get_attribute("onclick")
            page_num = re.search(r'\d+,', onclick, re.M | re.I)
            if page_num:
                num = int(page_num.group().strip(','))
                for j in range(num):
                    # 点击分页
                    if j == 0:
                        doc = html.document_fromstring(browser.page_source)
                        row_num = doc.xpath("count(//*[contains(@id,'ul_list{}')]//ul)".format(i))
                        # 获取行数
                        for k in range(1, int(row_num)+1):
                            for d in doc.xpath("//*[contains(@id,'ul_list{}')]//ul[contains(@class,"
                                               "'popcitylist')][{}]//li".format(i, k)):
                                redis.hmset("stations", {d.get('title'): str(d.get("data")) +
                                            ",{},{},{}".format(i, j + 1, k)})
                    else:
                        time.sleep(2)
                        browser.find_element_by_xpath("//a[contains(@class,'cityflip') "
                                                      "and contains(.,'下一页')]").click()

                        doc = html.document_fromstring(browser.page_source)
                        row_num = doc.xpath("count(//*[contains(@id,'ul_list{}')]//ul)".format(i))
                        for k in range(1, int(row_num)+1):
                            for d in doc.xpath("//*[contains(@id,'ul_list{}')]//ul[contains(@class,"
                                               "'popcitylist')][{}]//li".format(i, k)):
                                redis.hmset("stations", {d.get('title'): str(d.get("data")) +
                                            ",{},{},{}".format(i, j+1, k)})
            else:
                print('wrong page number')
