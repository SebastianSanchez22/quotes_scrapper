import scrapy

# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    custom_settings = {
        'FEED_URI':'quotes.json',
        'FEED_FORMAT':'json',    
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        next_page_button_link = response.xpath('//li[@class="next"]/a/@href').get()
    
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
        else:
            yield {
                'quotes': quotes
            }


    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        yield {
            'title': title, 
            'top_ten_tags': top_ten_tags
        }

        next_page_button_link = response.xpath('//li[@class="next"]/a/@href').get()
        # Importante preguntar si la variable next_page_button_link contiene algo 
				# ya que por logica en algun momento llegariamos a ultima pagina.
        if next_page_button_link:
            # El metodo follow nos permite seguir al link (lo que hace scrapy es 
						# dejar la url absoluta y cambiar el resto) 
            # Este metodo posee un callback es decir un metodo que se ejecutara 
						# automaticamente despues de haber cambiado de url.
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})

   
