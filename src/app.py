#%%
import json
import yaml
import pandas as pd
import plotly.graph_objects as go
from setting.map_layout import MapLayout

layout = MapLayout()

# サービスファイルの読み込み
with open('app_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data["services"])

# mapping_matrixの作成
fig = go.Figure(layout=layout.set_layout())
fig.add_trace(layout.set_scatter(df))

fig.show()
#%% 
# PNGファイルを作成
fig.write_image("images/med_app_scatter.png",engine='orca')

