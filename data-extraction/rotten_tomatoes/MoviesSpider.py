from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from time import sleep
from random import random
import urls

class MoviesSpider(Spider):
    name = "movies"

    def __init__(self, urls_file, *args, **kwargs):
        self.urls_file = urls_file

    def start_requests(self):
        m_urls, movie_ids = urls.get_urls(self.urls_file)

        if not m_urls:
            raise Exception("No movies available")

        for url,movie_id in zip(m_urls, movie_ids):
            yield Request(
                url=url,
                cb_kwargs={'movie_id': movie_id},
                errback=self.handle_failure, 
            )

    def parse(self, response, movie_id):
        '''
        Tomatometer:
        #a.tomato_meter_link span.mop-ratings-wrap__percentage <-- inner text

        Xpath: //a[@id="tomato_meter_link"]
                    //span[@class="mop-ratings-wrap__percentage"]
                        /text() <-- 1ra ocurrencia

        Audience score:
        div.audience-score span.mop-ratings-wrap__percentage <-- inner text

        Xpath: //div[contains(@class, "audience-score")]
                    //span[@class="mop-ratings-wrap__percentage"]
                        /text() <-- 1ra ocurrencia
        '''
        tomatometer = None
        audience_score = None
        if response.status == 200:
            tomatometer_xpath = '//a[@id="tomato_meter_link"]//span[@class="mop-ratings-wrap__percentage"]/text()'
            tomatometer = response.xpath(tomatometer_xpath).extract_first()

            audience_score_xpath = '//div[contains(@class, "audience-score")]//span[@class="mop-ratings-wrap__percentage"]/text()'
            audience_score = response.xpath(audience_score_xpath).extract_first()

        # Tomatometer and audience_score will 
        yield {
            "movie_id": movie_id, # from movielens
            "tomatometer": tomatometer.strip() if tomatometer else None, 
            "audience_score": audience_score.strip() if audience_score else None
        }

    def handle_failure(self, failure):
        url = failure.request.url
        status = failure.value.response.status
        movie_id = failure.request.cb_kwargs["movie_id"]
        
        if status == 403:
            sleep(2*random()) # [0, 2] s
            yield Request(
                url=url,
                callback=self.parse,
                cb_kwargs={'movie_id': movie_id},
                errback=self.handle_failure, 
            )

        elif status == 404:
            with open("404_responses.csv", "a") as f:
                f.write(f"{movie_id},{url}\n")

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "rotten_movies.csv": {"format": "csv"},
        },
    })
    process.crawl(MoviesSpider, urls_file="../../raw-data/movies_names.csv")
    process.start()


























