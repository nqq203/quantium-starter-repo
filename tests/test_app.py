import pytest

# dash_duo là fixture có sẵn từ dash.testing để test app
def test_header_present(dash_duo):
    from src.app import app
    dash_duo.start_server(app)

    # Header phải có text "Soul Foods Pink Morsel Sales Visualiser"
    header = dash_duo.find_element("h1")
    assert "Soul Foods Pink Morsel Sales Visualiser" in header.text


def test_graph_present(dash_duo):
    from src.app import app
    dash_duo.start_server(app)

    # Biểu đồ Graph phải tồn tại
    graph = dash_duo.find_element("#sales-chart")
    assert graph is not None


def test_region_picker_present(dash_duo):
    from src.app import app
    dash_duo.start_server(app)

    # Region filter RadioItems phải tồn tại
    region_picker = dash_duo.find_element("#region-filter")
    assert region_picker is not None
