""" Utils for load data from json format and transform to PageData. """
from collections import namedtuple
from json import loads


PageData = namedtuple(
    "PageData", ["url", "mark_class", "destroy_classes", "hide_classes"]
)


def load_data(filename):
    """ Load PageData from json nextline separate examples """
    with open(filename, "rt") as file:
        return [PageData(**loads(raw)) for raw in file.readlines()]
