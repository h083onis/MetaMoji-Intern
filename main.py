#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  eYACHO/GEMBA Noteからのメッセージを受け取り、レシピ検索を行うRESTメソッドを定義する
# 
# [NOTES]
#
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.recipe_processor import RecipeProcessor
from utils.util import getNoteId
    
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



#
# [FUNCTION] is_reload_enabled()
#
# [DESCRIPTION]
#  実行するコマンドに--reloadが含まれるか判定する
#
# [INPUTS] None
#
# [OUTPUTS]
#  True: 含まれる False: 含まれない
#
# [NOTES]
#  Trueの場合はデバッグ実行とみなし、JSONデータをコンソール上に表示する
#
def is_reload_enabled():
    return "--reload" in sys.argv
#
# HISTORY
# [1] 2024-12-XX - Initial version
#

#
# GET Method
# End Point: /
#
# [DESCRIPTION]
#  トップページを開く
#
# [INPUTS]
#  request - リクエスト
# 
# [OUTPUTS]
# 
# [NOTES]
#  Web画面上に単に、"Recipe REST Server for GEMBA"と表示するのみ
#
@app.get("/", response_class=HTMLResponse)
async def topPage(request: Request):
    
    return templates.TemplateResponse("top.html", {"request": request, "title": "Recipe REST Server for GEMBA"})
#
# HISTORY
# [1] 2024-09-30 - Initial version
#

#
# GET Method
# End Point: /recipe/get
#
# [DESCRIPTION]
#  /recipe/putで処理した結果を受け取る
#
# [INPUTS] 
#  request - Request from the method（現時点では利用しない）
# 
# [OUTPUTS]
#  レシピ名、調理時間、調理コスト、カロリーのリストを出力
#  {
#    "keys": [recipeName', 'cookTime', 'cost', 'calorie'],
#    "records": [{'recipeName': 'かつ丼', 'cookTime': 5, 'cost': 300, 'calorie':992}, ...],
#    "message": None
#  }
# 
# [NOTES]
#  /recipe/putで登録された食材からレシピ一覧を提示する
#

#'_pageId': '__subId_v2_[15accacb-3105-40fe-9309-bd1b2957fe6d]_[page]_106'
#__subId_v2_[8fe4458c-0b4d-44cf-b07b-b22b562ee30a]_[page]_26

@app.post("/recipe/get")
def recipeGet(json_data:dict):
    rp = RecipeProcessor()

    results = {}
    results['keys'] = rp.keys

    note_id = getNoteId(json_data['_NOTE_LINK'])
    rp.save_file = note_id
    results["records"] = rp.load_recipes(note_id)

    # list = []
    # elements = {'recipeName':'鶏もも肉と玉ねぎのハーブ炒め', 'cookTime': 15, 'cost': 300, 'url':360, 'ingredients':"ss"}
    # list.append(elements)
    # elements = {'recipeName': '鶏ささみの肉じゃが', 'cookTime': 20, 'cost': 400, 'url':560,'ingredients':"ss"}
    # list.append(elements)
    # elements = {'recipeName':'鶏もも肉とじゃがいものクリーム煮', 'cookTime': 30, 'cost': 400, 'url':670,'ingredients':"ss"}
    # list.append(elements)

    # results['records'] = list
    results['message'] = "取得完了"

    if is_reload_enabled():
        print("[JSON]", results)

    return results

#
# HISTORY
# [1] 2024-12-XX - Initial version
#

#
# POST Method
# End Point: /recipe/put
#
# [DESCRIPTION]
#   eYACHO/GEMBA Noteから食材リストを受け取り処理を行う
#
# [INPUTS] 
#   request - bodyにクライアント（eYACHO/GEMBA Note）からのJSONデータが含まれる
# 
# [OUTPUTS]
#   次のJSONを返す
#   { "message": <メッセージ> }
# 
# [NOTES]
#   eYACHO/GEMBA Noteのボタンアクション「サーバーへ送信」でメッセージを表示させる
#
@app.post("/recipe/put")
def recipePut(json_data: dict):
    results = {}
    results['message'] = "条件に合うレシピが見つかりませんでした"
    
    if is_reload_enabled():
        print("[JSON]", json_data)
    
    rp = RecipeProcessor()
    note_id = getNoteId(json_data['_noteLink'])
    rp.save_file = note_id
    print(rp.save_file)
    status = rp.save_recipes_to_buffer(json_data)

    # ここで受け取った情報から何か処理を実行し、保持しておく
    if status:
        results["message"] = f"条件に合うレシピが{status}件見つかりました"
    return results

# [JSON] {'_userName': '大西 真輝', '_noteTitle': '食材フォーム', '_noteLink': 'https://mps-beta.metamoji.com/link/TbhXHepm-YEMGXRy1bSR6awh.mmjloc', '_pageLink': 'https://mps-beta.metamoji.com/link/5FktPA7lXE7aNNhph-DMw7uD.mmjloc', '_driveId': '3080466101', '_documentId': 'ab2f8c7a-0eda-48c6-87e7-d6e8ece81b95--3078700101', '_objectType': 2, '_objectId': '__subId_v2_[15accacb-3105-40fe-9309-bd1b2957fe6d]_[page]_106', '_pageId': '__subId_v2_[15accacb-3105-40fe-9309-bd1b2957fe6d]_[page]_106', '_x': 0, '_y': 0, '_width': 556, '_height': 417,
#  'vegetables': 'しめじ'}
#
# HISTORY
# [1] 2024-12-XX - Initial version
#