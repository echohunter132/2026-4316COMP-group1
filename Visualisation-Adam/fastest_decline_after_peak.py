import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this path if your dataset is stored somewhere else
DATA_PATH = "data/covid_19_clean_complete.csv"

data = pd.read_csv(DATA_PATH)
data.columns = data.columns.str.strip()
data["Date"] = pd.to_datetime(data["Date"])

plt.style.use("_mpl-gallery")

def fastest_decline_after_peak():
    active_trend = data.groupby(["Country/Region", "Date"])["Active"].sum().reset_index()

    def decline_rate(group):
        group = group.sort_values("Date")
        peak = group["Active"].max()
        peak_position = group["Active"].idxmax()
        after_peak = group.loc[peak_position:]

        if len(after_peak) > 1:
            return (after_peak.iloc[-1]["Active"] - peak) / len(after_peak)
        return 0

    declines = active_trend.groupby("Country/Region").apply(decline_rate)
    top5 = declines.sort_values().head(5)

    print("Countries that reduced active cases fastest after peak:")
    print(top5)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top5.index, top5.values)

    ax.set(
        title="Top 5 Countries with Fastest Active Case Decline After Peak",
        xlabel="Average Daily Decline After Peak",
        ylabel="Country"
    )

    ax.grid(True, axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fastest_decline_after_peak()
