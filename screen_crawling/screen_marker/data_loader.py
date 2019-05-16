from collections import namedtuple
from json import loads


PageData = namedtuple(
    "PageData", ["url", "mark_class", "destroy_classes", "hide_classes"]
)


def load_data(filename):
    with open(filename, "rt") as file:
        return [PageData(**loads(raw)) for raw in file.readlines()]
