import pandas as pd
import requests
import json
from pathlib import Path


class RecipeProcessor():
    def __init__(self):
        self.save_file = ''
        self.terms = {
            'vegetables': None,
            'seafood': None,
            'meat': None,
            'dairyProducts': None,
            'soybeans': None,
            'others': None,
            'cost': None,
            'cookTime': None
        }
        self.keys = ['recipeName', 'cookTime', 'cost', 'url', 'ingredients']
        self.recipes_file = "recipe_data/recipe.csv"

    def save_recipes_to_buffer(self, params):
        is_parameters_set = False
        for key in self.terms.keys():
            if key in params.keys():
                self.terms[key] = params[key]
                is_parameters_set = True

        if not is_parameters_set:
            return None

        results = self.look_up_recipes()

        #値の中身ではなくオブジェクトが同一であるかを判定
        if results is None:
            return None
    
        recipes_list = []
        for i, row in results.iterrows():
            recipe = {}
            recipe["recipeName"] = row["recipeName"]
            recipe["ingredients"] = row["ingredients"]
            recipe["cost"] = row["cost"]
            recipe["cookTime"] = row["cookTime"]
            recipe["url"] = row["url"]
            recipes_list.append(recipe)

        with open('buffer/'+self.save_file+'.json', 'w', encoding='utf-8') as f:
            json.dump(recipes_list, f, indent=2, ensure_ascii=False)

        return len(recipes_list)

    def look_up_recipes(self):
        df = pd.read_csv(self.recipes_file, index_col=False, header=0)

        keywords = {
            ingredient.strip()
            for key, value in self.terms.items()
            if key not in ['cost', 'cookTime'] if value != None
            for ingredient in value.split(',')
        }
        df["match_count"] = df["ingredients"].apply(
            lambda ingredients: self.count_keyword_matches(
                ingredients, keywords)
        )
        filtered_df = df[df["match_count"] > 0].sort_values(by="match_count", ascending=False)
        if self.terms["cost"]:
            filtered_df = filtered_df[filtered_df["cost"] <= self.terms["cost"]]
        if self.terms["cookTime"]:
            filtered_df = filtered_df[filtered_df["cookTime"] <= self.terms["cookTime"]]

        if filtered_df.empty:
            return None

        # print(filtered_df[["ingredients", "match_count"]].head())
        return filtered_df

    def count_keyword_matches(self, ingredients, keywords):
        ingredient_list = set(ingredients.split("、"))
        return len(ingredient_list & keywords)

    def load_recipes(self, note_id):
        file_path = 'buffer/'+note_id+'.json'
        if Path(file_path).is_file():
            with open(file_path, 'r', encoding='utf-8') as f:
                records = json.load(f)
            return records
        
        return None

        """
        {
    'keys': ['key1', 'key2', ... 'keyN'], # recordsの中で用いるキーの一覧
    'records': [
        {'key1': value-11, 'key2': value-21, ... 'keyN': value-N1}, 
        {'key1': value-12, 'key2': value-22, ... 'keyN': value-N2}, 
        ...,
        {'key1': value-1m, 'key2': value-2m, ... 'keyN': value-Nm}, 
    ],
    'message': エラーメッセージ or null(success)
        }
        """
