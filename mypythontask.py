import os

import requests
import hashlib
import sqlite3
import csv
import zipfile

from task import main


def md5Checksum(filePath):
    """Return the md5 checksum of file"""
    m = hashlib.md5()
    with open(filePath, "rb") as fh:
        m = hashlib.md5()
        while True:
            data = fh.readline(8192)
            m.update(data)
            if not data:
                break
        return m.hexdigest()


url = "https://scihub.copernicus.eu/dhus/search?q=beginposition:%5BNOW-4DAYS%20TO%20NOW%5D%20AND%20producttype:SLC&rows=3&start=0"

username = "coahbp"
password = "admin123"

parameters = {"rows": 3,
              "start": 0,
              }

r = requests.get(url, auth=(username, password), params=parameters)
r.encoding = "utf-8"

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(WORK_DIR)

if r.status_code == requests.codes.ok:
    file = open(os.path.join(file_path, "timerange.txt"), "wb")
    file.write(r.content)
    file.close()
    checksum_local = md5Checksum("timerange.txt")

for i in range(1, 2):
    f = open("timerange.txt", 'r+').readlines()[18::]
    for line in f:
        if "beginposition" in line:
            file = open("%s.txt" % i, "w")
            file.write(line)
            file.close()
            md5Checksum("%s.txt" % i)
            i += 1

main()
db_path = os.path.join(WORK_DIR, "pythonsqlite.db")
try:
    sqliteConnection = sqlite3.connect(db_path)
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    filename = ["timerange.txt", "1.txt", "2.txt", "3.txt"]
    for item in filename:
        path = os.path.abspath(item)
        checksum = md5Checksum(item)
        mylist = (item, path, checksum)
        count = cursor.execute('INSERT INTO projects (filename, path, md5sum) VALUES (?,?,?)', (mylist))
        sqliteConnection.commit()
        print("Record inserted successfully into pythonsqlite table ", cursor.rowcount)

    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM projects")
    with open("results.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(cursor)
    cursor.close()
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table:", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")

ZIP_DIR = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(ZIP_DIR, "myfolder.zip")

zip_file = zipfile.ZipFile(zip_path, "w")
zip_file.write("timerange.txt")
zip_file.write("results.csv")
zip_file.close()

mytask = os.listdir(WORK_DIR)

for item in mytask:
    if item.endswith((".txt", ".db", ".csv")):
        if item.startswith("requirements"):
            pass
        else:
            os.remove(os.path.join(WORK_DIR, item))
