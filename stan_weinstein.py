import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt


def apply_stan_weinstein_strategy(data):
    # Calculate the 30-week moving average
    data["30-week MA"] = data["Close"].rolling(window=30).mean()

    # Calculate the 10-week moving average
    data["10-week MA"] = data["Close"].rolling(window=10).mean()

    # Identify buy and sell signals based on the strategy
    data["Buy Signal"] = (data["10-week MA"] > data["30-week MA"]) & (
        data["10-week MA"].shift(1) < data["30-week MA"].shift(1)
    )
    data["Sell Signal"] = (data["10-week MA"] < data["30-week MA"]) & (
        data["10-week MA"].shift(1) > data["30-week MA"].shift(1)
    )

    # Create the plot
    fig, ax = plt.subplots()
    ax.set_ylabel("Price")
    ax.set_title("Stan Weinstein Strategy")

    # Plot the candlestick chart
    # mpf.plot(data, type="candle", ax=ax, volume=True, show_nontrading=False)
    data.rename(columns={"Adj Close": "Adj_close"}, inplace=True)
    data = data.copy()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    fig.set_facecolor("#ffe8a8")
    ax1.set_zorder(1)
    ax1.grid(True, color="k", linestyle="--")
    ax1.set_frame_on(False)
    ax2 = ax1.twinx()
    ax2.grid(False)
    mpf.plot(
        data, ax=ax1, type="candle", volume=ax2, xlim=(data.index[0], data.index[-1])
    )

    # Plot the moving averages
    ax.plot(data.index, data["30-week MA"], label="30-week MA")
    ax.plot(data.index, data["10-week MA"], label="10-week MA")
    ax.plot(data.index, data["Close"], label="Eicher Motors")

    # Plot the buy and sell signals
    ax.plot(
        data[data["Buy Signal"]].index,
        data[data["Buy Signal"]]["Close"],
        "^",
        markersize=10,
        color="g",
        label="Buy Signal",
    )
    ax.plot(
        data[data["Sell Signal"]].index,
        data[data["Sell Signal"]]["Close"],
        "v",
        markersize=10,
        color="r",
        label="Sell Signal",
    )

    ax.legend()
    plt.show()


# Assuming you have a CSV file with stock data
data = pd.read_csv("stock_data.csv", index_col=0, parse_dates=True)
apply_stan_weinstein_strategy(data)
