import json
import scrapy


class MerchSpider(scrapy.Spider):
    name = "items"
    start_urls = [
        "https://www.6pm.com/coach-bags/COjWAVIC-B3iAgIBCg.zso?s=isNew%2Fdesc%2FgoLiveDate%2Fdesc%2FrecentSalesStyle%2Fdesc%2F"
    ]

    def parse(self, response):
        for item in response.css('article.ob '):
            yield {
                "item": item.css('p.Fb::text').get(),
                "brand": item.xpath(
                    '//*[@id="searchPage"]/div/article[1]/div/p[1]/span/text()').get(),
                "price": item.css('span.Ob::text').get(),
                "MSRP": item.css('span.Cb::text').get(),
                "link": f"https://www.6pm.com{item.css('a').attrib['href']}",
            }

        next_page = response.css('a.ux::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = [
        "https://www.amazon.com/s?i=specialty-aps&srs=13575748011&page=2&qid=1583756045&ref=lp_13575748011_pg_2"
    ]

    def parse(self, response):
        for item in response.css(
                'div[class="sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"]'):
            yield {
                "item": item.css(
                    'span[class="a-size-medium a-color-base a-text-normal"]::text').get(),
                "ASIN": item.css('div::attr(data-asin)').get(),
                "price": item.css('span[class="a-offscreen"]::text').get(),
                "original price": item.css('span[aria-hidden="true"]::text').get(),
                "reviews": item.css('span[class="a-size-base"]::text').get(),
                "rating": item.css('span[class="a-icon-alt"]::text').get(),
                "link": f"https://www.amazon.com{item.css('a::attr(href)').get()}",
            }

        next_page = response.css('li[class="a-last"]').css('a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


with open('amazon.json') as f:
    data = json.load(f)

    with open('amazon.json', 'w') as f:
        json.dump(data, f, indent=4)
