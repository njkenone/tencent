# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class PositiontencentSpider(scrapy.Spider):
    name = 'positiontencent'
    allowed_domains = ['tencent.com']
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [url+str(offset)+"#a"]

    def parse(self, response):
        for each in response.xpath("//tr[@class='even']|//tr[@class='odd']"):
            item = TencentItem()
            item['positionName'] = each.xpath("./td[1]/a/text()").extract()[0]
            item['positionLink'] = each.xpath("./td[1]/a/@href").extract()[0]
            item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            item['positionNum'] = each.xpath("./td[3]/text()").extract()[0]
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]
            yield item
        if self.offset < 3300:
            self.offset += 10
        yield scrapy.Request(url=self.url+str(self.offset)+"#a", callback=self.parse)
