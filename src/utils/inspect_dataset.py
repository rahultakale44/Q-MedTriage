from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")


def inspect_csv(filename: str) -> None:
    path = DATA_DIR / filename

    print("=" * 80)
    print(f"FILE: {filename}")
    print("=" * 80)

    if not path.exists():
        print(f"File not found: {path}")
        return

    df = pd.read_csv(path)

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0].sort_values(ascending=False))

    print("\nData types:")
    print(df.dtypes)


def main() -> None:
    inspect_csv("train_cheXbert.csv")
    inspect_csv("train_visualCheXbert.csv")


if __name__ == "__main__":
    main()