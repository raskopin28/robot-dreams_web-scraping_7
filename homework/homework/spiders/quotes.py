import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    current_page = 1
    max_page = 2

    def parse(self, response):
        elements = response.xpath("//div[@class='quote']")
        for element in elements:
            yield {
                'text': element.xpath(".//span[@class='text']/text()").get(),
                'author': element.xpath(".//small[@class='author']/text()").get()
            }

        next_page = response.xpath("//ul/li[@class='next']/a/@href").get()
        if next_page is not None and self.current_page < self.max_page:
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse)
