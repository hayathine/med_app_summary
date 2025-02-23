import json
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import webbrowser

# 📂 JSON ファイルを読み込む
with open("app_list.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["tools"])

# 📊 散布図を作成
fig = px.scatter(df, x="X", y="Y", text="name", hover_data=["url"])
fig.update_traces(textposition="top center", marker=dict(size=12, color="blue"))

# 🌐 Dash アプリを作成
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="scatter-plot", figure=fig)
])

# 🖱️ クリックイベントを処理
@app.callback(
    Output("scatter-plot", "figure"),
    Input("scatter-plot", "clickData")
)
def display_click_data(clickData):
    if clickData:
        point_index = clickData["points"][0]["pointIndex"]
        url = df.iloc[point_index]["url"]
        print(f"Opening: {url}")
        webbrowser.open(url)  # クリックしたらブラウザでURLを開く
    return fig

# 🚀 アプリを実行
if __name__ == "__main__":
    app.run_server(debug=False,
                host='0.0.0.0',
                port=8080)
