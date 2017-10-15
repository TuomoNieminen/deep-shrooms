# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from mw_scraper.items import ImageItem, MushroomItem
  
class MWScraperImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, ImageItem):
            yield scrapy.Request(item['img_url'], meta={'image_name': item['name_img']})
        else:
            return item

    def file_path(self, request, response=None, info=None):
        return request.meta['image_name']

    def item_completed(self, results, item, info):
        if isinstance(item, ImageItem):
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            # Only a single downloaded item in the image_paths -list
            item['file_path'] = "{}{}".format('mushroom_img/', image_paths[0])
            return item
        else:
            return item

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file_classes = open('mushroom_classes.json', 'w')
        self.file_imgs = open('mushroom_imgs.json', 'w')

    def close_spider(self, spider):
        self.file_classes.close()
        self.file_imgs.close()

    def process_item(self, item, spider):
        if isinstance(item, MushroomItem):
            print(dict(item))
            line = json.dumps(dict(item)) + "\n"
            self.file_classes.write(line)
            return item
        if isinstance(item, ImageItem):
            print(dict(item))
            line = json.dumps(dict(item)) + "\n"
            self.file_imgs.write(line)
            return item