import numpy as np
import matplotlib.pyplot as plt

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

def plot_efficient_frontier(cla, points=100, show_assets=True, **kwargs):
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
    ax.plot(sigmas, mus, label="Efficient frontier")

    if show_assets:
        ax.scatter(
            np.sqrt(np.diag(cla.cov_matrix)),
            cla.expected_returns,
            s=30,
            color="k",
            label="Assets",
        )
        #NEW...
        for i in range(len(cla.tickers)):
            plt.text(np.sqrt(np.diag(cla.cov_matrix))[i],cla.expected_returns[i], cla.tickers[i])

    ax.scatter(optimal_risk, optimal_ret, marker="X", s=100, color="r", label="Optimal")
    ax.legend()
    ax.set_xlabel("Risk (Std Dev)")
    ax.set_ylabel("Return") #expected return, based on annualized return calculated

    _plot_io(**kwargs)
    return ax