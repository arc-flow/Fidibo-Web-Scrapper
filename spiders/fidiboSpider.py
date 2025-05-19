import scrapy
import re

class FidiboSpider(scrapy.Spider):
    name = 'fidiboSpider'
    allowed_domains = ['fidibo.com']
    start_urls = ['https://fidibo.com/book/1']
            


    def parse(self, response):
        
        if response.status == 200:

            title = response.css("h1.book-main-box-detail-title::text").get()
            author = response.css("div.book-main-box-detail-author a.book-main-box-detail-author-name::text").get()
            if title and author is not None:
                yield {
                    'title': title,
                    'author': author
                }

        current_url = response.url
        match = re.search(r'book/(\d+)', current_url)

        if match:
                current_id = int(match.group(1))  
                next_id = current_id + 1
                next_url = f'https://fidibo.com/book/{next_id}'
                yield scrapy.Request(next_url, callback=self.parse, errback=self.handle_error)

    def handle_error(self, failure):
        
        self.log(f"Error while fetching next page: {failure.value}", level=scrapy.log.WARNING)
       
        