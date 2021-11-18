# from flask import Flask, render_template, redirect, url_for
# from flask_pymongo import PyMongo
# import scraping

# app = Flask(__name__)

# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

# @app.route("/")
# def index():
#    mars = mongo.db.mars.find_one()
#    return render_template("index.html", mars=mars)


# @app.route("/scrape")   
# def scrape():
#    mars = mongo.db.mars
#    mars_data = scraping.scrape_all()
#    mars.update({}, mars_data, upsert=True)
#    return redirect('/', code=302)

# if __name__ == "__main__":
#    app.run()

# from flask import Flask, render_template, redirect, url_for
# from flask_pymongo import PyMongo
# # from import scraping
# import datetime as dt

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # When scraping, the "headless" browsing session is when a browser is run without the users seeing it at all. 
    #While we can see the word "browser" here twice, one is the name of the variable passed into the 
    # function and the other is the name of a parameter. 
    # Coding guidelines do not require that these match, even though they do in our current code.

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    #This dictionary does two things: It runs all of the functions we've created—featured_image(browser),
    #  for example—and it also stores all of the results. 
    #We're also adding the date the code was run last by adding "last_modified": dt.datetime.now(). 
    
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
   # Visit URL
   url = 'https://spaceimages-mars.com'
   browser.visit(url)

# Find and click the full image button
   full_image_elem = browser.find_by_tag('button')[1]
   full_image_elem.click()

# Parse the resulting html with soup
   html = browser.html
   img_soup = soup(html, 'html.parser')

# Find the relative image url. An img tag is nested within this HTML, so we've included it.
#.get('src') pulls the link to the image.
#What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image.
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags.
   
   #ADD TRY/EXCEPT FOR ERROR HANDLING
   try:
      # Find the relative image url. 
      img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

   except AttributeError:
      return None

# Use the base URL to create an absolute URL. adding the base URL to the scraped URL to connect to atual site. 
   img_url = f'https://spaceimages-mars.com/{img_url_rel}'

   return img_url


def mars_facts():

   try: 
      # use 'read_html' to scrape the facts table into a dataFarme 
      df = pd.read_html('https://galaxyfacts-mars.com')[0]

   except BaseException: 
      return None

   df.columns=['description', 'Mars', 'Earth']
   df.set_index('description', inplace=True)
   
   #Convert dataFrame tinto html format, add bootstrap 
   return df.to_html()


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

