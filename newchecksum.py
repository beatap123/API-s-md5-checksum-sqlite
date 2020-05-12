import os

import requests
import hashlib
import csv
import zipfile


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
    checksum_local = md5Checksum("timerange.txt")   # to jest całe info z API

for i in range(1, 2):
    f = open("timerange.txt", 'r+').readlines()[18::]
    for line in f:
        if "beginposition" in line:
            file = open("%s.txt" % i, "w")
            file.write(line)
            file.close()
            md5Checksum("%s.txt" % i)
            i += 1              # tutaj dzieli to na 3 i tworzy z tego trzy pliki,które będą później usunięte

with open("results.csv", "w") as csv_file: # otwiera csv jako bazę danych
    with open("10.txt") as f:
        for line in f:
            csv_file.write(line.rstrip())
            csv_file.write(md5Checksum("10.txt"))

#
# ZIP_DIR = os.path.dirname(os.path.abspath(__file__))
# zip_path = os.path.join(ZIP_DIR, "myfolder.zip")
#
# zip_file = zipfile.ZipFile(zip_path, "w")
# zip_file.write("timerange.txt")
# zip_file.write("results.csv")
# zip_file.close()
#
mytask = os.listdir(WORK_DIR)

for item in mytask:
    if item.endswith((".txt", ".db")):
        if item.startswith("requirements"):
            pass
        else:
            os.remove(os.path.join(WORK_DIR, item))