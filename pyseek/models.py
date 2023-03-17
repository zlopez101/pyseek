from dataclasses import dataclass, field
from datetime import date
from typing import Union, List
from enum import Enum


class Form(str, Enum):
    tenk = "10-K"
    tenq = "10-Q"
    three = "3"
    four = "4"
    five = "5"
    eightk = "8-K"


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
    taxonomy: str
    tag: str

    def __str__(self):
        return f"{self.taxonomy}/{self.tag}"
