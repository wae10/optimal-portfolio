#bokeh integration script
#plotting weights

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
# from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.tools import HoverTool




def bokeh_weights_graph(sharpe_pwt):
    """returns script and div for interactive bokeh graph of weights, input is collections.orderedDictionary of stocks and weights

    Returns:
        [script]: [script]
        [div]: [div]
    """

    # output_file("bar_colors.html")

    stocks = []
    weights = []

    for key, value in sharpe_pwt.items():
        stocks.append(key)
        weights.append(value)


    source = ColumnDataSource(data=dict(stocks=stocks, weights=weights))

    p = figure(x_range=stocks, y_range=(0,1), plot_height=350, title="Optimal Weights",
            toolbar_location=None, tools="")

    p.vbar(x='stocks', top='weights', width=0.9, legend_field="stocks", source=source)

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    hover = HoverTool()
    # hover.tooltips=[
    # ('Horizontal Movement', '@pfx_x'),
    # ('Vertical Movement', '@pfx_z'),
    # ('Pitch Name', '@pitch_name'),
    # ('Pitcher', '@MLBNAME')
    # ]

    p.add_tools(hover)

    script, div = components(p)

    return script, div

