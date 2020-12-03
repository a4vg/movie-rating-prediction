# scrapy runspider MoviesSpider.py -a urls_file=../../raw-data/movies_names.csv -o movies.csv -t csv

from scrapy import Spider, Request
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
                errback=self.handle_404, 
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

    def handle_404(self, failure):
        with open("404_responses.csv", "a") as f:
            movie_id = failure.request.cb_kwargs["movie_id"]
            url = failure.request.url
            f.write(f"{movie_id},{url}\n")

































