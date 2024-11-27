import requests
import re
from bs4 import BeautifulSoup
import json

class Scraping():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    def get_html(self, url, params=None, headrs=None):
        try:
            resp = requests.get(url, params=params, headers=headrs)
            resp.encoding = 'utf-8'

            soup = BeautifulSoup(resp.text, "html.parser")
            return soup
        except Exception as e:
            print(e)
            return None
    
    def get_page_info(self, url):
        result = {}
        params = {}
        headers = {"User-Agent": self.user_agent}
        soup = self.get_html(url, params, headers)
        # print(soup)
        scripts = soup.find_all("script", {"type":"application/ld+json"})
        # return scripts
        # 'type'のみを含むスクリプトを格納するリスト
        
        recipe_data = {}

        for script in scripts:
            try:
                json_data = json.loads(script.string)
                if "@type" in json_data and json_data["@type"] == "Recipe":
                    recipe_data = json_data
                    break
            except json.JSONDecodeError:
                continue  # JSONが無効ならスキップ

        cooking_time_tag = soup.find("p", {"class", "cooking-time"})
        cooking_time = cooking_time_tag.get_text(strip=True) if cooking_time_tag else "調理時間が見つかりませんでした"
        recipe_data["cokking_time"] = cooking_time

        expense_tag = soup.find("p", {"class": "expense"})
        expense = expense_tag.get_text(strip=True) if expense_tag else "費用目安が見つかりませんでした"
        recipe_data["expense"] = expense
                
        return recipe_data
    
    def get_text_by_elem(self, elem):
        try:
            text = elem.text
            text = text.strip()
            return text
        except Exception as e:
            return None
    
if __name__ == '__main__':
    url = "https://www.kurashiru.com/recipes/6a05509c-e9ba-4286-99fe-44eb7f8b0323"
    url = "https://www.kurashiru.com/recipes/ec28c79c-07ff-4e3e-b011-be628982eec3"
    sr = Scraping()
    result = sr.get_page_info(url)
    with open("result.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)
    # print(result)
