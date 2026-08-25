import pandas as pd
from pathlib import Path


# ============================================================
# Q-MedTriage - Dataset Analysis
# ============================================================

DATA_DIR = Path("data")


def analyze_file(file_path):
    print("=" * 80)
    print(f"ANALYZING: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"\nTotal rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")

    # --------------------------------------------------------
    # Unique patients
    # --------------------------------------------------------

    patients = df["Path"].str.extract(
        r"(patient\d+)"
    )[0]

    print(f"Unique patients: {patients.nunique():,}")

    # --------------------------------------------------------
    # Unique studies
    # --------------------------------------------------------

    studies = df["Path"].str.extract(
        r"(patient\d+/study\d+)"
    )[0]

    print(f"Unique studies: {studies.nunique():,}")

    # --------------------------------------------------------
    # Image views
    # --------------------------------------------------------

    print("\nImage view distribution:")
    print(df["Frontal/Lateral"].value_counts(dropna=False))

    # --------------------------------------------------------
    # Sex distribution
    # --------------------------------------------------------

    print("\nSex distribution:")
    print(df["Sex"].value_counts(dropna=False))

    # --------------------------------------------------------
    # Age statistics
    # --------------------------------------------------------

    print("\nAge statistics:")
    print(df["Age"].describe())

    # --------------------------------------------------------
    # Pneumonia distribution
    # --------------------------------------------------------

    if "Pneumonia" in df.columns:

        print("\nPneumonia label distribution:")

        print(
            df["Pneumonia"]
            .value_counts(dropna=False)
            .sort_index()
        )

        positive = (df["Pneumonia"] == 1).sum()
        negative = (df["Pneumonia"] == 0).sum()
        uncertain = (df["Pneumonia"] == -1).sum()
        missing = df["Pneumonia"].isna().sum()

        print("\nPneumonia summary:")
        print(f"  Positive   : {positive:,}")
        print(f"  Negative   : {negative:,}")
        print(f"  Uncertain  : {uncertain:,}")
        print(f"  Missing    : {missing:,}")

    print()


def main():

    chexbert = DATA_DIR / "train_cheXbert.csv"
    visual_chexbert = DATA_DIR / "train_visualCheXbert.csv"

    analyze_file(chexbert)
    analyze_file(visual_chexbert)


if __name__ == "__main__":
    main()