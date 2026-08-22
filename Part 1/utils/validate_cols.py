from typing import List, Dict
import csv 
import re

def validate_expected_cols(
    source_csv:str,
    datasets_config
):
    '''
    Args:
        source_csv: pass the disk location of the downloaded csv file
        datasets_config: a dict containing an array of strings of expected cols.
    Returns:
        empty list if all expected cols are in the csv, else returns which cols are missing 
    '''
    match = re.search(r"raw/(.*)\.csv",source_csv)
    filename = match.group(1)
    
    with open(source_csv, mode="r", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers: List[str] = next(reader)
        print(f"Extracted headers from {filename}: {headers}.")
    
    expected = datasets_config[filename]["expected_cols"]
    missing_cols: List = []
    for col in expected:
        if col not in headers:
            missing_cols.append(col)
    
    if missing_cols:
        raise AssertionError(f"Missing cols from {filename}: {missing_cols}")
    print(f"All expected columns present in {filename}.")