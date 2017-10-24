# deep-shrooms
Project for the Helsinki University course Introduction to Data Science

## Project website

[here](https://tuomonieminen.github.io/deep-shrooms)

To edit the content of the site, edit docs/index.Rmd markdown. Then ping Tuomo or use RStudio/knitr to update the .html.

## Scraper

To run the scraper to scrape the mushroom details and pictures from MushroomWorld you have to first install scrapy: `pip install scrapy`

Then go the to folder: `cd shroom_scrapers/`

And enter: `scrapy crawl mw_scraper`

### NOTE:

The images have been already downloaded and are downloaded inside the Jupyter notebook.

## Loading the trained model


Below is an example on how to load the keras model from a json file and then attach the trained weights to it.

```
from keras.models import model_from_json

json_file = open('models/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("models/weights.h5")
```

