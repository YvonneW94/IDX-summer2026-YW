"""Week 7: Outlier Detection and Data Quality.

This script applies the Interquartile Range (IQR) method to key numeric
fields in the feature-engineered Sold dataset. It preserves every source
record in a flagged output and also creates a separate filtered dataset for
analysis and Tableau development.


"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


IQR_COLUMNS = ["ClosePrice", "LivingArea", "DaysOnMarket"]
IQR_MULTIPLIER = 1.5


def parse_arguments() -> argparse.Namespace:
    """Read optional command-line paths."""
    parser = argparse.ArgumentParser(
        description="Apply Week 7 IQR outlier detection to Sold MLS data."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Path to feature_engineered_sold.csv.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for Week 7 output files.",
    )
    return parser.parse_args()


def locate_default_input() -> Path:
    """Find the standard Week 6 Sold output from common project locations."""
    script_dir = Path(__file__).resolve().parent
    working_dir = Path.cwd().resolve()

    candidates = [
        script_dir.parent / "outputs" / "feature_engineered_sold.csv",
        script_dir / "feature_engineered_sold.csv",
        working_dir / "outputs" / "feature_engineered_sold.csv",
        working_dir.parent / "outputs" / "feature_engineered_sold.csv",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    candidate_text = "\n".join(f"- {path}" for path in candidates)
    raise FileNotFoundError(
        "Could not find feature_engineered_sold.csv. Checked:\n"
        f"{candidate_text}\n"
        "Provide the file explicitly with --input."
    )


def validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Confirm required fields and convert them to numeric values."""
    missing_columns = [column for column in IQR_COLUMNS if column not in df.columns]
    if missing_columns:
        raise KeyError(f"Input dataset is missing required columns: {missing_columns}")

    prepared = df.copy()
    for column in IQR_COLUMNS:
        prepared[column] = pd.to_numeric(prepared[column], errors="coerce")

    return prepared


def add_iqr_flag(
    df: pd.DataFrame,
    column: str,
    multiplier: float = IQR_MULTIPLIER,
) -> tuple[pd.DataFrame, dict[str, float | int | str]]:
    """Add an IQR outlier flag and return the calculated field statistics."""
    valid_values = df[column].dropna()
    if valid_values.empty:
        raise ValueError(f"{column} contains no valid numeric values.")

    q1 = valid_values.quantile(0.25)
    q3 = valid_values.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    flag_column = f"{column}_IQR_Outlier"
    df[flag_column] = (
        df[column].notna()
        & ((df[column] < lower_bound) | (df[column] > upper_bound))
    )

    statistics = {
        "Field": column,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Multiplier": multiplier,
        "LowerBound": lower_bound,
        "UpperBound": upper_bound,
        "NonMissingValues": int(valid_values.size),
        "IQROutlierCount": int(df[flag_column].sum()),
    }
    return df, statistics


def add_business_rule_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flag values that are invalid regardless of their statistical range."""
    flagged = df.copy()

    flagged["ClosePrice_Invalid"] = (
        flagged["ClosePrice"].notna() & flagged["ClosePrice"].le(0)
    )
    flagged["LivingArea_Invalid"] = (
        flagged["LivingArea"].notna() & flagged["LivingArea"].le(0)
    )
    flagged["DaysOnMarket_Invalid"] = (
        flagged["DaysOnMarket"].notna() & flagged["DaysOnMarket"].lt(0)
    )

    business_rule_columns = [
        "ClosePrice_Invalid",
        "LivingArea_Invalid",
        "DaysOnMarket_Invalid",
    ]
    flagged["Any_Business_Rule_Invalid"] = flagged[business_rule_columns].any(axis=1)
    return flagged


def create_comparison(
    before: pd.DataFrame,
    after: pd.DataFrame,
) -> pd.DataFrame:
    """Compare dataset size and median values before and after filtering."""
    comparison_rows = [
        {
            "Metric": "Row Count",
            "BeforeFiltering": len(before),
            "AfterFiltering": len(after),
        }
    ]

    for column in IQR_COLUMNS:
        comparison_rows.append(
            {
                "Metric": f"Median {column}",
                "BeforeFiltering": before[column].median(),
                "AfterFiltering": after[column].median(),
            }
        )

    comparison = pd.DataFrame(comparison_rows)
    comparison["AbsoluteChange"] = (
        comparison["AfterFiltering"] - comparison["BeforeFiltering"]
    )
    comparison["PercentChange"] = np.where(
        comparison["BeforeFiltering"].ne(0),
        comparison["AbsoluteChange"] / comparison["BeforeFiltering"],
        np.nan,
    )
    return comparison


def main() -> None:
    """Run the complete Week 7 workflow and export all deliverables."""
    args = parse_arguments()

    input_path = args.input.resolve() if args.input else locate_default_input()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else input_path.parent
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("WEEK 7: OUTLIER DETECTION AND DATA QUALITY")
    print("=" * 70)
    print("Input:", input_path)
    print("Output directory:", output_dir)

    sold = pd.read_csv(input_path, low_memory=False)
    sold = validate_and_prepare(sold)
    original_row_count = len(sold)

    print(f"\nLoaded Sold dataset: {sold.shape[0]:,} rows x {sold.shape[1]} columns")

    iqr_statistics = []
    for column in IQR_COLUMNS:
        sold, statistics = add_iqr_flag(sold, column)
        iqr_statistics.append(statistics)
        print(
            f"{column}: {statistics['IQROutlierCount']:,} IQR outliers "
            f"outside [{statistics['LowerBound']:,.2f}, "
            f"{statistics['UpperBound']:,.2f}]"
        )

    iqr_flag_columns = [f"{column}_IQR_Outlier" for column in IQR_COLUMNS]
    sold["Any_IQR_Outlier"] = sold[iqr_flag_columns].any(axis=1)

    sold = add_business_rule_flags(sold)
    sold["Exclude_From_Analysis"] = (
        sold["Any_IQR_Outlier"] | sold["Any_Business_Rule_Invalid"]
    )

    sold_filtered = sold.loc[~sold["Exclude_From_Analysis"]].copy()

    if len(sold) != original_row_count:
        raise AssertionError("Flagging unexpectedly changed the full dataset row count.")
    if sold_filtered["Exclude_From_Analysis"].any():
        raise AssertionError("Filtered dataset still contains excluded records.")

    comparison = create_comparison(sold, sold_filtered)
    bounds = pd.DataFrame(iqr_statistics)

    flagged_path = output_dir / "week7_sold_flagged.csv"
    filtered_path = output_dir / "week7_sold_filtered.csv"
    comparison_path = output_dir / "week7_before_after_comparison.csv"
    bounds_path = output_dir / "week7_iqr_bounds.csv"

    sold.to_csv(flagged_path, index=False)
    sold_filtered.to_csv(filtered_path, index=False)
    comparison.to_csv(comparison_path, index=False)
    bounds.to_csv(bounds_path, index=False)

    excluded_count = int(sold["Exclude_From_Analysis"].sum())
    excluded_percent = excluded_count / len(sold) if len(sold) else np.nan

    print("\nFiltering summary")
    print("-" * 70)
    print(f"Full flagged records: {len(sold):,}")
    print(f"Excluded from analysis: {excluded_count:,} ({excluded_percent:.2%})")
    print(f"Clean filtered records: {len(sold_filtered):,}")
    print("\nBefore-and-after comparison:")
    print(comparison.to_string(index=False))

    print("\nExported files")
    print("-" * 70)
    for path in (flagged_path, filtered_path, comparison_path, bounds_path):
        print(path)


if __name__ == "__main__":
    main()
