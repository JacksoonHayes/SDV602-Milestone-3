"""
Download ?
"""
# https://newsimland.com/~todd/hs21.csv
# 
# https://www.rbnz.govt.nz/-/media/ReserveBank/Files/Statistics/tables/c21/hc21.xlsx?revision=466b2f49-b480-447e-9d1d-9461589d722c

def Answer1():
    import csv
    from urllib.request import urlopen

    url = 'https://newsimland.com/~todd/hs21.csv'
    #response = urlopen(url)
    #cr = csv.reader(response)


def Answer2():
    import pandas as pd
    data = pd.read_csv('https://newsimland.com/~todd/hs21.csv')
    print(data)

def Answer3():
    import requests
    import csv
    url = 'https://newsimland.com/~todd/hs21.csv'
    r = requests.get(url)
    text = r.iter_content
    print(text)
    #reader = csv.reader(text, delimiter=',')
    #for row in reader:
    #    print(row)


Answer2()


