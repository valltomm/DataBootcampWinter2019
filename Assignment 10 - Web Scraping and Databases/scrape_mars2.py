#!/usr/bin/env python
# coding: utf-8

# ## NASA Mars News

# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[1]:


from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from splinter import Browser
import requests 
import time
from selenium import webdriver


## return all functions

# In[2]:

def scrape():
    executable_path = {"executable_path": "chromedriver"}
    browser= Browser("chrome", **executable_path, headless=False)
    title, paragraph = mars_news(browser)


    # create dictionary with each function to run
    data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": marsHemispheres(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts()
    }

    browser.quit()
    return data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/" 
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    title = soup.find("div", class_="content_title").text
    paragraph = soup.find("div", class_="rollover_description_inner").text

    print(f"Latest Title: {title}")
    print(f"Latest Paragraph Text: {paragraph}")

    return title, paragraph

# ## JPL Mars Space Images - Featured Image

# Visit the url for JPL Featured Space Image here. https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
# 
# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
# Make sure to find the image url to the full size .jpg image.
# Make sure to save a complete url string for this image.

# In[68]:

def featured_image(browser):
    executable_path = {"executable_path": "chromedriver"}
    browser= Browser("chrome", **executable_path, headless=False)

    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url1)

    html = browser.html
    soup = bs(html, "html.parser")

    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    img_url = new_soup.find('img', class_='main_image')
    src_img_url = img_url.get('src')

    featured_image_url = "https://www.jpl.nasa.gov" + src_img_url

    # print(featured_image)
    return featured_image_url


# ## Mars Weather

# Visit the Mars Weather twitter account here (https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

# In[22]:

def mars_weather(browser):
    tw_url = "https://twitter.com/marswxreport?lang=en/" 
    tw_response = requests.get(tw_url)

    soup = bs(tw_response.text, 'html.parser')

    tweet = soup.find_all('div', class_="js-tweet-text-container")

    mars_weather = tweet[0].text
    print(mars_weather)
    return mars_weather


# ## Mars Facts

# Visit the Mars Facts webpage here (https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.

# In[34]:

def mars_facts():

    Mfacts_url = "https://space-facts.com/mars/"
    Mfacts_response= requests.get(Mfacts_url)

    table = pd.read_html(Mfacts_response.text)

    table


    # In[36]:


    Mfacts_df = table[0]
    Mfacts_df.columns = ["Feature", "Value"]
    Mfacts_df.set_index("Feature", inplace=True)
    Mfacts_df


    # In[39]:


    Mfacts_html = Mfacts_df.to_html()
    Mfacts_html = Mfacts_html.replace("\n", "")
    Mfacts_html

    return Mfacts_df.to_html(classes="table table-striped")


# ## Mars Hemispheres

# Visit the USGS Astrogeology site here (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# In[52]:


def marsHemispheres(browser):
 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hem_response= requests.get(hemispheres_url)
    soup = bs(hem_response.text, 'html.parser')

    
    # browser.visit(hemispheres_url)

    # HTML Object
    #html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    #soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemispheres_list = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemispheres_list.append({"title" : title, "img_url" : img_url})
        
    return hemispheres_list

print(scrape())