import json
import pandas as pd
import dash
import plotly.graph_objects as go
import webbrowser
import os
from dash import dcc, html
from dash.dependencies import Input, Output, State
from setting.map_layout import MapLayout
from github import Github
from env import Env

REPO_NAME = "med_app_summary"
g = Github(Env.GITHUB_TOKEN)
repo = g.get_user().get_repo(REPO_NAME)
# ----------------------------------------

layout = MapLayout()

# サービスファイルの読み込み
with open('app_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data["services"])

# mapping_matrixの作成
fig = go.Figure(layout=layout.set_layout())
fig.add_trace(layout.set_scatter(df))

# 🌐 Dash アプリを作成
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="scatter-plot", figure=fig),
    # 📝 テキストボックスを追加
    html.Div([
        html.Label("Name:"),
        dcc.Input(id="name-input", type="text", value=""),
        html.Label("URL:"),
        dcc.Input(id="url-input", type="text", value=""),
        html.Button("Submit", id="submit-button"),
    ])
])

# 🖱️ クリックイベントを処理


@app.callback(
    # TODO:文字数制限
    Output("scatter-plot", "figure"),
    Input("scatter-plot", "clickData"),
    Input("submit-button", "n_clicks"),
    State("name-input", "value"),
    State("url-input", "value")
)
def display_click_data(clickData, n_clicks, name_input, url_input):
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")
        if trigger_id[0] == "scatter-plot" and trigger_id[1] == "clickData":
            point_index = clickData["points"][0]["pointIndex"]
            url = df.iloc[point_index]["url"]
            print(f"Opening: {url}")
            webbrowser.open(url)  # クリックしたらブラウザでURLを開く
        elif trigger_id[0] == "submit-button":
            # gh-pagesブランチからadd_data.jsonを取得
            contents = repo.get_contents(
                "assets/add_data.json", ref="gh-pages")
            try:
                with open("assets/add_data.json", "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:  # TODO: 例外処理の追加
                #  ファイルが存在しない場合は空のリストを作成
                existing_data = []

            # 新しいデータの追加
            new_data = {"name": name_input, "url": url_input}
            print(f"確認{existing_data}")
            existing_data["services"].append(new_data)

            try:
                # gh-pagesブランチのファイルを更新
                repo.update_file(
                    contents.path,
                    "Update add_data.json",
                    json.dumps({"services":existing_data}, indent=2),
                    contents.sha,
                    branch="gh-pages",
                )
                print("Data added successfully")
                # print(f"New data: {existing_data}")
            except Exception as e:
                return f"An error occurred: {e}"

            # プルリクエストを作成 (gh-pagesブランチをターゲットにする)
            title = f"New data added: {name_input}"
            body = f"New data added from Dash app: {name_input},{url_input}"
            print(title)
            print(body)
            try:
                pr = repo.create_pull(
                    title=title,
                    body=body,
                    head="gh-pages",
                    base="gh-pages",
                )
                print(f"Pull request created: {pr.html_url}")
            except Exception as e:
                return f"An error occurred: {e}"
    return fig


# 🚀 アプリを実行
if __name__ == "__main__":
    app.run_server(debug=False,
                   host='0.0.0.0',
                   port=8080)
