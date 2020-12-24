# web_app/routes/home_routes.py

from flask import Blueprint, render_template, redirect, request, flash, send_file, make_response, send_from_directory, url_for

from app.script import get_cla
from app.functions import plot_efficient_frontier



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


@home_routes.route("/plot/done", methods=["POST"])
def plot():
    """ Returns html with the plot.
    """

    print("ENTERING PLOT DATA INPUTS")

    params = dict(request.form)

    print(params)

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

    points=100
    show_assets=True

    fig, ax = plot_efficient_frontier(cla,start,end,points,show_assets=True)

    width = 1000
    height = 1000
    # fig = mplfigure.Figure(frameon=False)
    dpi = fig.get_dpi()
    fig.set_size_inches(width / dpi, height / dpi)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

    # if cla.weights is None:
    #     cla.max_sharpe()
    # optimal_ret, optimal_risk, _ = cla.portfolio_performance()

    # if cla.frontier_values is None:
    #     cla.efficient_frontier(points=points)

    # mus, sigmas, _ = cla.frontier_values

    # fig, ax = plt.subplots()
    # ax.plot(sigmas, mus, label="Efficient frontier")

    # if show_assets:
    #     ax.scatter(
    #         np.sqrt(np.diag(cla.cov_matrix)),
    #         cla.expected_returns,
    #         s=30,
    #         color="k",
    #         label="Assets",
    #     )
    #     #NEW...
    #     for i in range(len(cla.tickers)):
    #         plt.text(np.sqrt(np.diag(cla.cov_matrix))[i],cla.expected_returns[i], cla.tickers[i])

    # ax.scatter(optimal_risk, optimal_ret, marker="X", s=100, color="r", label="Optimal")
    # ax.legend()
    # ax.set_xlabel("Risk (Std Dev)")
    # ax.set_ylabel("Return") #expected return, based on annualized return calculated

    # canvas = FigureCanvasAgg(fig)
    # img = io.BytesIO()
    # fig.savefig(img)
    # img.seek(0)

    # encoded_img = base64.encodebytes(img.getvalue()).decode('ascii')
    # return encoded_img

    # return send_file(img, mimetype='image/png')


@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    #return "Welcome Home (TODO)"
    return render_template("home.html")


# @home_routes.route("/plot", methods=["POST"])
# def enter_score():
#     print("CLICKED BUTTON...")
#     print("FORM DATA:", dict(request.form)) #> {'full_name': 'Example User', 'email_address': 'me@example.com', 'country': 'US'}
#     params = dict(request.form)
#     tickers = []
#     tickers.append(params["stock_1"])
#     tickers.append(params["stock_2"])
#     tickers.append(params["stock_3"])

#     start = params["start"]
#     end = params["end"]

#     cla = get_cla(tickers, start, end)

#     fig = plot_efficient_frontier(cla, points=100, show_assets=True)
#     fig.savefig('/images/new_plot.png')

#     return render_template("result.html", name = 'new_plot', url = '/images/new_plot.png')



    # if user["email_address"] and user["first_name"] and user["last_name"] and user["date"] and user["course"] and user["score"] and user["rating"] and user["slope"]:
    #     differential = (eval(user["score"])-eval(user["rating"]))*(113/eval(user["slope"]))
    #     post_score(user["email_address"], user["first_name"], user["last_name"], user["date"], user["course"], user["score"], user["rating"], user["slope"], differential)
    #     email=user["email_address"].lower()
    #     results = scores(email)
    #     flash(f"Your score of {user['score']} at {user['course']} on {user['date']} was entered successfully!", "success") #success = green color alert
    #     return render_template("handicap_result.html", email=email, results=results)
        
    # else:
    #     flash(f"Oops, try again! Make sure you fill out all elements of the form!", "danger")
    #     return render_template("post.html")
    

# @home_routes.route("/users/new")
# def new_user():
#     print("VISITED THE REGISTRATION PAGE")
#     # return "Sign Up for our Product! (TODO)"
#     return render_template("new_user_form.html")

# @home_routes.route("/users/create", methods=["POST"])
# def create_user():
#     print("CREATING A NEW USER...")
#     print("FORM DATA:", dict(request.form)) #> {'full_name': 'Example User', 'email_address': 'me@example.com', 'country': 'US'}
#     user = dict(request.form)
#     # todo: store in a database or google sheet!
#     #flash(f"User '{user['full_name']}' created successfully!", "success")
#     flash(f"User '{user['full_name']}' created successfully!", "success") #success = green color alert
#     return redirect("/")

