# -*- coding: utf-8 -*-
# @Time    : 2018/5/20 23:34
# @Author  : Yuan Zheng
# @Version    : 0.0.1
# @File    : main.py

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
import pytesseract
import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


# 每月的天数
def month_dict(year, month):
    dict_t = {1:31, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            return 29
        else:
            return 28
    else:
        return dict_t.get(month)




# 此函数用于打开浏览器
def openbrowser():
    global browser
    url = "http://index.baidu.com/"#百度指数网站
    browser = webdriver.Chrome('chromedriver.exe')
    browser.maximize_window()
    browser.get(url)
    # 点击网页的登录按钮
    browser.find_element_by_xpath('//*[@id="home"]/div[1]/div[2]/div[1]/div[4]').click()
    time.sleep(3)
    # 传入账号密码
    account="######"
    passwd="######"

    browser.find_element_by_id("TANGRAM__PSP_4__userName").send_keys(account)
    browser.find_element_by_id("TANGRAM__PSP_4__password").send_keys(passwd)
    browser.find_element_by_id("TANGRAM__PSP_4__submit").click()

    time.sleep(3)

    input("登陆完成请回车")


def get_image_first(name,year, month):
    year = str(year)
    if month < 10:
        month = '0'+ str(month)
    else:
        month = str(month)
    print(name, year, month)
    try:
        # 清空网页输入框
        browser.find_element_by_xpath('//*[@id="search-input-form"]/input[3]').clear()
        # 写入需要搜索的百度指数
        browser.find_element_by_xpath('//*[@id="search-input-form"]/input[3]').send_keys(name)
        # 点击搜索
        browser.find_element_by_class_name("search-input-operate").click()
    except:
        # 清空网页输入框
        browser.find_element_by_xpath('//*[@id="schword"]').clear()
        # 写入需要搜索的百度指数
        browser.find_element_by_xpath('//*[@id="schword"]').send_keys(name)
        # 点击搜索
        browser.find_element_by_xpath('//*[@id="schsubmit"]').click()

    # 点击网页上的开始日期
    browser.maximize_window()
    time.sleep(3)
    t = []
    while not t:
        try:
            browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
        except:
            try:
                tt = browser.find_element_by_xpath('/html/body/div[3]/div[1]/a')
                if tt:
                    return -1
            except:
                pass
            # tt = browser.find_element_by_xpath('/')
            time.sleep(1)
        t = browser.find_elements_by_xpath("//span[@class='selectA yearA']")
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + year + "']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + month + "']").click()

    # 选择网页上的截止日期
    browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + year + "']").click()
    browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
    browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + month + "']").click()

    browser.find_element_by_xpath("//input[@value='确定']").click()

    # 截取指数的图片
    browser.execute_script("""
                    (function () {
                        var y = 100;
                        var step = 100;
                        window.scroll(0, 0);

                        function f() {
                            window.scroll(0, y);
                            document.title += "scroll-done";
                        }

                        setTimeout(f, 1000);
                    })();
                """)
    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(2)
    # time.sleep(2)
    try:
        t = browser.find_elements_by_xpath('//*[@id="trend"]/div/p')
        if t:
            return 1
    except:
        pass
    browser.save_screenshot("test.png")
    return 0


# 返回 1 重做
def get_image(name,year, month):
    year = str(year)
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    print(name, year, month)
    t = []
    valid = 0
    while not t:
        try:
            browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
            t = browser.find_elements_by_xpath("//span[@class='selectA monthA']")
        except:
            time.sleep(1)

    while not valid:
        try:
            browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
            browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + month + "']").click()
            browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
            browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + year + "']").click()

            # 选择网页上的截止日期
            browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
            browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + month + "']").click()
            browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
            browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + year + "']").click()

            browser.find_element_by_xpath("//input[@value='确定']").click()
            valid = 1
        except Exception as e:
            print(e)
            time.sleep(2)
    time.sleep(2)

    try:
        t = browser.find_elements_by_xpath('//*[@id="trend"]/div/p')
        if t:
            return 1
    except:
        pass

    browser.save_screenshot("test.png")
    return 0




def get_axis():
    im = Image.open('test.png')
    print(im.size)

    # 此处参数需要根据窗口大小调整
    width = 100
    height = 260
    left = 1610
    top = 581
    valid = np.zeros(7, dtype='int')
    for i in range(7):
        im_t = im.crop((left, top + 38 * i, left + width, top + 38 * (i+1)))

        imname = 'axis'+str(i+1)+'.png'
        print(imname)
        im_t.save(imname)
        r,g,b = im_t.split()
        w,h = b.size
        b = b.resize((2*w,2*h))
        b.save('axis_b'+str(i+1)+'.png')
        code = pytesseract.image_to_string(b)
        code_true = code.replace(',','')
        print(code_true)

        try:
            code_int = int(code_true)
            valid[i] = code_int
        except:
            pass
    print(valid)
    internal = dict()
    for i in range(6):
        if valid[i] != 0 and valid[i+1] !=0:
            internal[str(valid[i]-valid[i+1])] =  internal.get(str(valid[i]-valid[i+1]),0) + 1
    internal = sorted(internal.items(), key=lambda d: d[1],reverse = True)
    if not internal:
        max_index = 7
        min_index = 0
    else:
        print(internal[0])
        if (internal[0][1]<3):
            print('---------ERROR----------')
        for i in range(6):
            if valid[i] != 0 and valid[i + 1] != 0:
                if valid[i] - valid[i + 1] == int(internal[0][0]):
                    max_index = valid[i] + i*int(internal[0][0])
                    min_index = valid[i] - (7-i) * int(internal[0][0])
                    break
    print('max index', max_index)
    print('min_index', min_index)
    return max_index, min_index


# 采用r通道是否小于120来获取曲线
def get_value(year, month, from_day ,to_day, max_index, min_index):
    days = month_dict(year, month)
    im = Image.open('test.png')
    print(im.size)

    # 此参数根据具体窗口大小需要调整
    right = 1703
    left = 186
    top = 582
    bottom = 844
    valid = np.zeros(7, dtype='int')
    im_t = im.crop((left, top, right, bottom))
    im_t.save('value.png')
    r,g,b = im_t.split()
    r = np.asarray(r)
    r_line = np.zeros_like(r)
    r_line[(r < 120)] = 1
    sns.heatmap(r_line)
    plt.show()

    i = from_day
    width = im_t.size[0]
    height = im_t.size[1]
    days = month_dict(year, month)
    print(width, height, days)
    while i <= to_day:
        index = int((width - 1) * (i - 1)/(days - 1))
        height_index = np.nonzero(r_line[:, index])[0][-1]
        value = int((height - 1 - height_index)/(height - 1)*(max_index - min_index) + min_index)
        print(year, month, i, value)
        sort_times.append((datetime.date(year, month, i).strftime("%Y-%m-%d"),value))
        i += 1

def get_all_value(name, from_time, end_time):
    global sort_times
    sort_times = list()
    from_year, from_month, from_day = map(int, from_time.split('-'))
    end_year, end_month, end_day = map(int, end_time.split('-'))
    i_year = from_year
    i_month = from_month

    while i_year <= end_year:
        if i_year == from_year and i_year == end_year:
            while i_month <= end_month:
                if i_month == from_month and i_month == end_month:
                    back = 1
                    while back != 0:
                        if back == -1:
                            return list()
                        back = get_image_first(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, from_day, end_day, max_index, min_index)
                    print(i_year, i_month, from_day, end_day)
                elif i_month == from_month:
                    back = 1
                    while back != 0:
                        if back == -1:
                            return list()
                        back = get_image_first(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, from_day, month_dict(i_year, i_month), max_index, min_index)
                    print(i_year, i_month, from_day, month_dict(i_year, i_month))
                elif i_month == end_month:
                    back = 1
                    while back != 0:
                        back = get_image(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, 1, end_day, max_index, min_index)
                    print(i_year, i_month, 1, end_day)
                else:
                    back = 1
                    while back != 0:
                        back = get_image(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, 1, month_dict(i_year, i_month), max_index, min_index)
                    print(i_year, i_month, 1, month_dict(i_year, i_month))
                i_month += 1
        elif i_year == from_year:
            while i_month <= 12:
                if i_month != from_month:
                    back = 1
                    while back != 0:
                        back = get_image(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, 1, month_dict(i_year, i_month), max_index, min_index)
                    print(i_year, i_month, 1, month_dict(i_year, i_month))
                else:
                    back = 1
                    while back != 0:
                        if back == -1:
                            return list()
                        back = get_image_first(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, from_day, month_dict(i_year, i_month), max_index, min_index)
                    print(i_year, i_month, from_day, month_dict(i_year, i_month))
                i_month += 1
        elif i_year == end_year:
            while i_month <= end_month:
                if i_month != end_month:
                    back = 1
                    while back != 0:
                        back = get_image(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, 1, month_dict(i_year, i_month), max_index, min_index)
                    print(i_year, i_month, 1, month_dict(i_year, i_month))
                else:
                    back = 1
                    while back != 0:
                        back = get_image(name, i_year, i_month)

                    max_index, min_index = get_axis()
                    get_value(i_year, i_month, 1, end_day, max_index, min_index)
                    print(i_year, i_month, 1, end_day)
                i_month += 1
        else:
            while i_month <= 12:
                back = 1
                while back != 0:
                    back = get_image(name, i_year, i_month)

                max_index, min_index = get_axis()
                get_value(i_year, i_month, 1, month_dict(i_year, i_month), max_index, min_index)
                print(i_year, i_month, 1, month_dict(i_year, i_month))
                i_month += 1
        i_year += 1
        i_month = 1
    return sort_times

if __name__ == '__main__':
    openbrowser()
    key_word = 'XXX'
    from_time = '2012-01-01'
    end_time = '2018-04-30'
    index = get_all_value(key_word, from_time, end_time)
    print(index)
    #get_axis()
