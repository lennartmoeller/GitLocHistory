from __future__ import annotations

from typing import Literal


class Datapoint:
    """
    Statistic datapoint.
    """

    timestamp: int
    lines: int = 0
    code: int = 0
    comment: int = 0
    blank: int = 0
    wcomplexity: int = 0

    def __init__(self, timestamp):
        """
        Datapoint constructor.
        :param timestamp: The UNIX timestamp of the datapoint.
        """
        self.timestamp = timestamp

    def add(self, data: Datapoint | dict[Literal["Lines", "Code", "Comment", "Blank", "WeightedComplexity"], int]):
        """
        Adds the given data to this datapoint.
        :param data: The data to add.
        """
        self.lines += data["Lines"] if type(data) is dict else data.lines
        self.code += data["Code"] if type(data) is dict else data.code
        self.comment += data["Comment"] if type(data) is dict else data.comment
        self.blank += data["Blank"] if type(data) is dict else data.blank
        self.wcomplexity += data["WeightedComplexity"] if type(data) is dict else data.wcomplexity
