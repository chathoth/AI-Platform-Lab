import csv
from pathlib import Path

def test_evaluation_dataset_exists():
    dataset = Path("evaluation/evaluation_dataset.csv")
    assert dataset.exists()
    rows = list(csv.DictReader(dataset.open()))
    assert len(rows) >= 10
