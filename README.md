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
