import requests
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
from urllib.parse import urlparse

class RecipeScraping():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        
    def excute(self, url, urls_file="urls.txt", output="recipes.csv"):
        print("start : recipe screping")
        # recipe_df = pd.DataFrame(
        #     columns=["id", "recipe_name", "recipe_ingredient", "servings"
        #              "cooking_time", "expense", "url"]
        # )
        with open(urls_file, "r", encoding="utf-8") as f:
            urls = f.read().split("\n")[:-1]
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        num_recipes = str(len(urls))
        print(f"number of recipes : {num_recipes}")
        for i, recipe_url in enumerate(urls, 1):
            print(str(i)+' / '+num_recipes)
            print(base_url+recipe_url)
            recipe_json = self.get_page_info(i, base_url+recipe_url)
            # if not recipe_json:
            #     continue
            # id = len(recipe_df) + 1
            # new_row = {
            #     "id": id,
            #     "recipe_name": recipe_json["name"],
            #     "recipe_ingredient": recipe_json["recipeIngredient"],
            #     "servings": recipe_json["recipeYield"].split()[0],
            #     "cooking_time": recipe_json["totalTime"],
            #     "expense": recipe_json["expense"],
            #     "url": recipe_json["mainEntityOfPage"]["@id"],
            # }
            # recipe_df = pd.concat([recipe_df, pd.DataFrame([new_row])], ignore_index=True)
        # recipe_df.to_csv(output, index=False)
            

    def get_html(self, url, params=None, headrs=None):
        try:
            resp = requests.get(url, params=params, headers=headrs)
            resp.encoding = 'utf-8'

            soup = BeautifulSoup(resp.text, "html.parser")
            return soup
        except Exception as e:
            print(e)
            return None
        
    def get_urls(self, url, output="urls.txt"):
        print("start : get_urls")
        params = {}
        headers= {"User-Agent": self.user_agent}
        soup = self.get_html(url, params, headers)
        
        urls = []
        result = soup.find("span", {"class":"DlyPagination-text--total"})
        match = re.search(r'(\d+)', result.text)
        if not match:
            assert "error: not found total pages"    
        total_pages = match.group(1)
            
            
        scripts = soup.find_all('a', {"class":'DlyLink title'})
        urls.extend([a['href'] for a in scripts])
        num_urls = str(total_pages)
        print("1 / "+num_urls)
        for i in range(2, int(total_pages)+1):
            print(str(i)+' / '+num_urls)
            next_page = url +"?page="+str(i)
            soup = self.get_html(next_page, params, headers)
            scripts = soup.find_all('a', {"class":'DlyLink title'})
            urls.extend([a['href'] for a in scripts])
        with open(output, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(f"{url}\n")
    
    def get_page_info(self, idx, url):
        params = {}
        headers = {"User-Agent": self.user_agent}
        soup = self.get_html(url, params, headers)
        # print(soup)
        # return
        script_tag = soup.find("script", string=lambda x: x and "window.__delyKurashiruEnvironment.ssrContext" in x)
        # print(script_tag)
        # script_tag = soup.find("script", text=lambda x: "window.__delyKurashiruEnvironment.ssrContext" in x)
        
        if script_tag:
            # JavaScriptコードの中身を文字列として取得
            script_content = script_tag.string

            # JSONデータ部分を抽出
            start_index = script_content.find('{"path"')
            end_index = script_content.rfind("}") + 1
            json_data_str = script_content[start_index:end_index]

            # JSON文字列を辞書型に変換
            ssr_context = json.loads(json_data_str) 
            # print(ssr_context)
        else:
            print("該当するスクリプトが見つかりませんでした。")
        # ファイルにJSONデータを書き込む
        with open("resource/"+str(idx)+".json", "w", encoding="utf-8") as file:
            json.dump(ssr_context["state"]["fetchVideo"]["data"]["data"], file, ensure_ascii=False, indent=4)
        # scripts = soup.find_all("script", {"type":"application/ld+json"})   
        # recipe_data = {}

        # for script in scripts:
        #     try:
        #         json_data = json.loads(script.string)
        #         if "@type" in json_data and json_data["@type"] == "Recipe":
        #             recipe_data = json_data
        #             break
        #     except json.JSONDecodeError:
        #         continue  # JSONが無効ならスキップ
            
        # expense = soup.find("span", {"class":"RecipeDetail-metadataItemValueYen"})
        # if not expense:
        #     return None

        # recipe_data["expense"] = expense.text.strip()
        # return recipe_data
    
    def get_text_by_elem(self, elem):
        try:
            text = elem.text
            text = text.strip()
            return text
        except Exception as e:
            return None
    
if __name__ == '__main__':
    # url = "https://www.kurashiru.com/recipes/6a05509c-e9ba-4286-99fe-44eb7f8b0323"
    # url = "https://www.kurashiru.com/recipes/ec28c79c-07ff-4e3e-b011-be628982eec3"
    # url = "https://www.kurashiru.com/video_categories/139"
    # url = 'https://www.kurashiru.com/recipes/e3fd1786-3931-4324-81a6-1f1f5b02ed55'
    # url = "https://www.kurashiru.com/recipes/835cabd1-d8cb-49e4-82e2-86422971a534"
    url = "https://www.kurashiru.com/recipes/3e020702-6099-43ee-a777-b430983c39d6"
    sr = RecipeScraping()
    # sr.get_urls(url)
    sr.excute(url)
    # sr.get_page_info(url)
