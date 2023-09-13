import scrapy


class AlgerSpider(scrapy.Spider):
    name = "bejaia"
    allowed_domains = ["www.tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Restaurants-g1903178-Bejaia_Bejaia_Province.html"]

    def parse(self, response):
        links= response.css('div.RfBGI a::attr(href)')
        for link in links :

            yield response.follow(link,callback=self.scrap_add)


        next_page=response.css('.primary::attr(href)').get()   
        if next_page is not None :
            yield response.follow(next_page,callback=self.parse)

    def scrap_add(self,response):
        restaurant_info={
        'name':response.css('.HjBfq::text').get(),
       'note':response.css('span.DsyBj svg::attr(aria-label)').get(),
       'reviews': [],
        }

        reviews=response.css('.review-container')
        for review in reviews:

           review_info = {
            'text':review.css('.partial_entry::text').get(),
           'stars':review.css('span.ui_bubble_rating::attr(class)').get(),
            'date':review.css('span.ratingDate::attr(title)').get(),
            }
           restaurant_info['reviews'].append(review_info)

        yield restaurant_info

        next_page=response.css('.primary::attr(href)').get()    
        if next_page is not None :
            yield response.follow(next_page,callback=self.scrap_add)


      



