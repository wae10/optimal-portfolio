# web_app/routes/home_routes.py

from flask import Blueprint, render_template, redirect, request, flash, send_file, make_response, send_from_directory, url_for

from app.script import get_cla, optimal_shares, graph_weights, optimal_shares_min_vol, graph_weights_min_vol
from app.functions import plot_efficient_frontier2, plot_efficient_frontier3, plot_weights2



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





###########################
from app.bokeh import bokeh_weights_graph
###########################

#for storing variables
class DataStore():
    num = None
    amount = None
    objective = None

    #for bokeh stuff
    div = None
    script = None

data = DataStore()


@home_routes.route('/favicon.ico')
def fav():
    return redirect(url_for('static', filename='favicon.ico'), code=302)

@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    #return "Welcome Home (TODO)"
    return render_template("home1.html")

@home_routes.route("/num-stocks", methods=["POST"])
def enter_num_stocks():
    print("ENTERING NUMBER OF STOCKS...")
    params = dict(request.form)
    print(params)
    num = int(params["stock_num"])
    amount = int(params["amount"])
    objective = params["objective"]
    print(num)
    
    #update global class vars
    data.num = num
    data.amount = amount
    data.objective = objective
    print("OBJECTIVE:", objective)

    return render_template('home2.html', num=num, amount=amount)

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

    amount = data.amount

    #which objective?
    if data.objective == "Minimize Volatility":
        bytesObj, ef_html_fig = plot_efficient_frontier3(cla, start, end, points=100, show_assets=True)
        allocation, leftover, performance = optimal_shares_min_vol(lst, start, end, amount)
        min_vol_pwt = graph_weights_min_vol(lst,start,end)
        print("MIN_VOL_PWT", min_vol_pwt)

        bytesObj2, fig_html = plot_weights2(min_vol_pwt)


    #default to max sharpe ratio even if incorrect value
    else:
        bytesObj, ef_html_fig = plot_efficient_frontier2(cla, start, end, points=100, show_assets=True)
        allocation, leftover, performance = optimal_shares(lst, start, end, amount)
        #GRAPH WEIGHTS PART
        sharpe_pwt = graph_weights(lst,start,end)
        print("SHARPE_PWT", sharpe_pwt)

        print("type(sharpe_pwt)", type(sharpe_pwt))

        print("\nfor key, value in sharpe_pwt.items()")
        for key, value in sharpe_pwt.items():
            print (key)
            print (value)

        bytesObj2, fig_html = plot_weights2(sharpe_pwt)



    img = base64.b64encode(bytesObj.getvalue())

    #RESULTS DESCRIPTION

    print("AMOUNT: ", amount)

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

    img2 = base64.b64encode(bytesObj2.getvalue())

    #tweaking 'objective' for results.html output
    if data.objective == "Minimize Volatility":
        objective = "minimum volatility portfolio"
    else:
        objective = "maximum sharpe ratio portfolio"

    #write fig_html to chart.html
    Html_file= open("web_app/templates/chart.html","w")
    Html_file.write(ef_html_fig)
    Html_file.close()

    script, div = bokeh_weights_graph(sharpe_pwt)

    data.script = script
    data.div = div

    print(script)

    print("\n\n")

    print(div)

    return render_template('results.html', script=script, div=div, ef_html_fig=ef_html_fig, amount=amount, img=img.decode('ascii'), img2=img2.decode('ascii'), allocation=allocation, keys=keys, length=length, leftover=leftover, performance = performance, objective=objective)

@home_routes.route("/plot/chart")
def interactive_chart():
    print("INTERACTIVE CHART OPENING...")
    return render_template("chart.html")


@home_routes.route("/plot/bokeh_temp")
def bokeh_temp():
    print("CLICKED BOKEH TEMP LINK...")
    return render_template("bokeh_temp.html", div=data.div, script=data.script)

@home_routes.route("/todo")
def todo():
    print("TODO...")
    return render_template("todo.html")