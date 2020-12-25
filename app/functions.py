import numpy as np
import matplotlib.pyplot as plt

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
    ax.set_xlabel("Standard Deviation", fontsize=20)
    ax.set_ylabel("Expected Return", fontsize=20) #expected return, based on annualized return calculated

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
    ax.set_xlabel("Standard Deviation", fontsize=20)
    ax.set_ylabel("Expected Return", fontsize=20) #expected return, based on annualized return calculated

    title = "Efficient Frontier \n(based on rtns from " + start + " to " + end + ")"

    plt.title(label=title,fontsize=27,pad=20)

    plt.legend(prop={"size":13})

    plt.xticks(fontsize= 13)

    plt.yticks(fontsize= 13)

    width = 1000
    height = 1000
    # fig = mplfigure.Figure(frameon=False)
    dpi = fig.get_dpi()
    fig.set_size_inches(width / dpi, height / dpi)

    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)

    return bytes_image
