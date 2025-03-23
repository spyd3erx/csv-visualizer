import pandas as pd
from dataclasses import dataclass

@dataclass
class DataAnalyst:
    data: pd.DataFrame
    filename: str
    error: str = None
