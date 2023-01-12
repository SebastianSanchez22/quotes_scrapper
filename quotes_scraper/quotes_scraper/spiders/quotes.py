import scrapy

# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //li[@class="next"]/a/@href

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    custom_settings = {
        'FEED_URI':'quotes.json',
        'FEED_FORMAT':'json',
        'FEED_EXPORT_ENCODING': 'utf-8' ,
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['sebastiansaor22@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'SebastianSanchez'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            kwargs['quotes'].extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        next_page_button_link = response.xpath('//li[@class="next"]/a/@href').get()
    
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs=kwargs)
        else:
            yield kwargs


    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]


        yield {
            'title': title, 
            'top_tags': top_tags
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

   
