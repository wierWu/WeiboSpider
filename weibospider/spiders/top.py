#热门榜单
#!/usr/bin/env python
# encoding: utf-8
"""
Author: wier.wj
Created Time: 2023/6/04
"""
import json
from scrapy import Spider
from scrapy.http import Request
from spiders.comment import parse_tweet_info,parse_time,parse_user_info

class TopSpider(Spider):
    
    def start_requests(self):
        """
        爬虫入口
        """
        for page in range(1,20000):
            url = f'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_8999_-_ctg1_8999_home&page={page}'
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        网页解析
        """
        data = json.loads(response.text)
        statuses = data['data']['statuses']
        for content_info in statuses:
            item = parse_tweet_info(content_info)
            mid = item['mid']
            yield item
            #获取最热门的10个评论
            comment_url =  f"https://weibo.com/ajax/statuses/buildComments?" \
                  f"is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count=10"
            yield Request(comment_url, callback=self.parse_comment, meta={'source_url': comment_url,'tweet_info':item})
           
            
            
        
        
    def parse_comment(self,resp):
        """
        评论解析
        """
        data = json.loads(resp.text)
        tweet_info = resp.meta['tweet_info']
        comment_list = []
        tweet_info['commentList'] = comment_list
        
        for comment in data['data']:
            item = dict()
            item['created_at'] = parse_time(comment['created_at'])
            item['id'] = comment['id']
            item['like_counts'] = comment['like_counts']
            item['ip_location'] = comment['source']
            item['content'] = comment['text_raw']
            comment_list.append(item)
        
        return comment_list