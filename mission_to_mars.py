# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # NASA URL PAGE
    url = 'https://mars.nasa.gov/news/'
    browser = webdriver.Chrome()
    browser.get(url)

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Results for only TITLES
    resultsTitle = soup.find_all('div', class_="content_title")

    # Looping through TITLES 
    Titles = []
    for result in resultsTitle:
        # Error handling
        try:
            # Identify and return title of listing
            title = result.find('a').text
            Titles.append(title)
        except AttributeError as e:
            print(e)

    # Results for DESCRIPTIONS
    soupDesc = BeautifulSoup(browser.page_source, "html.parser")
    #descriptions = soupPara.find_all('div', class_='article_teaser_body')
    resultDesc = soupDesc.select(".article_teaser_body")


    # Looping through DESCRIPTIONS 
    Descriptions = []
    for result in resultDesc:
        # Error handling
        try:
            # Identify and return title of listing
            Descriptions.append(result.text)
            #Titles.append(title)
        except AttributeError as e:
            print(e)

    #JPL MARS SPACE IMAGES
    urlImages = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = webdriver.Chrome()
    browser.get(urlImages)
    
    # Results for IMAGES
    soupImage = BeautifulSoup(browser.page_source, "html.parser")
    resultImage = soupImage.select(".carousel_items")

    for result in resultImage:
        # Error handling
        try:
            # Identify and return title of listing
            image = result.select("article")
            #print(image)
            for img in image:
                featured_image_url = "https://www.jpl.nasa.gov" + img["style"].split("'")[1]
                #Images.append("https://www.jpl.nasa.gov" + img["src"])
                #print(img["src"])
            #Descriptions.append(result.text)
        except AttributeError as e:
            print(e)
    
    # MARS WEATHER
    #Twitter page
    urlTwitter = 'https://twitter.com/marswxreport?lang=en'
    browser = webdriver.Chrome()
    browser.get(urlTwitter)
    
    # Results for TWEETS
    soupTweets = BeautifulSoup(browser.page_source, "html.parser")
    resultTweets = soupTweets.select(".js-tweet-text-container")
    
    # Looping through TWEETS
    latestTweet = resultTweets[0].select("p")
    for tw in latestTweet:
        mars_weather = tw.text
        
    # MARS FACTS
    urlFacts = 'https://space-facts.com/mars/'
    #Get Table
    marsTable = pd.read_html(urlFacts)
    #Convert to HTML Table string
    marsTable_df = marsTable[0]
    mars_html_table = marsTable_df.to_html()

    # MARS HEMISPHERES
    #Hemispheres page
    urlHemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = webdriver.Chrome()
    browser.get(urlHemi)
    
    # Results for HEMISPHERES
    soupHemi = BeautifulSoup(browser.page_source, "html.parser")
    resultHemi = soupHemi.select(".description")

    hemisphere_image_urls = { "data":[]}

    for result in resultHemi:
        # Error handling
        try:
            data = {}
            test = result.select("h3")
            for ts in test:
                data["title"] = ts.text
            link = result.select('a')
            for lk in link:
                fullImgURL = "https://astrogeology.usgs.gov" + lk["href"]
                browser = webdriver.Chrome()
                browser.get(fullImgURL)
                # Results for HEMISPHERES
                soupfullImg = BeautifulSoup(browser.page_source, "html.parser")
                resultfullImg = soupfullImg.select(".downloads")
                for full in resultfullImg:
                    imgJPG = full.select("li")
                    final = imgJPG[0].select("a")
                    for fn in final:
                        data["img_url"] = fn["href"]
                        #print(fn["href"])
                #print(fullImgURL)
            #data["title"] = result["alt"]
            #data["img_url"] = result["src"]
            hemisphere_image_urls["data"].append(data)
            #print(result["alt"])

        except AttributeError as e:
            print(e)
            
    # Storing in JSON DICTIONARY
    mars = {}
    #Mars News Titles
    mars["Mars_News_Titles"] = Titles
    mars["Mars_Descriptions"] = Descriptions
    mars["Featured_Space_Image"] = featured_image_url
    mars["Latest_Mars_Weather_Tweet"] = mars_weather
    mars["Mars_Facts_HTML_Table"] = mars_html_table
    mars["Hemisphere_Image_URLS"] = hemisphere_image_urls
    
    return mars