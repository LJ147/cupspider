#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by LJ on 2017/4/14
# 获取起点全部小说的基本信息(url 推荐票数等)，存入数据库
import random
import sys
import db_tool
import web_tool
import time

reload(sys)
sys.setdefaultencoding("utf-8")
import datetime

TOTAL_PAGE = 20000


# 爬取、解析并存储单一页面的小说信息（mysql）
def scrape_one_page(page):
    # 排序方式为总推荐票数
    # url = 'http://a.qidian.com/?size=-1&sign=-1&tag=-1&chanId=-1&subCateId=-1&orderId=2&update=-1&page={page}&month=-1&style=1&action=-1&vip=-1'.format(
    #     page=page)

    url = 'http://www.jjwxc.net/bookbase_slave.php?booktype=&opt=&page={page}&endstr=&orderstr=4'.format(page = page)
    soup = web_tool.getSoup(url)
    items = soup.find_all('tr', onmouseover="this.bgColor = '#ffffff';")
    items = soup.find_all()
    # items2 = soup.find_all('tr', class_='bg2')

    # items = soup.find_all('div', class_='book-mid-info')

    print "current page : " + str(page)

    for item in items:
        if item.a != None:
            title = str(item.find('td', class_='td6').text)
            book_url = item.find('td', class_='td4').a['href']

            # # 解析界面元素
            # title = item.a.text
            # book_url = item.a.get('href')[2:]
            # update = item.find('p', class_='update')
            # lists = update.split('\n', -1)
            # count = lists[0][:-1]
            # vote_ticket = lists[1][1:-3]
            # count = parse_str_number(count)
            # vote_ticket = parse_str_number(vote_ticket)
            # details = item.p.text
            # author = details.split('|')[0].replace('\n', '')
            # types = details.split('|')[1]
            # type_one = types.split('·')[0]
            # type_two = types.split('·')[1]
            # status = details.split('|')[2].replace('\n', '')
            insert = "insert into book_url_17k(url ,title) VALUES (%s,%s)"

            param = (book_url, title)

            # insert = "insert into bookForQidian(title,url,author,typeOne,typeTwo,numberOfWords,recommend,status) values(%s,%s,%s,%s,%s,%s,%s,%s)"
            # 分别为小说标题、url、作者、两种分类、总字数、总推荐票数、状态
            # param = (title, book_url, author, type_one, type_two, count, vote_ticket, status)
            # 插入状态
            status = db_tool.execute_sql(insert, param)
            if status == 0:
                print '-----插入成功--------'
                print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print "book_name: " + title
                # print "author: " + author
                print '--------------------'
            else:
                print '-----插入失败--------'


        else:
            print "no data inside!"


# 递归调用
def craw_all(page):
    try:
        while (page < TOTAL_PAGE):
            scrape_one_page(page)
            page = page + 1
    # 某一页面出现错误时，页码page加一，跳过该页继续爬取
    except:
        page = page + 1
        craw_all(page)


if __name__ == '__main__':
    # drop = "DROP TABLE IF EXISTS book_url_17k"
    param = ()

    # db_tool.execute_sql(drop,param)

    sql = "CREATE TABLE book_url_jinjiang (url  VARCHAR (250) NOT NULL PRIMARY KEY,title  VARCHAR(250))"

    db_tool.execute_sql(sql, param)

    start_time = datetime.datetime.now()
    # 初始page
    page = 1
    try:
        while (page < TOTAL_PAGE):
            scrape_one_page(page)
            page = page + 1
    except:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print 'current page :' + str(page)

        # 遇到错误时随机休眠一段时间（IP跳跃的简易替代）
        rand = random.randint(3, 10)
        print 'sleep  ' + str(rand) + "seconds "
        time.sleep(rand)

        craw_all(page)

    finally:

        endtime = datetime.datetime.now()
        print 'Time :' + str((endtime - start_time).seconds) + 's'
