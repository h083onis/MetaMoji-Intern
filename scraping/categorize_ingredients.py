import json
import glob

tmp = len(glob.glob("resource/**/*.json", recursive=True))

category_dict = {'魚介', 'はちみつ', '餅', '野菜', '乳製品', '肉', '大豆・豆腐', 'その他'}
categorized_dict = {tmp:set() for tmp in category_dict}

def dfs(categorized_dict, node, category_name):
    if len(node["children"]) == 0:
        return
    for subchild in node.get("children", []):
        categorized_dict[category_name].add(subchild["name"])
        dfs(categorized_dict, subchild, category_name)

result = set()

for i in range(1, tmp+1):
    with open('resource/'+str(i)+'.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    categories = data["attributes"]["related-categories"]
    if len(categories) == 0:
        continue

    for category in data["attributes"]["related-categories"]:
        if "材料で探す" == category.get("name"):
            for child in category.get("children", []):
                dfs(categorized_dict, child, child["name"])

categorized_dict = {key:sorted(list(value)) for key, value in categorized_dict.items()}

with open("category.json", "w", encoding="utf-8") as f:
    json.dump(categorized_dict, f, indent=2,ensure_ascii=False)
    
