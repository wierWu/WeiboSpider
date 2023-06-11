#热门榜单
#!/usr/bin/env python3
# encoding: utf-8
"""
Author: wier.wj
Created Time: 2023/6/04
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.common import parse_user_info,parse_tweet_info,parse_time

class TopSpider(Spider):

    """
    周排行榜数据采集
    """
    name = "top"
    
    def start_requests(self):
        """
        入口-微博周榜单，爬取100w
        """
        for page in range(1,20000):
            url = f'https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_8698_-_ctg1_8698&luicode=20000174&page={page}'
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        statuses = data['data']['cards']
        for content_info in statuses:
            content_info = content_info['mblog']
            item = parse_tweet_info(content_info)
            mid = item['mid']
            yield item
            #获取最热门的10个评论
            comment_url =  f"https://weibo.com/ajax/statuses/buildComments?" \
                  f"is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=10"
            yield Request(comment_url, callback=self.parse_comment, meta={'tweet':item})  
        
    def parse_comment(self,resp):
        """
        评论解析
        """
        data = json.loads(resp.text)
        tweet = resp.meta['tweet']
        for comment in data['data']:
            item = {}
            item['mid'] = tweet['mid']
            item['type'] = 'comment'
            item['created_at'] = parse_time(comment['created_at'])
            item['id'] = comment['id']
            item['like_counts'] = comment['like_counts']
            if 'source' in comment:
                item['ip_location'] = comment['source']
            item['content'] = comment['text_raw']
            #微博内容
            item['tweet'] = tweet
            ##评论用户信息
            if 'user' in comment:
                item['comment_user'] = parse_user_info(comment['user'])
            yield item
        # item = comment_list
        # yield item