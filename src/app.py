import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import datetime

# Đọc dữ liệu đã xử lý từ task trước
df = pd.read_csv("output.csv")

# Chuyển cột Date sang datetime
df["Date"] = pd.to_datetime(df["Date"])

# Gom tổng sales theo ngày (tất cả region)
df_grouped = df.groupby("Date", as_index=False)["Sales"].sum()

# Tạo app Dash
app = dash.Dash(__name__)

# Line chart với Plotly Express
fig = px.line(
    df_grouped,
    x="Date",
    y="Sales",
    title="Pink Morsels Sales Over Time",
    labels={"Date": "Date", "Sales": "Total Sales (USD)"}
)

# Thêm đường dọc ngày 2021-01-15 (price increase)
fig.add_shape(
    type="line",
    x0=datetime.datetime(2021, 1, 15),
    y0=0,
    x1=datetime.datetime(2021, 1, 15),
    y1=df_grouped["Sales"].max(),   # kéo tới max Sales
    line=dict(color="red", width=2, dash="dash")
)

# Thêm annotation text
fig.add_annotation(
    x=datetime.datetime(2021, 1, 15),
    y=df_grouped["Sales"].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=2,
    ax=40,
    ay=-40
)


# Layout Dash
app.layout = html.Div(children=[
    html.H1("Soul Foods Pink Morsel Sales Visualiser", style={'textAlign': 'center'}),
    dcc.Graph(id="sales-chart", figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
