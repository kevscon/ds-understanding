import scrapy

# create spider class for scraping
class AliceSpider(scrapy.Spider):

    # name to call spider in terminal
    name = 'alice_spider'

    # set spider settings
    custom_settings = {
        "DOWNLOAD_DELAY": 3, # wait time between downloading pages
        "CONCURENT_REQUESTS_PER_DOMAIN": 3, # max concurrent requests
        "FEED_FORMAT": 'csv', # output file type
        "FEED_URI": 'alice_data.csv' # output file name
    }

    # initial webpages
    start_urls = [
        'http://www.alice-in-wonderland.net/resources/chapters-script/alices-adventures-in-wonderland/chapter-1/'
    ]

    # this initial function must be called "parse"
    # function to list webpages
    def parse(self, response):
        # iterate through webpage hyperlink elements
        for link in response.xpath('//ul[@class="sub-menu-ul"]/ul/li/a/@href').extract():
            # load each page and run "parse_webpage" function
            yield scrapy.Request(
                url=link, # url for request
                callback=self.parse_webpage, # function to be called
                meta={'url': link} # metadata
            )

    # function to retrieve data from each webpage
    def parse_webpage(self, response):
        # load webpage for scraping
        url = response.request.meta['url']
        # scrape elements
        title = response.xpath('//h1/text()').extract()[0]
        first_paragraph = response.xpath('//main/article/p/text()').extract()[0]

        # yield scraped data (to file)
        yield {
            'title': title,
            'paragraph': first_paragraph
        }
