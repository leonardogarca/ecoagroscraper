import pandas as pd
from bs4 import BeautifulSoup
from requests import get

def getTable(cetip, id):
    url = "https://www.ecoagro.agr.br/historico-pu/" + id + '/' + cetip
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    table = html_soup.find('table', class_="current__table")

    table_head = table.find('thead')
    headers = table_head.find_all('th')

    out_headers = []

    for header in headers:
        out_headers.append(header.text)

    out = []

    rows = table.find_all("tr")

    for row in rows:
        fields = row.find_all('td')
        out_row = []
        for field in fields:
            out_row.append(field.text)
        out.append(out_row)

    df = pd.DataFrame(out, columns=out_headers)
    return df

def downloadXlsBackup(cetip, id):
    response = get("https://www.ecoagro.agr.br/excel-historico-pu/129/CRA0190066O")
    with open(cetip + '.xls', 'wb') as out:
        out.write(response.content)

def cleanTable(df):
    df["Data"] = df['Data'].str.replace('.','/')
    df["Data"] = df['Data'].str[3:6] + df['Data'].str[0:3] + df['Data'].str[6:]
    df = df.loc[::-1].reset_index(drop=True)
    return df

def getId(cetip):
    url = "https://www.ecoagro.agr.br/emissoes?pesquisa=" + cetip
    response = get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    elements = soup.find_all(attrs={"data-id":True})
    if len(elements) != 1:
        print("deu ruim")
        return
    else:
        return elements[0]['data-id']

cetip = input("CETIP do fundo: ")

id = getId(cetip)

df = getTable(cetip, id)

df = cleanTable(df)

df.to_csv(cetip + ".csv", index=False)

downloadXlsBackup(cetip, id)