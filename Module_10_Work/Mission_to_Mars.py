
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


#Set up Splinter 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

#Convert the brower html to soup object and then quit browser. 
html = browser.html
news_soup = soup(html, 'html.parser')


slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and save it as `news_title`.  
#.get_text(). When this new method is chained onto .find(), only the text of the element is returned. 
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text. There will be many matches because there are many articles, each with a tag of <div /> and a class of article_teaser_body. 
#We want to pull the first one on the list, not a specific one, that is why we use .find instead of .find_all
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Images 


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
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL. adding the base URL to the scraped URL to connect to atual site. 
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ## Mars Facts 


#Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function.

#Create a dataframe for the table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
#By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item 
#in the list. Then, it turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

#Thankfully, Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function. 
#The result is a slightly confusing-looking set of HTML code—it's a <table /> element with a lot of nested elements.
df.to_html()


browser.quit()



