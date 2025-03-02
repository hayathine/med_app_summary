import yaml
import pandas as pd
import plotly.graph_objects as go
import os

setting_file = os.path.join(os.path.dirname(__file__), 'settings.yaml')

class MapLayout:
    def __init__(self):
        self.settings = {}
        with open(setting_file, 'r', encoding='utf-8') as f:
            self.settings = yaml.safe_load(f)

    def set_layout(self)->go.Layout:
        # layoutの設定
        layout = go.Layout(
            title=dict(
                text="MAPPING MATRIX",
                font=dict(size=40)
                ),
            font=dict(size=10),
            xaxis=self.settings["xaxis"],
            yaxis=self.settings["yaxis"],
            annotations=self.settings["annotations"],
            hovermode="closest"
        )
        return layout

    def set_categories(self)->dict:
        return self.settings["categories"]
    
    def set_symbols(self)->dict:
        return self.settings["targets"]
    
    def set_scatter(self, df:pd.DataFrame)->go.Scatter:
        scatter = go.Scatter(
            x=df["X"],
            y=df["Y"],
            mode="markers+text",
            text=df["name"],
            textposition="top center",
            marker=dict(
                size=10,
                symbol=df["target"].map(self.set_symbols()),
                color=df["category"].map(self.set_categories())
            ),
            customdata=df["url"],
            hovertemplate="<b>%{text}</b><br>Click to open URL<extra></extra>"
        )
        return scatter
        