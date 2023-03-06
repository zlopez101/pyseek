from dataclasses import dataclass, field
from datetime import date
from typing import Union, List


@dataclass
class CIK:
    title: str
    ticker: str
    cik_str: str

    def __post_init__(self):
        self.cik_str = str(self.cik_str)
        while len(self.cik_str) < 10:
            self.cik_str = "0" + self.cik_str


@dataclass
class Measure:
    frame: str
    filed: date
    end: date
    form: str
    fp: str
    fy: str
    val: Union[float, int]
    accn: str


@dataclass
class Concept:
    label: str
    description: str
    units: str
    measures: List[Measure] = field(default_factory=list, repr=False)
