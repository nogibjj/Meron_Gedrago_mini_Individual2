"""
Extract a dataset from a URL, JSON or CSV formats tend to work well
"""

import requests
import sqlite3
import csv
import os
import time


def extract(
    url="https://github.com/fivethirtyeight/data/raw/refs/heads/master/births/US_births_2000-2014_SSA.csv",
    file_path="data/data.csv",
):
    """ "Extract a url to a file path"""

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with requests.get(url) as r:
        with open(file_path, "wb") as f:
            f.write(r.content)
    return file_path


"""Query the database"""


def read():
    """Read and print the database for all the rows of the dataBirth table"""
    conn = sqlite3.connect("birthData.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM birthData")
    # print(cursor.fetchall())
    conn.close()
    return "Successfully read!"


def create():
    """Create a fake data"""
    conn = sqlite3.connect("birthData.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO birthData VALUES ('2014','11','11','1','11')")
    conn.commit()
    conn.close()
    return "Sucessfully created!"


def update():
    """Update day of week value of 1 and set the births to 1000"""
    conn = sqlite3.connect("birthData.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE birthData SET births = '1000' WHERE day_of_week = '1';")
    conn.commit()
    conn.close()
    return "Successfully updated!"


def delete():
    """Delete rows that year is equal to 2000"""
    conn = sqlite3.connect("birthData.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM birthData WHERE year = '2000';")
    conn.commit()
    conn.close()
    return "Sucessfully deleted!"


"""
Transforms and Loads data into the local SQLite3 database
"""


# load the csv file and insert into a new sqlite3 database
def load(dataset="data/data.csv"):
    """ "Transforms and Loads data into the local SQLite3 database"""

    # prints the full working directory and path
    print(os.getcwd())
    payload = csv.reader(open(dataset, newline=""), delimiter=",")
    conn = sqlite3.connect("birthData.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS birthData ")
    c.execute("CREATE TABLE birthData (year,month, date_of_month, day_of_week, births)")
    # insert
    c.executemany("INSERT INTO birthData VALUES (?,?, ?,?,?)", payload)
    conn.commit()
    conn.close()
    return "birthData.db"


if __name__ == "__main__":
    start_time = time.time()
    extract()
    load()
    read()
    create()
    update()
    delete()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
