#from ast import Index
#from tkinter.constants import FALSE
#from typing import Union

import pandas as pd

from pandas.core.arrays import ExtensionArray


def retrieve_data_company(company):

    url = "https://bgp.he.net/search?search%5Bsearch%5D="+str(company)+"&commit=Search"  # Example URL with tables

    try:
        # read_html returns a list of DataFrames, one for each table found
        tables = pd.read_html(url)

        #print(f"Found {len(tables)} tables on the page.")

        for i, df in enumerate(tables):
            extracted_header = df.columns
            if not(isinstance(extracted_header, pd.MultiIndex)):
#                print(f"\n--- Table {i} Head ---")
#                print(df.head())
                if ("Type" in extracted_header.tolist()):
                    valore_cercato = 'ASN'
                    colonna_target = 'Result'
                    colonna_ricerca = 'Type'

                    # 1. Crea la maschera booleana (True/False)
                    mask = (df[colonna_ricerca] == valore_cercato)

                    # 2. Controlla se esiste almeno un True
                    if mask.any():
                        # 3. idxmax() trova l'indice della *prima* riga True
                        primo_indice = mask.idxmax()

                        # 4. Estrai il valore con .loc[indice, colonna] (molto veloce)
                        risultato = df.loc[primo_indice, colonna_target]
                        df_selected = pd.DataFrame([{'Company': company, 'ASN': risultato}])

                        df_selected.to_csv(nome_file_csv_raw, sep=',', mode='a', index=False, header=False,
                                           lineterminator='', doublequote=True)
                        print(".")


    except Exception as e:
        print(f"An error occurred: {e}")
        print("This could be due to no tables found, or a network issue.")


dfAS = pd.read_csv("company.csv")
#print(dfAS.values)

intest = ['Company','ASN']
df_intestazione = pd.DataFrame(columns=intest)
nome_file_csv_raw = 'out_asn_company.csv'

df_intestazione.to_csv(nome_file_csv_raw,mode='w',index=False,header=True)


for j in dfAS.values.tolist():
    retrieve_data_company(j[0])