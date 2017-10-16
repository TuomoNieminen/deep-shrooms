import scrapy

from mw_scraper.items import ImageItem, MushroomItem

TARGET_MUSHROOMS = [
  'Cantharellus cibarius',
  'Cantharellus tubaeformis',
  'Lactarius trivialis',
  'Albatrellus ovinus',
  'Boletus edulis',
  'Russula paludosa',
  'Lactarius deliciosus',
  'Lactarius deterrimus',
  'Agaricus arvensis',
  'Amanita muscaria',
  'Amanita virosa',
  'Amanita phalloides',
  'Galerina marginata',
  'Cortinarius rubellus',
  'Amanita regalis',
  'Amanita porphyria',
  'Hypholoma fasciculare',
  'Gyromitra esculenta'
]

class MWScraper(scrapy.Spider):
    name = 'mw_scraper'
    start_urls = ['http://www.mushroom.world/mushrooms/namelist']

    def parse(self, response):
        for div_item in response.css('div.item'):
            link = div_item.css('a')
            small = div_item.css('small')
            link_url = response.urljoin(link.css('::attr(href)').extract_first().strip())

            name_eng = small.css('::text').extract_first()
            # English name might be null
            name_eng_formatted = name_eng.strip()[1:-1] if name_eng is not None else ''
            shroom_dict = {
                'name_latin' : link.css('::text').extract_first(),
                'name_eng' : name_eng_formatted,
                'url_mw' : link_url,
            }
            yield response.follow(link_url, self.parse_show_page, meta={'shroom': shroom_dict})

    def parse_show_page(self, response):
        shroom = response.meta['shroom']

        img_urls = []
        for i, div_img in enumerate(response.css('div.image')):
            link = div_img.css('a')
            link_url = response.urljoin(link.css('::attr(href)').extract_first().strip())
            img_urls.append(link_url)
            latin_formatted = shroom['name_latin'].lower().replace(' ', '_')
            img_name = "{}{}.jpg".format(latin_formatted, i)
            yield ImageItem(name_latin=shroom['name_latin'], name_img=img_name, img_url=link_url)

        div_edibility = response.css('div.textus')[3]
        shroom['img_urls'] = img_urls
        shroom['edibility'] = div_edibility.css('::text').extract_first().lower()
        yield MushroomItem(shroom)
