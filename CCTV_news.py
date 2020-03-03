import time
import requests
import datetime
import csv
import json
import re
from lxml import etree

'''
http://api.cportal.cctv.com/api/rest/articleInfo/getScrollList?n=20&version=1&pubDate=1546272000000&p=1&n=20&app_version=803
http://api.cportal.cctv.com/api/rest/articleInfo/getScrollList?n=20&version=1&pubDate=1546358400000&p=2&n=20&app_version=803
http://m.news.cctv.com/2020/02/14/ARTIZRSdZ8PrFMmgJrJJNmhg200214.shtml

'''

# # 1. 创建文件对象
# f = open('央视新闻demo1.csv', 'w', encoding='utf-8', newline='')
#
# # 2. 基于文件对象构建 csv写入对象
# csv_writer = csv.writer(f)
#
# # 3. 构建列表头
# csv_writer.writerow(["标题", "内容"])

# # 4. 写入csv文件内容
# csv_writer.writerow(["l",'18','男'])

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
#     'Cookie': 'vjlast=1579065191.1579065191.30; vjuids=fbb4d598.16fa79eab82.0.d9339e310a717; cna=aY2lFgOm2WgCAXkYQmRdBdD8; _gscu_1112351457=816879006ntm6o18; _gscbrs_1112351457=1; sca=72a191b0'
# }

# '''将数字转换为日期'''
# data_time = 1546358400
# timeArray = time.localtime(data_time)
# Time = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
# print(Time)
# start_time = datetime.datetime.strptime('2019-12-21 00:00:00', '%Y-%m-%d %H:%M:%S')
# timeStamp = time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S'))
# print(timeStamp)


start_time = datetime.datetime.strptime('2019-12-21 00:00:00', '%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime.strptime('2019-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')

for i in range(0, 21):  # 循环天数 356天
    # 将时间转换为数字
    timeStamp = time.mktime(time.strptime(str(start_time), '%Y-%m-%d %H:%M:%S'))
    pubDate = int(timeStamp * 1000)
    # print(pubDate)
    for page in range(1, 15):  # 循环页数 循环 15页
        url = 'http://api.cportal.cctv.com/api/rest/articleInfo/getScrollList?n=20&version=1&pubDate={}&p={}&n=20&app_version=803'.format(
            pubDate, page)
        yangshi_json = requests.get(url, headers=headers).text
        yangshi = json.loads(yangshi_json)
        if yangshi['itemList'] != None:
            detail_url_list = yangshi['itemList']
            for detail in detail_url_list:
                alldata = []
                title = detail['itemTitle']
                detail_url = detail['detailUrl']
                print(title)
                alldata.append(title)
                # print(detail_url)
                try:
                    # 构造详情页url
                    id_re = re.compile('id=(.*?)&|id=(.*\d+)')
                    id = id_re.findall(detail_url)[0]
                    id = ''.join(id)
                    # http://m.news.cctv.com/2019/01/01/ARTItEaS48JPAVhCyFEoXvuj190101.shtml
                    # http://m.news.cctv.com/2019/01/01/ArtitEaS48JPAVhCyFEoXvuj190101.shtml

                    id1 = id[0:4].upper()
                    id2 = id[4:]
                    id_upper = id1 + id2

                    year = start_time.year
                    month = start_time.month
                    day = start_time.day
                    # print(year,month,day)
                    if int(month) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        month = '0' + str(month)
                    if int(day) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        day = '0' + str(day)


                    detail_url = 'http://m.news.cctv.com/{}/{}/{}/{}.shtml'.format(year, month, day, id_upper)
                    print(detail_url)
                    html = requests.get(detail_url, headers=headers).content.decode('utf-8')
                    # with open('yangshi.html', 'w', encoding='utf-8')as f:
                    #     f.write(html)

                    tree = etree.HTML(html)
                    content = tree.xpath('.//div[@class="cnt_bd"]//p/text()|.//div[@class="cnt_bd"]//p//span/text()')
                    content = ''.join(content).strip()
                    alldata.append(content)
                    # 4. 写入csv文件内容
                    csv_writer.writerow(alldata)
                except:
                    continue
        else:
            break
    start_time = start_time + datetime.timedelta(1)  # 天数加一
    if start_time == end_time:
        print('结束')
        break

# 5. 关闭文件
f.close()
