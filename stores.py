from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
import os



class Stores:

    def __init__(self, game):
        self.game = game
        PATH = "C:\Program Files (x86)\geckodriver.exe"
        op = webdriver.FirefoxOptions()
        op.headless = True
        self.driver = webdriver.Firefox(executable_path=PATH, options=op, service_log_path=os.devnull)



    def steam(self):
        url = f"https://store.steampowered.com/search/?term={self.game}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        div = doc.find('div', attrs={'id': "search_resultsRows"})
        games = div.find('span', attrs={'class': 'title'})
        price_div = div.find('div',  attrs={'class': 'col search_price_discount_combined responsive_secondrow'})
        price_child = price_div.findChildren('div')[1]
        price = price_child.find_all(text=re.compile("\$.*"))
        if len(price) == 2:
            price = price[1].strip()
        elif len(price) == 1:
            price = price[0].strip()
        else:
            price = "Price not available"
        return games.string + ": " + price
    
    def epic_games(self):
        url = f"https://www.epicgames.com/store/en-US/browse?q={self.game}&sortBy=relevancy&sortDir=DESC&count=40"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        game = doc.find('ul', attrs={'class': 'css-cnqlhg'})
        if game == None:
            no_results = doc.find("div", class_="css-1dbkmxi")
            return no_results.span.string
        else:
            game = game.findChildren('li')[0]
        game_info = game.find(class_="css-hkjq8i")
        game_name = game_info.find("div", attrs={'class': 'css-1h2ruwl'})
        prices = game_info.find("div", attrs={"class": "css-fhxb3m"}).findChild('span', attrs={'class': 'css-1vm3ks'})
        prices = prices.find_all("div", attrs={'class': 'css-1x8w2lj'})
        if len(prices) == 2:
            price = prices[1].span
        else:
            price = prices[0].span
        
        return f"{game_name.string}: {price.string}"


    def ubi_store(self):
        self.driver.get("https://store.ubi.com/")
        search_box = self.driver.find_element_by_xpath("//input[@type='search']")
        search_box.send_keys(self.game)
        self.driver.implicitly_wait(4)
        html = self.driver.page_source
        doc = BeautifulSoup(html, "html.parser")
        games = doc.find("ul", id="search-result-items")
        game = games.find("li")
        game_name = game.find("div", class_="prod-title")
        game_price = game.find("span", class_="standard-price algolia-product-price")
        game_type = game.find("div", class_="card-subtitle")
        
        return f"{game_name.string} {game_type.string}: {game_price.string}"


    def humble_store(self):
        url = f"https://www.humblebundle.com/store/search?sort=bestselling&search={self.game}"
        self.driver.get(url)
        html = self.driver.page_source
        doc = BeautifulSoup(html, "html.parser")
        games_ul = doc.find("ul", attrs={"class": "entities-list js-entities-list no-style-list full js-full"})
        game = games_ul.find("li", class_="entity-block-container js-entity-container")
        game_name = game.find("span", class_="entity-title")
        game_price = game.find("span", class_="price")
        return f"{game_name.string}: {game_price.string}"

    def fanatical(self):
        url = f"https://www.fanatical.com/en/search?search={self.game}"
        self.driver.get(url)
        time.sleep(2)
        html = self.driver.page_source
        doc = BeautifulSoup(html, "html.parser")
        div = doc.find("div", class_="ais-Hits__root")
        game_card = div.find("div", class_="card-container col-6 col-sm-4 col-md-6 col-lg-4")
        game_href = game_card.find("a", class_="faux-block-link__overlay-link", href=True)
        game_url = f"https://www.fanatical.com{game_href['href']}"
        self.driver.get(game_url)
        time.sleep(2)
        game_page = self.driver.page_source
        soup = BeautifulSoup(game_page, "html.parser")
        game_div = soup.find("div", class_="product pt-4")
        game_name = game_div.find("h1", class_="product-name")
        game_price = game_div.find("div", class_="price").span
        return f"{game_name.string}: {game_price.string}"


 

    def shut_down(self):
        self.driver.quit()