# web_app/routes/home_routes.py

from flask import Blueprint, render_template, redirect, request, flash, send_file, make_response, send_from_directory, url_for

from app.script import get_cla
from app.functions import plot_efficient_frontier, plot_efficient_frontier2



home_routes = Blueprint("home_routes", __name__)



import io
from io import BytesIO
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


from matplotlib.figure import Figure

app = Flask(__name__)


from dotenv import load_dotenv
import os
from app import APP_ENV


###########################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
from matplotlib.ticker import FuncFormatter

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.cla import CLA
from pypfopt.plotting import plot_weights
from matplotlib.ticker import FuncFormatter
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from collections import namedtuple

###########################

plt.switch_backend('Agg')
import base64

import matplotlib.figure as mplfigure


@home_routes.route('/favicon.ico')
def hello():
    return redirect(url_for('static', filename='favicon.ico'), code=302)


# @home_routes.route("/plot/done", methods=["POST"])
# def plot():
#     """ Returns html with the plot.
#     """

#     print("ENTERING PLOT DATA INPUTS")

#     params = dict(request.form)

#     print(params)

#     tickers = []
#     tickers.append(params["stock_1"])
#     tickers.append(params["stock_2"])
#     tickers.append(params["stock_3"])

#     # Converting 
#     lst = [x.upper() for x in tickers] 
#     print(lst)

#     start = params["start"]
#     end = params["end"]

#     cla, start, end = get_cla(lst, start, end)

#     points=100
#     show_assets=True

#     fig, ax = plot_efficient_frontier(cla,start,end,points,show_assets=True)

#     width = 1000
#     height = 1000
#     # fig = mplfigure.Figure(frameon=False)
#     dpi = fig.get_dpi()
#     fig.set_size_inches(width / dpi, height / dpi)

#     canvas = FigureCanvas(fig)
#     output = io.BytesIO()
#     canvas.print_png(output)
#     response = make_response(output.getvalue())
#     response.mimetype = 'image/png'
#     return render_template('results.html', response=output)


@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    #return "Welcome Home (TODO)"
    return render_template("home.html")


@home_routes.route("/plot/done", methods=["POST"])
def enter_score():
    print("CLICKED BUTTON...")
    print("FORM DATA:", dict(request.form)) #> {'full_name': 'Example User', 'email_address': 'me@example.com', 'country': 'US'}
    params = dict(request.form)
    tickers = []
    tickers.append(params["stock_1"])
    tickers.append(params["stock_2"])
    tickers.append(params["stock_3"])

    # Converting 
    lst = [x.upper() for x in tickers] 
    print(lst)

    start = params["start"]
    end = params["end"]

    cla, start, end = get_cla(lst, start, end)


    bytesObj = plot_efficient_frontier2(cla, start, end, points=100, show_assets=True)


    img = base64.b64encode(bytesObj.getvalue())


    return render_template('results.html', img=img.decode('ascii'))

