import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Change this path if your dataset is stored somewhere else
DATA_PATH = "data/covid_19_clean_complete.csv"

data = pd.read_csv(DATA_PATH)
data.columns = data.columns.str.strip()
data["Date"] = pd.to_datetime(data["Date"])

plt.style.use("_mpl-gallery")

def find_anomalies():
    df_sorted = data.sort_values(["Country/Region", "Date"]).copy()

    df_sorted["Confirmed Change"] = df_sorted.groupby("Country/Region")["Confirmed"].diff()
    df_sorted["Deaths Change"] = df_sorted.groupby("Country/Region")["Deaths"].diff()

    anomalies = df_sorted[
        (df_sorted["Deaths Change"] > 0) & (df_sorted["Confirmed Change"] <= 0)
    ]

    anomaly_counts = anomalies["Country/Region"].value_counts().head(10)

    print("Countries with unusual reporting patterns:")
    print(anomaly_counts)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(anomaly_counts.index, anomaly_counts.values)

    ax.set(
        title="Top 10 Countries with Death Increases but No Confirmed Case Increase",
        xlabel="Number of Anomaly Days",
        ylabel="Country"
    )

    ax.grid(True, axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    find_anomalies()
