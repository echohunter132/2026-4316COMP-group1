import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this path if your dataset is stored somewhere else
DATA_PATH = "data/covid_19_clean_complete.csv"

data = pd.read_csv(DATA_PATH)
data.columns = data.columns.str.strip()
data["Date"] = pd.to_datetime(data["Date"])

plt.style.use("_mpl-gallery")

def longest_decline_streak():
    df_sorted = data.sort_values(["Country/Region", "Date"]).copy()

    def longest_decline(group):
        decline_streak = 0
        max_streak = 0

        changes = group["Active"].diff()

        for change in changes:
            if change < 0:
                decline_streak += 1
                max_streak = max(max_streak, decline_streak)
            else:
                decline_streak = 0

        return max_streak

    decline_streaks = df_sorted.groupby("Country/Region").apply(longest_decline)
    top5 = decline_streaks.sort_values(ascending=False).head(5)

    print("Countries with the longest sustained decrease in active cases:")
    print(top5)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top5.index, top5.values)

    ax.set(
        title="Top 5 Countries with Longest Sustained Decline in Active Cases",
        xlabel="Longest Consecutive Decline Streak (Days)",
        ylabel="Country"
    )

    ax.grid(True, axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    longest_decline_streak()
