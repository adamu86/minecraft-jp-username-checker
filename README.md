# Minecraft Japanese Username Checker

A tool for checking the availability of Minecraft usernames generated from Japanese first names. It uses the [Mojang API](https://api.mojang.com) to verify whether a given username is taken or free to register.

---

## How it works

The pipeline consists of two scripts:

**`process.py`** — Reads a CSV dataset of Japanese first names, removes duplicates, filters out names shorter than 3 characters, and saves a clean list to the `input/` directory.

**`check.py`** — Takes the processed list and checks each username against the Mojang API. Available usernames are printed in green and saved to a `.txt` file. Taken names are printed in red. Network errors trigger automatic retries.

---

## Project structure

```
project/
├── app/               # Scripts (process.py, check.py)
├── datasets/          # Raw CSV files from the source dataset
├── input/             # Processed name lists (output of process.py)
└── output/            # Available username results (output of check.py)
```

---

## Dataset

Names are sourced from the [japanese-personal-name-dataset](https://github.com/shuheilocale/japanese-personal-name-dataset) by shuheilocale — a dataset of Japanese personal names in hiragana, romaji, and kanji.

The dataset contains:

| File | Description | Count |
|------|-------------|-------|
| `first_name_man_org.csv` | All male first names | 5,678 |
| `first_name_man_opti.csv` | Popular male first names only | 703 |
| `first_name_woman_org.csv` | All female first names | 3,346 |
| `first_name_woman_opti.csv` | Popular female first names only | 241 |

The scripts use the **romaji column** (column index 1) from these CSV files. The "optimized" variants are curated by the dataset author and contain only the more commonly used names.

Dataset license: [MIT](https://github.com/shuheilocale/japanese-personal-name-dataset/blob/main/LICENSE)

---

## Requirements

```
pip install requests tqdm
```

Python 3.8+. The `check.py` script will attempt to auto-install dependencies if they are missing.

---

## Usage

**Step 1 — Process the dataset:**

```bash
python process.py
```

This reads `datasets/first_name_man_opti.csv` by default and writes a cleaned list to `input/first_name_man_opti.csv`.

To process a different file, call `process()` with custom arguments:

```python
from process import process
process(filename="first_name_woman_opti.csv")
```

**Step 2 — Check availability:**

Open `check.py` and set the `filepath` variable to point at the file you want to check. By default it uses the optimized male names list:

```python
filepath = f"{APP_INPUT_PATH}{MAN_OPTIMIZED}"
```

Swap `MAN_OPTIMIZED` for `MAN_ORIGINAL`, `WOMAN_OPTIMIZED`, or `WOMAN_ORIGINAL` depending on which list you want to process. Then run:

```bash
python check.py
```

Results are saved to `output/` with the filename based on the input file (e.g. `first_name_man_opti_available.txt`).

---

## API reference

Username availability is checked against:

```
GET https://api.mojang.com/users/profiles/minecraft/{username}
```

| Status code | Meaning |
|-------------|---------|
| `200` | Username is taken |
| `204` / `404` | Username is available |
| `429` | Rate limited — script waits 15s and retries |

---

## Notes

- Minecraft usernames are case-insensitive, 3–16 characters long, and allow only letters, digits, and underscores. Names shorter than 3 characters are filtered out by `process.py`.
- The "optimized" dataset variants are a good starting point — 703 male and 241 female names is manageable to check in a single run without hitting rate limits too aggressively.
- Output files are appended to, not overwritten, so re-running the checker on a partially completed list will duplicate results for any names checked twice.