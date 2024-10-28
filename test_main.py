"""
Test goes here

"""

from main import extract
from main import load
from main import read, create, update, delete


def test_extract():
    assert extract() == "data/data.csv"


def test_transform():
    assert load() == "birthData.db"


def test_create():
    assert create() == "Sucessfully created!"


def test_read():
    assert read() == "Successfully read!"


def test_update():
    assert update() == "Successfully updated!"


def test_delete():
    assert delete() == "Sucessfully deleted!"


if __name__ == "__main__":
    test_extract()
    test_transform()
    test_create()
    test_read()
    test_update()
    test_delete()
    print("Everything passed")
