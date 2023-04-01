from __future__ import annotations

from typing import Literal


class Datapoint:
    """
    Statistic datapoint.
    """

    timestamp: int
    loc: int = 0
    lloc: int = 0
    sloc: int = 0
    cloc: int = 0
    eloc: int = 0

    def __init__(self, timestamp):
        """
        Datapoint constructor.
        :param timestamp: The UNIX timestamp of the datapoint.
        """
        self.timestamp = timestamp

    def add(self, data: Datapoint | dict[Literal["Lines", "Code", "Comment", "Blank"], int]):
        """
        Adds the given data to this datapoint.
        :param data: The data to add.
        """
        self.loc += data["Lines"] if type(data) is dict else data.loc
        self.sloc += data["Code"] if type(data) is dict else data.sloc
        self.cloc += data["Comment"] if type(data) is dict else data.cloc
        self.eloc += data["Blank"] if type(data) is dict else data.eloc
        self.lloc = self.sloc + self.cloc
