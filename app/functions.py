import numpy as np
import matplotlib.pyplot as plt, mpld3
import matplotlib

from dotenv import load_dotenv
import os
from app import APP_ENV

import io
from io import BytesIO

# from __init__ import APP_ENV

def _plot_io(**kwargs):
    """
    Helper method to optionally save the figure to file.

    :param filename: name of the file to save to, defaults to None (doesn't save)
    :type filename: str, optional
    :param dpi: dpi of figure to save or plot, defaults to 300
    :type dpi: int (between 50-500)
    :param showfig: whether to plt.show() the figure, defaults to True
    :type showfig: bool, optional
    """
    filename = kwargs.get("filename", None)
    showfig = kwargs.get("showfig", True)
    dpi = kwargs.get("dpi", 300)

    plt.tight_layout()
    if filename:
        plt.savefig(fname=filename, dpi=dpi)
    if showfig:
        plt.show()

def plot_efficient_frontier(cla, start, end, points=100, show_assets=True, **kwargs):
    """
    Plot the efficient frontier based on a CLA object

    :param points: number of points to plot, defaults to 100
    :type points: int, optional
    :param show_assets: whether we should plot the asset risks/returns also, defaults to True
    :type show_assets: bool, optional
    :param filename: name of the file to save to, defaults to None (doesn't save)
    :type filename: str, optional
    :param showfig: whether to plt.show() the figure, defaults to True
    :type showfig: bool, optional
    :return: matplotlib axis
    :rtype: matplotlib.axes object
    """
    if cla.weights is None:
        cla.max_sharpe()
    optimal_ret, optimal_risk, _ = cla.portfolio_performance()

    if cla.frontier_values is None:
        cla.efficient_frontier(points=points)

    mus, sigmas, _ = cla.frontier_values

    fig, ax = plt.subplots()
    ax.plot(sigmas, mus, label="Efficient Frontier", linewidth=3)

    if show_assets:
        ax.scatter(
            np.sqrt(np.diag(cla.cov_matrix)),
            cla.expected_returns,
            s=120,
            color="k",
            label="Assets",
        )
        #NEW...
        for i in range(len(cla.tickers)):
            plt.text(np.sqrt(np.diag(cla.cov_matrix))[i] + 0.0005,cla.expected_returns[i] + 0.0005, cla.tickers[i], fontsize=15, ha='center')




    ax.scatter(optimal_risk, optimal_ret, marker="X", s=200, color="r", label="Optimal (Max Sharpe Ratio)")
    ax.legend()
    ax.set_xlabel("Risk", fontsize=20)
    ax.set_ylabel("Returns", fontsize=20) #expected return, based on annualized return calculated

    title = "Efficient Frontier \n(based on rtns from " + start + " to " + end + ")"

    plt.title(label=title,fontsize=27,pad=20)

    plt.legend(prop={"size":13})

    plt.xticks(fontsize= 13)

    plt.yticks(fontsize= 13)


    _plot_io(**kwargs)
    return fig, ax

def plot_efficient_frontier2(cla, start, end, points=100, show_assets=True, **kwargs):
    """
    Plot the efficient frontier based on a CLA object

    :param points: number of points to plot, defaults to 100
    :type points: int, optional
    :param show_assets: whether we should plot the asset risks/returns also, defaults to True
    :type show_assets: bool, optional
    :param filename: name of the file to save to, defaults to None (doesn't save)
    :type filename: str, optional
    :param showfig: whether to plt.show() the figure, defaults to True
    :type showfig: bool, optional
    :return: bytes_image
    :rtype: BytesIO
    """

    COLOR = '#E4E6EB'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    # plt.rcParams['legend.fontcolor'] = COLOR
    plt.rcParams['legend.frameon'] = True


    #font config
    matplotlib.rcParams['font.family'] = "sans-serif"
    # csfont = {'fontname':'Comic Sans MS'}
    hfont = {'fontname':'Hammersmith One'}

    #font size config
    ticks = 25
    labels = 30
    titlesize = 40
    suptitlesize = 60
    pad = 15


    if cla.weights is None:
        cla.max_sharpe()
    optimal_ret, optimal_risk, _ = cla.portfolio_performance()

    if cla.frontier_values is None:
        cla.efficient_frontier(points=points)

    mus, sigmas, _ = cla.frontier_values

    fig, ax = plt.subplots()
    ax.set_facecolor("#3A3B3C")
    fig.patch.set_facecolor("#3A3B3C")

    ax.plot(
        sigmas, 
        mus, 
        label="Efficient Frontier", 
        color="#047bff", 
        linewidth=4,
        )

    if show_assets:
        ax.scatter(
            np.sqrt(np.diag(cla.cov_matrix)),
            cla.expected_returns,
            s=350,
            color="k",
            label="Assets",
            zorder=4,
        )
        #NEW...
        for i in range(len(cla.tickers)):
            plt.text(np.sqrt(np.diag(cla.cov_matrix))[i] + 0.0005,cla.expected_returns[i] + 0.0005, cla.tickers[i], fontsize=labels, ha='center', zorder=5)


    ax.scatter(optimal_risk, optimal_ret, zorder=3, s=350, marker="x", linewidths=5, color="r", label="Optimal (Max Sharpe Ratio)")
    ax.legend()
    ax.set_xlabel("Risk", fontsize=titlesize, **hfont, labelpad=pad)
    ax.set_ylabel("Returns", fontsize=titlesize, **hfont, labelpad=pad) #expected return, based on annualized return calculated

    suptitle = "Efficient Frontier" 
    fig.suptitle(suptitle, fontsize=suptitlesize, **hfont)

    title = "\nBased on Returns from " + start + " to " + end
    plt.title(label=title, fontsize=titlesize, **hfont, pad =20)

    plt.legend(fontsize=labels, labelcolor="black")

    plt.xticks(fontsize= ticks, **hfont)

    plt.yticks(fontsize= ticks, **hfont)

    width = 1500
    height = 1500
    # fig = mplfigure.Figure(frameon=False)
    dpi = fig.get_dpi()
    fig.set_size_inches(width / dpi, height / dpi)

    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)


    
    html_fig = mpld3.fig_to_html(fig,figid='ef_chart')


    return bytes_image, html_fig


def plot_efficient_frontier3(cla, start, end, points=100, show_assets=True, **kwargs):
    """
    Plot the efficient frontier based on a CLA object, optimizes for minimum volatility

    :param points: number of points to plot, defaults to 100
    :type points: int, optional
    :param show_assets: whether we should plot the asset risks/returns also, defaults to True
    :type show_assets: bool, optional
    :param filename: name of the file to save to, defaults to None (doesn't save)
    :type filename: str, optional
    :param showfig: whether to plt.show() the figure, defaults to True
    :type showfig: bool, optional
    :return: bytes_image
    :rtype: BytesIO
    """

    COLOR = '#E4E6EB'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    # plt.rcParams['legend.fontcolor'] = COLOR
    plt.rcParams['legend.frameon'] = True


    #font config
    matplotlib.rcParams['font.family'] = "sans-serif"
    # csfont = {'fontname':'Comic Sans MS'}
    hfont = {'fontname':'Hammersmith One'}

    #font size config
    ticks = 25
    labels = 30
    titlesize = 40
    suptitlesize = 60
    pad = 15


    if cla.weights is None:
        cla.min_volatility()
    optimal_ret, optimal_risk, _ = cla.portfolio_performance()

    if cla.frontier_values is None:
        cla.efficient_frontier(points=points)

    mus, sigmas, _ = cla.frontier_values

    fig, ax = plt.subplots()
    ax.set_facecolor("#3A3B3C")
    fig.patch.set_facecolor("#3A3B3C")

    ax.plot(
        sigmas, 
        mus, 
        label="Efficient Frontier", 
        color="#047bff", 
        linewidth=4,
        )

    if show_assets:
        ax.scatter(
            np.sqrt(np.diag(cla.cov_matrix)),
            cla.expected_returns,
            s=350,
            color="k",
            label="Assets",
            zorder=4,
        )
        #NEW...
        for i in range(len(cla.tickers)):
            plt.text(np.sqrt(np.diag(cla.cov_matrix))[i] + 0.0005,cla.expected_returns[i] + 0.0005, cla.tickers[i], fontsize=labels, ha='center', zorder=5)


    ax.scatter(optimal_risk, optimal_ret, zorder=3, s=350, marker="x", linewidths=5, color="r", label="Optimal (Minimum Volatility)")
    ax.legend()
    ax.set_xlabel("Risk", fontsize=titlesize, **hfont, labelpad=pad)
    ax.set_ylabel("Returns", fontsize=titlesize, **hfont, labelpad=pad) #expected return, based on annualized return calculated

    suptitle = "Efficient Frontier" 
    fig.suptitle(suptitle, fontsize=suptitlesize, **hfont)

    title = "\nBased on Returns from " + start + " to " + end
    plt.title(label=title, fontsize=titlesize, **hfont, pad =20)

    plt.legend(fontsize=labels, labelcolor="black")

    plt.xticks(fontsize= ticks, **hfont)

    plt.yticks(fontsize= ticks, **hfont)

    width = 1500
    height = 1500
    # fig = mplfigure.Figure(frameon=False)
    dpi = fig.get_dpi()
    fig.set_size_inches(width / dpi, height / dpi)

    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)

    html_fig = mpld3.fig_to_html(fig,figid='ef_chart')


    return bytes_image, html_fig


def plot_weights(weights, **kwargs):
    """
    Plot the portfolio weights as a horizontal bar chart
    :param weights: the weights outputted by any PyPortfolioOpt optimiser
    :type weights: {ticker: weight} dict
    :return: matplotlib axis
    :rtype: matplotlib.axes object
    """
    desc = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in desc]
    vals = [i[1] for i in desc]

    y_pos = np.arange(len(labels))

    fig, ax = plt.subplots()
    ax.barh(y_pos, vals)
    ax.set_xlabel("Weight")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()

    _plot_io(**kwargs)
    return ax

#slightly changed to return BytesIO image now
def plot_weights2(weights, **kwargs):
    """
    Plot the portfolio weights as a horizontal bar chart
    :param weights: the weights outputted by any PyPortfolioOpt optimiser
    :type weights: {ticker: weight} dict
    :return: bytes_image
    :rtype: BytesIO
    """

    COLOR = '#E4E6EB'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR

    #font config
    matplotlib.rcParams['font.family'] = "sans-serif" 
    # csfont = {'fontname':'Comic Sans MS'}
    hfont = {'fontname':'Hammersmith One'}

    #font size config
    ticks = 25
    labelsize = 35
    titlesize = 60
    pad = 20

    desc = sorted(weights.items(), key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in desc]
    vals = [i[1] for i in desc]

    y_pos = np.arange(len(labels))

    weights_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


    fig, ax = plt.subplots()
    ax.set_facecolor("#3A3B3C")
    fig.patch.set_facecolor("#3A3B3C")

    ax.set_xlim([0, 1])

    rects = ax.barh(y_pos, vals, color="#047bff")
    ax.set_xlabel("Weight", fontsize= labelsize, **hfont, labelpad=pad)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize= labelsize, **hfont)

    plt.xticks(fontsize= ticks, **hfont)
    plt.yticks(fontsize= labelsize, **hfont, rotation=0)

    ax.invert_yaxis()

    title = "Optimal Weights"
    plt.title(label=title, fontsize=titlesize, pad=50, **hfont)



    #bar labels
    for i, v in enumerate(vals):
        ax.text(v, i, "{:.2f}%".format(v*100), color='#E4E6EB', rotation=0, fontsize=labelsize, ha='left', va='center')


    #FORMATTING
    ax.tick_params(axis='both', which='major', pad=15)
    ax.set_facecolor("#3A3B3C")



    #IMAGE STUFF

    width = 1500
    height = 1500
    # fig = mplfigure.Figure(frameon=False)
    dpi = fig.get_dpi()
    fig.set_size_inches(width / dpi, height / dpi)

    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)

    html_fig = mpld3.fig_to_html(fig,figid='weights_chart')

    return bytes_image, html_fig