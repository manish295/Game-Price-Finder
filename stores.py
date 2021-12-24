from bs4 import BeautifulSoup
import requests
import re
from config import *

class Stores:

    def __init__(self, game):
        self.game = game


    def steam(self):
        url = f"https://store.steampowered.com/search/?term={self.game}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        div = doc.find('div', attrs={'id': "search_resultsRows"})
        if div == None:
            return {"store": "Steam" ,"game":"Game not found/Does not exist in store.", "price": "Not Available", "image": "Not Found", "link": "Not Available"}
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
        return {"store": "Steam", "game":game_name.string, "price": price, "image": game_img, "link": game_link}
    
    def epic_games(self):
        url = f"https://www.epicgames.com/store/en-US/browse?q={self.game}&sortBy=relevancy&sortDir=DESC&count=40"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        game = doc.find('ul', attrs={'class': 'css-cnqlhg'})
        if game == None:
            return {"store":"Epic Games", "game":"Game not found/Does not exist in store.", "price": "Not Available", "image": "Not Found", "link": "Not Available"}
        else:
            game = game.findChildren('li')[0]
        game_link = "https://www.epicgames.com" + game.find("a", class_="css-1jx3eyg")['href']
        game_img_div = game.find("div", class_="css-f0xnhl")
        game_img = game_img_div.find("img")['data-image'].replace(" ","%20")
        game_info = game.find(class_="css-hkjq8i")
        game_name = game_info.find("div", attrs={'class': 'css-1h2ruwl'})
        price = game_info.find("span", class_="css-z3vg5b")
        if price == None:
            price = game_info.find(text=re.compile("\$.*"))

        return {"store": "Epic Games", "game":game_name.string, "price": price.string, "image": game_img, "link": game_link}


    def ubi_store(self):
        jsonRequestData = '{"requests":[{"indexName":"store_en-us", "query": "%s"}]}' % (self.game)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        response = requests.post(f"https://avcvysejs1-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.9.2)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.4.5)%3B%20react%20(16.8.3)%3B%20react-instantsearch%20(6.11.1)&x-algolia-api-key={ubi_store_key}&x-algolia-application-id=AVCVYSEJS1", headers=headers, data=jsonRequestData)
        json_reponse = response.json()
        if json_reponse["results"][0]["hits"] == []:
            return {"store":"Ubisoft Store", "game":"Game not found/Does not exist in store.", "price": "Not Available", "image": "Not Found", "link": "Not Available"}
        game_info = json_reponse["results"][0]["hits"][0]
        game_name = game_info["title"]
        game_type = game_info["Edition"]
        game_price = "$" + str(format(game_info["price"][0]["USD"], ".2f"))
        game_img = game_info["image_link"]
        game_link = game_info["linkWeb"]
                
        return {"store": "Ubisoft Store", "game": game_name + " " + game_type, "price": game_price, "image":game_img, "link": game_link}


    def green_man_gaming(self):
        jsonRequestData = '{"requests": [{"indexName": "prod_ProductSearch_US", "query": "%s"}]}' % (self.game)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        response = requests.post(f"https://sczizsp09z-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.5.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.8.3)%3B%20JS%20Helper%20(3.2.2)&x-algolia-api-key={green_key}&x-algolia-application-id=SCZIZSP09Z", headers=headers, data=jsonRequestData)
        if response.json()["results"][0]["hits"] == []:
            return {"store":"Green Man Gaming", "game":"Game not found/Does not exist in store.", "price": "Not Available", "image": "Not Found", "link": "Not Available"}
        game_info = response.json()["results"][0]["hits"][0]
        game_name = game_info["DisplayName"]
        game_price = "$" + str(format(game_info["Regions"]["US"]["Drp"], ".2f"))
        img_url = game_info["ImageUrl"]
        game_img = f"https://images.greenmangaming.com{img_url}"
        link_url = game_info["Url"]
        game_link = f"https://www.greenmangaming.com{link_url}"
        return {"store": "Green Man Gaming", "game":game_name, "price": game_price, "image": game_img, "link": game_link}

    def fanatical(self):
        jsonRequestData = '{"requests": [{"indexName": "fan", "query": "%s", "facetFilters": [["display_type:game"]]}], "apiKey": "%s"}' % (self.game, api_key)
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        response = requests.post("https://w2m9492ddv-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20react-instantsearch%204.5.2%3B%20JS%20Helper%20(2.28.1)&x-algolia-application-id=W2M9492DDV", headers=headers, data=jsonRequestData)
        if response.json()["results"][0]["hits"] == []:
            return {"store":"Fanatical", "game":"Game not found/Does not exist in store.", "price": "Not Available", "image": "Not Found", "link": "Not Available"}
        game_info = response.json()["results"][0]["hits"][0]
        game_name = game_info["name"]
        game_price = "$" + str(game_info["price"]["USD"])
        cover = game_info["cover"]
        game_img = f"https://fanatical.imgix.net/product/original/{cover}?auto=compress,format&w=1280&fit=crop&h=720&q=75"
        slug = game_info["slug"]
        game_url = f"https://www.fanatical.com/en/game/{slug}"
        return {"store": "Fanatical", "game":game_name, "price": game_price, "image": game_img, "link": game_url} 
    

    def gamesplanet(self):
        url = f"https://us.gamesplanet.com/search?query={self.game}"
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        games = soup.find("div", class_="row row-page-ctn")
        game_div = games.find("div").div
        game_img = game_div.find("img")["src"]
        game_link = game_div.find("a", class_="d-block text-decoration-none stretched-link")["href"]
        game_url = f"https://us.gamesplanet.com{game_link}"
        game_name = game_div.find("a", class_="d-block text-decoration-none stretched-link").string
        game_price = game_div.find("span", class_="price_current")

        return {"store": "GamesPlanet", "game":game_name, "price": game_price.string, "image": game_img, "link": game_url} 

    def gamersgate(self):
        response = requests.get(f"https://www.gamersgate.com/api/games/?query={self.game}+&dlc=on&sort=alphabetically&timestamp=1640368554888&need_change_browser_url=true")
        if response.json()["catalog"] == []:
            return {"store":"GamersGate", "game":"Game not found/Does not exist in store.", "price": "Not Available", "image": "Not Found", "link": "Not Available"}
        game_info = response.json()["catalog"][0]
        game_price = game_info["price"]
        game_url = "https://www.gamersgate.com/" + game_info["link"]
        game_img = game_info["image"]
        game_name = game_info["name"]
        return {"store": "GamersGate", "game": game_name, "price": game_price, "image": game_img, "link": game_url}
