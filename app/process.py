import pandas as pd


DATASET_PATH = "../datasets/"
APP_INPUT_PATH = "../input/"
MAN_OPTIMIZED = "first_name_man_opti.csv"
MAN_ORIGINAL = "first_name_man_org.csv"
WOMAN_OPTIMIZED = "first_name_woman_opti.csv"
WOMAN_ORIGINAL = "first_name_woman_org.csv"

def process(dataset_path = DATASET_PATH, output_path = APP_INPUT_PATH, filename = MAN_OPTIMIZED):
    df = pd.read_csv(f"{dataset_path}{filename}", usecols=[1])

    first_names = df.drop_duplicates().sort_values(by=df.columns[0])

    first_names = first_names[first_names.iloc[:, 0].str.len() >= 3]

    first_names.to_csv(f"{output_path}{filename}", index=False, header=False)


if __name__ == "__main__":
    process()