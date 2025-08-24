import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import datetime

# === Đọc dữ liệu đã xử lý từ output.csv ===
df = pd.read_csv("output.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Khởi tạo app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f8f9fa",
        "padding": "20px"
    },
    children=[
        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#2c3e50"}
        ),

        html.Div(
            [
                html.Label("Select Region:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"margin": "10px"}
                ),
            ],
            style={
                "backgroundColor": "#ffffff",
                "padding": "10px",
                "borderRadius": "8px",
                "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                "marginBottom": "20px"
            }
        ),

        dcc.Graph(id="sales-chart", style={"borderRadius": "10px", "overflow": "hidden"})
    ]
)

# Callback update chart theo region
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(region):
    if region == "all":
        dff = df.groupby("Date", as_index=False)["Sales"].sum()
        title = "Total Sales Across All Regions"
    else:
        dff = df[df["Region"].str.lower() == region].groupby("Date", as_index=False)["Sales"].sum()
        title = f"Sales in {region.capitalize()} Region"

    # Vẽ line chart
    fig = px.line(
        dff,
        x="Date",
        y="Sales",
        title=title,
        labels={"Date": "Date", "Sales": "Sales (USD)"}
    )

    # Thêm vline ngày tăng giá 2021-01-15
    fig.add_shape(
        type="line",
        x0=datetime.datetime(2021, 1, 15),
        y0=0,
        x1=datetime.datetime(2021, 1, 15),
        y1=dff["Sales"].max(),
        line=dict(color="red", width=2, dash="dash")
    )
    fig.add_annotation(
        x=datetime.datetime(2021, 1, 15),
        y=dff["Sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40
    )

    fig.update_layout(
        plot_bgcolor="#ecf0f1",
        paper_bgcolor="#f8f9fa",
        font=dict(color="#2c3e50")
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
