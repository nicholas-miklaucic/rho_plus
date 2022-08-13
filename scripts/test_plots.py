#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
import rho_plus as rho
from pathlib import Path


def test_plot(use_rho=False, is_dark=False):
    if use_rho:
        # Use Rho+ styling
        rho.mpl_setup(is_dark, setup=True)
    else:
        # use defaults
        plt.rcdefaults()

    # Rho+ doesn't pick a font for you: use whatever you like/have installed
    plt.rcParams["font.sans-serif"] = ["Source Sans Pro"]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
        2, 2, figsize=(12, 12), gridspec_kw=dict(wspace=0.3)
    )

    fig.suptitle("Demo Plot")

    flights = sns.load_dataset("flights")

    sns.boxplot(
        data=flights,
        x="month",
        y="passengers",
        ax=ax1,
        # use Rho+ box plot styling
        **(rho.boxstyle() if use_rho else {})
    )
    ax1.set_title("Airline Passengers by Month")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Airline Passengers")

    if use_rho:
        # move the y-axis label to the top and make it horizontal
        rho.ylabel_top(ax1)

        # make the axes end at the limits of the plot, and show those as ticks
        rho.smart_ticks(ax1)

    xx = np.arange(10) + 1
    ax2.plot(xx, 2 * xx, label="$O(n)$")
    ax2.plot(xx[:5], np.exp(xx[:5] - 0.1), label="Exponential (cut off for space)")
    ax2.plot(xx, xx ** 2, label="$O(n^2)$")
    ax2.plot(xx, xx * np.log(xx) + 5 / (xx + 2), label=r"$O(n \log n)$")
    ax2.plot(xx, np.log(xx), label=r"$O(\log n)$")
    ax2.plot(xx, xx * 0 + 1, label=r"$O(1)$")
    ax2.legend()
    ax2.set_ylabel("Runtime", wrap=True)
    ax2.set_title("Different Kinds of Big-O Growth")

    if use_rho:
        # move the y-axis label to the top and make it horizontal
        rho.ylabel_top(ax2)

        # make the axes end at the limits of the plot, and show those as ticks
        rho.smart_ticks(ax2)

        # add the labels to the ends of the line chart instead of a legend
        rho.line_labels(ax2)

    penguins = sns.load_dataset("penguins")
    im = ax3.scatter(
        data=penguins,
        c="body_mass_g",
        x="bill_depth_mm",
        y="bill_length_mm",
        ec="face",
        # use Rho+ version of viridis
        # this isn't quite as light of a yellow, so it shows up better on a white background
        cmap="rho_viridia" if use_rho else "viridis",
    )
    ax3.set_title("Penguin Bills by Body Mass")
    ax3.set_xlabel("Bill Depth (mm)")
    ax3.set_ylabel("Bill Length (mm)")
    fig.colorbar(im, ax=ax3)

    if use_rho:
        # move the y-axis label to the top and make it horizontal
        rho.ylabel_top(ax3)

    mpg = sns.load_dataset("mpg")
    sns.boxplot(
        data=mpg,
        y="origin",
        x="horsepower",
        orient="h",
        ax=ax4,
        # use Rho box styling
        **(rho.boxstyle() if use_rho else {})
    )

    if use_rho:
        # switch to alternate unfilled boxplot
        rho.unfill_boxplot(ax4)

        # move the y-axis label to the top and make it horizontal
        rho.ylabel_top(ax4)

    ax4.set_title("Car Horsepower by Region")
    return fig


print("Saving demo images...")

imdir = Path.cwd() / "images"

test_plot().savefig(imdir / "default.png")

test_plot(True).savefig(imdir / "rho-light.png")

test_plot(True, True).savefig(imdir / "rho-dark.png")
print("Done!")
