import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this path if your dataset is stored somewhere else
DATA_PATH = "data/covid_19_clean_complete.csv"

data = pd.read_csv(DATA_PATH)
data.columns = data.columns.str.strip()
data["Date"] = pd.to_datetime(data["Date"])

plt.style.use("_mpl-gallery")

def fastest_region_to_100k():
    region_daily = data.groupby(["WHO Region", "Date"])["Confirmed"].sum().reset_index()

    def time_to_threshold(group, threshold=100000):
        group = group.sort_values("Date")
        reached = group[group["Confirmed"] >= threshold]

        if not reached.empty:
            return (reached.iloc[0]["Date"] - group.iloc[0]["Date"]).days
        return np.nan

    threshold_times = region_daily.groupby("WHO Region").apply(time_to_threshold)
    threshold_times = threshold_times.dropna().sort_values()

    print("Fastest WHO regions to reach 100,000 confirmed cases:")
    print(threshold_times)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(threshold_times.index, threshold_times.values)

    ax.set(
        title="Days Taken for WHO Regions to Reach 100,000 Confirmed Cases",
        xlabel="Days Taken",
        ylabel="WHO Region"
    )

    ax.grid(True, axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    fastest_region_to_100k()
