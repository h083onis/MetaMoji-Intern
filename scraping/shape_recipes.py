import json
import glob

tmp = len(glob.glob("resource/**/*.json", recursive=True))

def dfs(categorized_dict, node, category_name):
    if len(node["children"]) == 0:
        return
    for subchild in node.get("children", []):
        categorized_dict[category_name].add(subchild["name"])
        dfs(categorized_dict, subchild, category_name)

recipes = []

for i in range(1, tmp+1):
    with open('resource/'+str(i)+'.json', 'r', encoding='utf-8') as f:
        data = json.load(f)["attributes"]
    recipe_dict = {}
    recipe_dict["title"] = data["title"]
    recipe_dict["cooking_time"] = data["cooking-time"]
    recipe_dict["ingredients"] = data["ingredients-inline"]
    recipe_dict["expense"] = data["expense"]
    recipes.append(recipe_dict)

with open("recipe.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, indent=2, ensure_ascii=False)

print(len(recipes))
    
    