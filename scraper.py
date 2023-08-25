import pandas as pd
from bs4 import BeautifulSoup
from requests import get


def downloadXls(cetip, id):
    response = get("https://www.ecoagro.agr.br/excel-historico-pu/" + id + '/' + cetip)
    with open(cetip + '.xls', 'wb') as out:
        out.write(response.content)
        out.close()
    return pd.read_html(response.content, header=0)

def cleanTable(df):
    df["Data"] = df['Data'].str.replace('.','/', regex=False)
    df = df.loc[::-1].reset_index(drop=True)
    return df

def getId(cetip):
    url = "https://www.ecoagro.agr.br/emissoes?pesquisa=" + cetip
    response = get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all("tr")

    for row in rows:
        fields = row.find_all('td')
        for field in fields:
            if field.text.find(cetip) != -1:
                return row['data-id']

cetip = input("CETIP do fundo: ")

id = getId(cetip)

df = downloadXls(cetip, id)

print(df)

df = cleanTable(df)

df.to_csv(cetip + ".csv", index=False)
