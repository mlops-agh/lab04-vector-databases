from datasets import Dataset, load_dataset

COLUMNS_TO_KEEP = [
    "name",
    "windows",
    "linux",
    "mac",
    "detailed_description",
    "supported_languages",
    "price",
]


def load_games(n: int) -> Dataset:
    """Load the first `n` rows of the Steam games dataset with only the columns we need."""
    dataset = load_dataset("FronkonGames/steam-games-dataset")["train"]
    return dataset.select_columns(COLUMNS_TO_KEEP).select(range(n))
