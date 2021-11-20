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
        self.driver = webdriver.Firefox(executable_path=PATH, service_log_path=os.devnull, options=op)



    def steam(self):
        url = f"https://store.steampowered.com/search/?term={self.game}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        div = doc.find('div', attrs={'id': "search_resultsRows"})
        if div == None:
            return {None: None}
        game = div.find('a')
        game_link = game['href']
        game_img_url = requests.get(game_link).text
        img_soup = BeautifulSoup(game_img_url, "html.parser")
        game_img_div = img_soup.find("div", id="gameHeaderImageCtn")
        game_img = game_img_div.find("img")["src"]
        game_name = game.find("span", class_="title")
        price_div = div.find('div',  attrs={'class': 'col search_price_discount_combined responsive_secondrow'})
        price_child = price_div.findChildren('div')[1]
        price = price_child.find_all(text=re.compile("\$.*"))
        if len(price) == 2:
            price = price[1].strip()
        elif len(price) == 1:
            price = price[0].strip()
        else:
            price = None
        return {"game":game_name.string, "price": price, "image": game_img, "link": game_link}
    
    def epic_games(self):
        url = f"https://www.epicgames.com/store/en-US/browse?q={self.game}&sortBy=relevancy&sortDir=DESC&count=40"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        game = doc.find('ul', attrs={'class': 'css-cnqlhg'})
        if game == None:
            return {None: None}
        else:
            game = game.findChildren('li')[0]
        game_link = "https://www.epicgames.com" + game.find("a", class_="css-1jx3eyg")['href']
        game_img_div = game.find("div", class_="css-f0xnhl")
        game_img = game_img_div.find("img")['data-image'].replace(" ","%20")
        game_info = game.find(class_="css-hkjq8i")
        game_name = game_info.find("div", attrs={'class': 'css-1h2ruwl'})
        price = game_info.find(text=re.compile("\$.*"))

        return {"game":game_name.string, "price": price.string, "image": game_img, "link": game_link}


    def ubi_store(self):
        self.driver.get("https://store.ubi.com/")
        self.driver.implicitly_wait(5)
        search_box = self.driver.find_element_by_xpath("//input[@type='search']")
        search_box.send_keys(self.game)
        time.sleep(1)
        self.driver.get_screenshot_as_file("Screenshots/ubistore.png")
        html = self.driver.page_source
        doc = BeautifulSoup(html, "html.parser")
        games = doc.find("ul", id="search-result-items")
        game = games.find("li")
        if game == None:
            return {None: None}
        game_link = game.find("a")["href"]
        game_img = game.find("img")['src']
        game_name = game.find("div", class_="prod-title")
        game_price = game.find(text=re.compile("\$.*"))
        game_type = game.find("div", class_="card-subtitle")
        
        return {"game":game_name.string+" "+game_type.string, "price": game_price.string, "image":game_img, "link": game_link}


    def humble_store(self):
        url = f"https://www.humblebundle.com/store/search?sort=bestselling&search={self.game}&platform=windows"
        self.driver.get(url)
        self.driver.get_screenshot_as_file("Screenshots/humblestore.png")
        html = self.driver.page_source
        doc = BeautifulSoup(html, "html.parser")
        games_ul = doc.find("ul", attrs={"class": "entities-list js-entities-list no-style-list full js-full"})
        game = games_ul.find("li", class_="entity-block-container js-entity-container")
        if game == None:
            return {None: None}
        game_link = "https://www.humblebundle.com" + game.find("a")["href"]
        game_img = game.find("img")['src']
        game_name = game.find("span", class_="entity-title")
        game_price = game.find("span", class_="price")
        return {"game":game_name.string, "price": game_price.string, "image": game_img, "link": game_link}

    def fanatical(self):
        url = f"https://www.fanatical.com/en/search?search={self.game}&sortBy=fan&types=game"
        self.driver.get(url)
        time.sleep(2)
        self.driver.get_screenshot_as_file("Screenshots/fanatical1.png")
        html = self.driver.page_source
        doc = BeautifulSoup(html, "html.parser")
        div = doc.find("div", class_="ais-Hits__root")
        game_card = div.find("div", class_="card-container col-6 col-sm-4 col-md-6 col-lg-4")
        if game_card == None:
            return {None: None}
        game_link = game_card.find("a", class_="faux-block-link__overlay-link", href=True)["href"]
        game_url = f"https://www.fanatical.com{game_link}"
        self.driver.get(game_url)
        time.sleep(2)
        self.driver.get_screenshot_as_file("Screenshots/fanatical2.png")
        game_page = self.driver.page_source
        soup = BeautifulSoup(game_page, "html.parser")
        game_div = soup.find("div", class_="product pt-4")
        img_div = game_div.find("div", class_="responsive-image-island product-cover-container standard-cover")
        game_img = img_div.find("img")['src']
        game_name = game_div.find("h1", class_="product-name")
        game_price = game_div.find("div", class_="price").span
        return {"game":game_name.string, "price": game_price.string, "image": game_img, "link": game_url}

 

    def shut_down(self):
        self.driver.quit()