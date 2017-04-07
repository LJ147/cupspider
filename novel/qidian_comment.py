#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by LJ on 2017/3/25
import sys
import db_tool
import json
import mongoDB
import random
import requests
import time

reload(sys)
sys.setdefaultencoding("utf-8")


def store_comment(token, page, book_id):
    # book_id:1003354631  token:NZv1ty8GbjYLuCTm9PMpf7yONl12AgeFQ9BuDYBJ
    r = requests.get(
        "http://book.qidian.com/ajax/comment/info?_csrfToken={token}&pageIndex={index}&pageSize=15&orderBy= &bookId={book_id}".format(
            token=token, book_id=book_id, index=page))

    content = json.loads(r.content)

    content['book_id'] = book_id

    # 插入全部评论信息
    try:

        mongoDB.insert_comment(content)
    except:
        # 遇到错误时随机休眠一段时间（IP跳跃的简易替代）
        rand = random.randint(3, 20)
        print 'sleep  ' + str(rand) + "seconds "
        time.sleep(rand)
        store_comment(token, page + 1, book_id)

    try:
        comment_info_list = content['data']['commentInfo']

        for item in comment_info_list:
            comment = item.get("comment")
            if comment != u"":
                print str(item.get("nickName")) + " said :" + comment + " about book " + book_id
                # 仅插入有内容的评论信息
                item['book_id'] = book_id
                mongoDB.insert_comment_with_content(item)




    except:
        print "no comment"


def get_comment_amount(token, page, book_id):
    # book_id:1003354631  token:NZv1ty8GbjYLuCTm9PMpf7yONl12AgeFQ9BuDYBJ
    r = requests.get(
        "http://book.qidian.com/ajax/comment/info?_csrfToken={token}&pageIndex={index}&pageSize=15&orderBy= &bookId={book_id}".format(
            token=token, book_id=book_id, index=page))

    content = json.loads(r.content)

    try:
        count = content['data']['totalCnt']
    except:
        count = 0
    finally:
        return count


if __name__ == '__main__':

    page = 15
    page_size = 15

    select_amount = 100

    sql = "SELECT COUNT(url) FROM bookForQidian"
    url_count = int(db_tool.select_url(sql)[0].get('COUNT(url)'))
    # 数据库记录需大于100


    urls = db_tool.select_one_hundred()
    for url in urls:

        # get_token(url[0].decode('utf-8'))
        # book_id:1003354631  token:NZv1ty8GbjYLuCTm9PMpf7yONl12AgeFQ9BuDYBJ book.qidian.com/info/1000117983
        book_id = str(url[0][21:])

        comment_max = int(
            get_comment_amount(token="NZv1ty8GbjYLuCTm9PMpf7yONl12AgeFQ9BuDYBJ", page=page, book_id=book_id))
        page_count = comment_max / page_size

        page = 1
        while (page < page_count):
            store_comment(token="NZv1ty8GbjYLuCTm9PMpf7yONl12AgeFQ9BuDYBJ", page=page, book_id=book_id)
            page = page + 1

    print "url is less than 100 or all the conmmends haves been stored"
