# web_app/routes/home_routes.py

from flask import Blueprint, render_template, redirect, request, flash, send_file, make_response, send_from_directory, url_for

from app.script import get_cla, optimal_shares
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
    return render_template("home1.html")

@home_routes.route("/num-stocks", methods=["POST"])
def enter_num_stocks():
    print("ENTERING NUMBER OF STOCKS...")
    data = dict(request.form)
    num = int(data["stock_num"])
    print(num)
    return render_template('home2.html', num=num)

@home_routes.route("/plot/done", methods=["POST"])
def enter_score():
    print("CLICKED BUTTON...")
    print("FORM DATA:", dict(request.form)) #> {'full_name': 'Example User', 'email_address': 'me@example.com', 'country': 'US'}
    params = dict(request.form)
    tickers = []

    for i in range(1, len(params)-1):   
        tickers.append(params["stock_"+str(i)])

    # Converting 
    lst = [x.upper() for x in tickers] 
    print(lst)

    start = params["start"]
    end = params["end"]

    cla, start, end = get_cla(lst, start, end)


    bytesObj = plot_efficient_frontier2(cla, start, end, points=100, show_assets=True)


    img = base64.b64encode(bytesObj.getvalue())

    #RESULTS DESCRIPTION
    amount = 10000 #default 10,0000 dollar amount invested
    allocation, leftover, performance = optimal_shares(lst, start, end, amount)

    print("ALLOCATION: ", allocation)

    #convert dict to list for access in html
    keys = list(allocation)

    print("LIST(ALLOCATION) aka keys: ", keys)

    performance = list(performance)

    print(performance)

    #formatting

    performance[0] = performance[0] * 100
    performance[1] = performance[1] * 100
    
    performance[0] = "{:.2f}%".format(performance[0]) 
    performance[1] = "{:.2f}%".format(performance[1])
    performance[2] = "{:.2f}".format(performance[2])

    leftover = "${:.2f}".format(leftover)

    #length of 'allocation' dictionary
    length = len(allocation)

    return render_template('results.html', img=img.decode('ascii'), allocation=allocation, keys=keys, length=length, leftover=leftover, performance = performance)

