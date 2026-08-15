#!/usr/bin/env python3
"""Generate the U.S. real GDP trend-cycle figure used in lecture02.qmd."""

from __future__ import annotations

import csv
import os
from datetime import datetime
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/gradmacro2026-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/gradmacro2026-cache")
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "lecture02" / "gdpc1.csv"
OUTPUT_PATH = ROOT / "figures" / "lecture02" / "us_real_gdp_trend_cycle.svg"
HP_LAMBDA = 1600.0


def read_gdp(path: Path) -> tuple[list[datetime], np.ndarray]:
    dates: list[datetime] = []
    values: list[float] = []

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["observation_date", "GDPC1"]:
            raise ValueError(f"Unexpected columns in {path}: {reader.fieldnames}")
        for row in reader:
            value = row["GDPC1"].strip()
            if not value or value == ".":
                continue
            dates.append(datetime.strptime(row["observation_date"], "%Y-%m-%d"))
            values.append(float(value))

    gdp = np.asarray(values, dtype=float)
    if len(dates) < 12 or len(dates) != len(gdp):
        raise ValueError("The GDP series is missing or too short for a quarterly trend chart.")
    if np.any(gdp <= 0):
        raise ValueError("Real GDP must be positive before taking logarithms.")
    if any(date.month not in {1, 4, 7, 10} for date in dates):
        raise ValueError("The input contains a non-quarterly observation date.")
    if any(
        (right.year * 12 + right.month) - (left.year * 12 + left.month) != 3
        for left, right in zip(dates, dates[1:])
    ):
        raise ValueError("The quarterly GDP series contains a date gap.")

    return dates, gdp


def hp_filter(series: np.ndarray, smoothing: float) -> tuple[np.ndarray, np.ndarray]:
    """Return the HP trend and cycle using the standard penalized least squares form."""

    n_obs = len(series)
    second_difference = np.diff(np.eye(n_obs), n=2, axis=0)
    system = np.eye(n_obs) + smoothing * (second_difference.T @ second_difference)
    trend = np.linalg.solve(system, series)
    cycle = series - trend
    return trend, cycle


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor("#fbfcfe")
    axis.grid(axis="y", color="#dfe5ec", linewidth=0.8)
    axis.grid(axis="x", visible=False)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color("#8793a1")
    axis.spines["bottom"].set_color("#8793a1")
    axis.tick_params(colors="#45515f", labelsize=10)


def main() -> None:
    dates, gdp = read_gdp(DATA_PATH)
    log_gdp = np.log(gdp)
    trend, cycle = hp_filter(log_gdp, HP_LAMBDA)
    cycle_percent = 100.0 * cycle

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Hiragino Sans",
                "Hiragino Kaku Gothic ProN",
                "Arial Unicode MS",
                "DejaVu Sans",
            ],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
        }
    )

    figure, (top, bottom) = plt.subplots(
        2,
        1,
        figsize=(11.0, 7.4),
        sharex=True,
        gridspec_kw={"height_ratios": [1.05, 1.0]},
    )
    figure.patch.set_facecolor("white")
    figure.suptitle(
        "米国実質GDPのトレンドと循環",
        x=0.085,
        y=0.980,
        ha="left",
        fontsize=18,
        fontweight="bold",
        color="#20262e",
    )
    figure.text(
        0.085,
        0.925,
        f"季節調整済み四半期データ、{dates[0].year}年第1四半期―"
        f"{dates[-1].year}年第{(dates[-1].month - 1) // 3 + 1}四半期",
        ha="left",
        fontsize=11,
        color="#596574",
    )

    style_axis(top)
    top.plot(
        dates,
        log_gdp,
        color="#2f6fbe",
        linewidth=1.6,
        label="対数実質GDP",
        zorder=2,
    )
    top.plot(
        dates,
        trend,
        color="#d9792f",
        linewidth=2.2,
        linestyle=(0, (5, 3)),
        label="HPトレンド",
        zorder=3,
    )
    top.set_title("A. 対数実質GDPとトレンド", loc="left", fontsize=13, pad=9, color="#20262e")
    top.set_ylabel("対数値", fontsize=11, color="#34404d")
    top.legend(
        loc="upper left",
        frameon=False,
        ncol=2,
        fontsize=10,
        handlelength=3.0,
        columnspacing=1.8,
    )

    style_axis(bottom)
    bottom.axhline(0.0, color="#596574", linewidth=1.0, zorder=1)
    bottom.plot(dates, cycle_percent, color="#2f6fbe", linewidth=1.6, zorder=2)
    bottom.set_title("B. トレンドからの対数乖離", loc="left", fontsize=13, pad=9, color="#20262e")
    bottom.set_ylabel("乖離（%）", fontsize=11, color="#34404d")
    bottom.set_xlabel("年", fontsize=11, color="#34404d")
    bottom.xaxis.set_major_locator(mdates.YearLocator(10))
    bottom.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    bottom.margins(x=0.005)

    figure.subplots_adjust(left=0.085, right=0.985, top=0.865, bottom=0.105, hspace=0.32)
    figure.text(
        0.085,
        0.025,
        "Source: U.S. Bureau of Economic Analysis via FRED (GDPC1).",
        ha="left",
        fontsize=9,
        color="#687482",
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        OUTPUT_PATH,
        format="svg",
        metadata={
            "Title": "米国実質GDPのトレンドと循環",
            "Description": "対数実質GDPとHPトレンド、およびトレンドからの対数乖離を示す二段の時系列図。",
            "Creator": "scripts/lecture02/generate_us_real_gdp_hp.py",
        },
    )
    plt.close(figure)

    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    print(
        f"Observations: {len(gdp)}; range: {dates[0].date()} to {dates[-1].date()}; "
        f"cycle mean: {cycle_percent.mean():.6f}%; "
        f"cycle range: [{cycle_percent.min():.3f}%, {cycle_percent.max():.3f}%]"
    )


if __name__ == "__main__":
    main()
