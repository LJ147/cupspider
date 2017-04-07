#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by LJ on 2017/3/25
# 获取起点全部小说的基本信息(url 推荐票数等)，存入数据库
import random
import sys
import db_tool
import web_tool
import time

reload(sys)
sys.setdefaultencoding("utf-8")
import datetime


# convert str to num    将count原始值（str） 199.7万字\n  转换为  （int）1997000
def parse_str_number(count):
    isBigNum = False

    for str_in in count.decode('utf-8'):
        # 单位为"万"
        if u'\u4e00' <= str_in <= u'\u9fff':
            count = count[:-1].encode('utf-8')
            isBigNum = True

            if count.find('.') == -1:
                count = int(count) * 10000
            else:
                split_list = count.split(".", -1)
                temp = len(split_list[1])
                try:
                    decimal = 1.0 * int(split_list[1]) / (10 ** temp)
                    count = (int(split_list[0]) + decimal) * 10000
                except ValueError:
                    print split_list
                    count = -1
                    print "ValueError: str to int "
    if isBigNum == False:
        if count.find('.') == -1:
            count = int(count)
        else:
            split_list = count.split('.', 1)
            try:
                count = int(split_list[0])
            except ValueError:
                print split_list
                count = -1
                print "Error: str to int "
    return int(count)


# 爬取、解析并存储单一页面的小说信息（mysql）
def scrape_one_page(page):
    # 排序方式为总推荐票数
    url = 'http://a.qidian.com/?size=-1&sign=-1&tag=-1&chanId=-1&subCateId=-1&orderId=2&update=-1&page={page}&month=-1&style=1&action=-1&vip=-1'.format(
        page=page)
    soup = web_tool.getSoup(url)
    items = soup.find_all('div', class_='book-mid-info')

    print "current page : " + str(page)

    for item in items:
        if item.a != None:

            # 解析界面元素
            title = item.a.text
            book_url = item.a.get('href')[2:]
            update = item.find('p', class_='update').text
            lists = update.split('\n', -1)
            count = lists[0][:-1]
            vote_ticket = lists[1][1:-3]
            count = parse_str_number(count)
            vote_ticket = parse_str_number(vote_ticket)
            details = item.p.text
            author = details.split('|')[0].replace('\n', '')
            types = details.split('|')[1]
            type_one = types.split('·')[0]
            type_two = types.split('·')[1]
            status = details.split('|')[2].replace('\n', '')

            insert = "insert into bookForQidian(title,url,author,typeOne,typeTwo,numberOfWords,recommend,status) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            # 分别为小说标题、url、作者、两种分类、总字数、总推荐票数、状态
            param = (title, book_url, author, type_one, type_two, count, vote_ticket, status)
            #插入状态
            status = db_tool.execute_sql(insert, param)
            if status == 0:
                print '-----插入成功--------'
                print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print "book_name: " + title
                print "author: " + author
                print '--------------------'
            else:
                print '-----插入失败--------'


        else:
            print "no data inside!"


# 递归调用
def craw_all(page):
    TOTAL_PAGE = 28922
    try:
        while (page < TOTAL_PAGE):
            scrape_one_page(page)
            page = page + 1
    # 某一页面出现错误时，页码page加一，跳过该页继续爬取
    except:
        page = page + 1
        craw_all(page)


if __name__ == '__main__':

    start_time = datetime.datetime.now()
    # 初始page
    page = 1
    try:
        while (page < 28922):
            scrape_one_page(page)
            page = page + 1
    except:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print 'current page :' + str(page)

        # 遇到错误时随机休眠一段时间（IP跳跃的简易替代）
        rand = random.randint(3, 20)
        print 'sleep  ' + str(rand) + "seconds "
        time.sleep(rand)

        craw_all(page)

    finally:

        endtime = datetime.datetime.now()
        print 'Time :' + str((endtime - start_time).seconds) + 's'
