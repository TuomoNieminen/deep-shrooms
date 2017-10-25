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

### Predicting

Note that the model expects inputs as 4d arrays: (None, 480, 480, 3). If you want to predict the probability of edibility of a single mushroom, pass 
the image to the model as a (1, 480, 480, 3) array. Also note that **the model has been trained using images where the pixes values have been rescaled to value between 0 and 1**. The model expects that all inputs are rescaled by a division by 255.

```
x = X_imgs[0]               # X_imgs contains images as (N, 480, 480, 3) array
x.shape = (1, ) + x.shape   # reshape x to (1, 480, 480, 3)
x = x / 255.0               # rescale

loaded_model.predict(x).round(3)
# array([[ 0.32712618]], dtype=float32)
```