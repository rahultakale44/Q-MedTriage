import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


# ============================================================
# Q-MedTriage - Dataset Preprocessing
# ============================================================

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Input / output paths
DATA_DIR = PROJECT_ROOT / "data"

CHEXBERT_FILE = DATA_DIR / "train_cheXbert.csv"
VISUAL_CHEXBERT_FILE = DATA_DIR / "train_visualCheXbert.csv"

PROCESSED_DIR = DATA_DIR / "processed"


# Reproducibility
RANDOM_STATE = 42


def load_dataset(file_path):
    """Load dataset from CSV."""

    print("=" * 80)
    print(f"Loading: {file_path.name}")
    print("=" * 80)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    return df


def clean_dataset(df):
    """Clean and prepare dataset."""

    print("\n" + "=" * 80)
    print("CLEANING DATASET")
    print("=" * 80)

    df = df.copy()

    # --------------------------------------------------------
    # Remove rows without required patient information
    # --------------------------------------------------------

    before = len(df)

    df = df.dropna(
        subset=[
            "Path",
            "Sex",
            "Age",
            "Frontal/Lateral"
        ]
    )

    print(
        f"Removed rows with missing basic information: "
        f"{before - len(df):,}"
    )

    # --------------------------------------------------------
    # Create patient ID
    # --------------------------------------------------------

    df["Patient_ID"] = (
        df["Path"]
        .str.extract(r"(patient\d+)", expand=False)
    )

    missing_patient_ids = df["Patient_ID"].isna().sum()

    print(f"Missing patient IDs: {missing_patient_ids:,}")

    df = df.dropna(subset=["Patient_ID"])

    # --------------------------------------------------------
    # Create Study ID
    # --------------------------------------------------------

    df["Study_ID"] = (
        df["Path"]
        .str.extract(
            r"(patient\d+/study\d+)",
            expand=False
        )
    )

    # --------------------------------------------------------
    # Normalize pneumonia labels
    # --------------------------------------------------------

    if "Pneumonia" in df.columns:

        # Original CheXbert labels:
        #
        # 1  = Positive
        # 0  = Negative
        # -1 = Uncertain
        # NaN = Missing
        #
        # For the initial binary classification pipeline,
        # we keep only definite positive / negative samples.

        df["Pneumonia_Label"] = df["Pneumonia"].map({
            0.0: 0,
            1.0: 1
        })

        before_label_filter = len(df)

        df = df.dropna(
            subset=["Pneumonia_Label"]
        )

        print(
            "Removed uncertain/missing pneumonia labels: "
            f"{before_label_filter - len(df):,}"
        )

        df["Pneumonia_Label"] = (
            df["Pneumonia_Label"]
            .astype(int)
        )

    # --------------------------------------------------------
    # Reset index
    # --------------------------------------------------------

    df = df.reset_index(drop=True)

    print(f"Rows after cleaning: {len(df):,}")

    return df


def create_patient_level_split(df):
    """
    Create train/validation/test splits at patient level.

    This prevents images from the same patient appearing
    in multiple splits.
    """

    print("\n" + "=" * 80)
    print("CREATING PATIENT-LEVEL SPLIT")
    print("=" * 80)

    # --------------------------------------------------------
    # Get unique patients
    # --------------------------------------------------------

    patients = df["Patient_ID"].unique()

    print(f"Total unique patients: {len(patients):,}")

    # --------------------------------------------------------
    # Train: 80%
    # Temporary: 20%
    # --------------------------------------------------------

    train_patients, temp_patients = train_test_split(
        patients,
        test_size=0.20,
        random_state=RANDOM_STATE
    )

    # --------------------------------------------------------
    # Validation: 10%
    # Test: 10%
    # --------------------------------------------------------

    val_patients, test_patients = train_test_split(
        temp_patients,
        test_size=0.50,
        random_state=RANDOM_STATE
    )

    print(f"Train patients      : {len(train_patients):,}")
    print(f"Validation patients : {len(val_patients):,}")
    print(f"Test patients       : {len(test_patients):,}")

    # --------------------------------------------------------
    # Create masks
    # --------------------------------------------------------

    train_set = set(train_patients)
    val_set = set(val_patients)
    test_set = set(test_patients)

    train_df = df[
        df["Patient_ID"].isin(train_set)
    ].copy()

    val_df = df[
        df["Patient_ID"].isin(val_set)
    ].copy()

    test_df = df[
        df["Patient_ID"].isin(test_set)
    ].copy()

    # --------------------------------------------------------
    # Add split column
    # --------------------------------------------------------

    train_df["Split"] = "train"
    val_df["Split"] = "validation"
    test_df["Split"] = "test"

    # --------------------------------------------------------
    # Display statistics
    # --------------------------------------------------------

    print("\nImage distribution:")
    print(f"Train      : {len(train_df):,}")
    print(f"Validation : {len(val_df):,}")
    print(f"Test       : {len(test_df):,}")

    print("\nPneumonia distribution:")

    for name, split_df in [
        ("Train", train_df),
        ("Validation", val_df),
        ("Test", test_df)
    ]:

        print(f"\n{name}:")

        print(
            split_df["Pneumonia_Label"]
            .value_counts()
            .sort_index()
            .rename({
                0: "Negative",
                1: "Positive"
            })
        )

    return train_df, val_df, test_df


def verify_patient_leakage(
    train_df,
    val_df,
    test_df
):
    """Verify that patients do not overlap."""

    print("\n" + "=" * 80)
    print("CHECKING FOR PATIENT LEAKAGE")
    print("=" * 80)

    train_patients = set(
        train_df["Patient_ID"]
    )

    val_patients = set(
        val_df["Patient_ID"]
    )

    test_patients = set(
        test_df["Patient_ID"]
    )

    train_val = train_patients & val_patients
    train_test = train_patients & test_patients
    val_test = val_patients & test_patients

    print(
        f"Train ∩ Validation: {len(train_val)}"
    )

    print(
        f"Train ∩ Test      : {len(train_test)}"
    )

    print(
        f"Validation ∩ Test : {len(val_test)}"
    )

    if train_val or train_test or val_test:

        raise RuntimeError(
            "PATIENT LEAKAGE DETECTED!"
        )

    print("\n✓ No patient leakage detected.")


def save_splits(
    train_df,
    val_df,
    test_df
):
    """Save processed datasets."""

    print("\n" + "=" * 80)
    print("SAVING PROCESSED DATA")
    print("=" * 80)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    train_path = (
        PROCESSED_DIR /
        "train.csv"
    )

    val_path = (
        PROCESSED_DIR /
        "validation.csv"
    )

    test_path = (
        PROCESSED_DIR /
        "test.csv"
    )

    train_df.to_csv(
        train_path,
        index=False
    )

    val_df.to_csv(
        val_path,
        index=False
    )

    test_df.to_csv(
        test_path,
        index=False
    )

    print(f"Saved: {train_path}")
    print(f"Saved: {val_path}")
    print(f"Saved: {test_path}")


def main():

    print("\n")
    print("=" * 80)
    print("Q-MEDTRIAGE DATA PREPROCESSING PIPELINE")
    print("=" * 80)

    # --------------------------------------------------------
    # Load VisualCheXbert
    # --------------------------------------------------------

    df = load_dataset(
        VISUAL_CHEXBERT_FILE
    )

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    df = clean_dataset(df)

    # --------------------------------------------------------
    # Patient-level split
    # --------------------------------------------------------

    train_df, val_df, test_df = (
        create_patient_level_split(df)
    )

    # --------------------------------------------------------
    # Verify leakage
    # --------------------------------------------------------

    verify_patient_leakage(
        train_df,
        val_df,
        test_df
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_splits(
        train_df,
        val_df,
        test_df
    )

    print("\n" + "=" * 80)
    print("PREPROCESSING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()