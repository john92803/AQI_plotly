import requests
import pandas as pd
import plotly.express as px
import webbrowser
import os

# API 設定
API_URL = "https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=9e565f9a-84dd-4e79-9097-d403cae1ea75&limit=1000&sort=ImportDate desc&format=JSON"

# 取得資料
response = requests.get(API_URL)
data = response.json()["records"]

# 轉成 DataFrame 並處理格式
df = pd.DataFrame(data)
df = df[df["aqi"].str.isdigit()]  # 過濾無效值
df["aqi"] = df["aqi"].astype(int)
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)

# 顏色依照 AQI 設定（使用連續色條 or 自訂色階）
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="aqi",
    size_max=15,
    zoom=6.5,
    color_continuous_scale=[
        (0.0, "green"),
        (0.2, "yellow"),
        (0.4, "orange"),
        (0.6, "red"),
        (0.8, "purple"),
        (1.0, "maroon")
    ],
    size=[10]*len(df),
    hover_name="sitename",
    hover_data={"aqi": True, "status": True, "pollutant": True}
)

fig.update_layout(
    mapbox_style="carto-positron",
    title="台灣空氣品質指標（AQI）地圖",
    margin={"r":0,"t":40,"l":0,"b":0}
)

filename = "aqi_map.html"
fig.write_html(filename)
full_path = os.path.abspath(filename)
webbrowser.open(f"file://{full_path}")