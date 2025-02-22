#%%
import json
import pandas as pd
import plotly.graph_objects as go
import webbrowser

# jsonファイルの読み込み
# app_list.jsonファイルを読み込む
with open('app_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data["tools"])

# layoutの設定
layout = go.Layout(
    title="med_app_mappping_matrix",
    xaxis=dict(title="ターゲット",
            range=[0, 20]),
    yaxis=dict(title="アプローチ",
            range=[0, 20]),
    hovermode="closest"
)

# mapping_matrixの作成
fig = go.Figure(layout=layout)


#%%
# カテゴリと色の対応を定義
color_map = {
    "健康管理": "blue",
    "業務効率化": "green",
    "問診": "red",
    "診断補助": "purple",
    "コミュニケーション": "orange"
}

fig.add_trace(go.Scatter(
    x=df["X"],
    y=df["Y"],
    mode="markers+text",
    text=df["name"],
    textposition="top center",
    marker=dict(
        size=20,
        color=df["category"].map(color_map)
    ),
    customdata=df["url"],
    hovertemplate="<b>%{text}</b><br>Click to open URL<extra></extra>"
))
#%% 
# PNGファイルを作成
fig.write_image("med_app_scatter.png")

