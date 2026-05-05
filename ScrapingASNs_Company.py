#from ast import Index
#from tkinter.constants import FALSE
#from typing import Union

import pandas as pd

from pandas.core.arrays import ExtensionArray
from thefuzz import fuzz


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
                        campi_da_filtrare = ['Description',colonna_target]
                        df_filtrato = df.loc[mask,campi_da_filtrare]
                        primo_indice = mask.idxmax()
                        comp_he = df.loc[primo_indice, "Description"]
                        re_fuzzy = fuzz.token_set_ratio(company, comp_he)
                        risultato = df.loc[primo_indice, colonna_target]

                        for indice_riga, riga in df_filtrato.iterrows():
                            comp_he_temp = df_filtrato.loc[indice_riga,"Description"]
                            re_fuzzy_temp = fuzz.token_set_ratio(company, comp_he_temp)
                            if re_fuzzy_temp > re_fuzzy:
                                comp_he = comp_he_temp
                                re_fuzzy=re_fuzzy_temp
                                risultato = df_filtrato.loc[indice_riga,colonna_target]




                        # 4. Estrai il valore con .loc[indice, colonna] (molto veloce)


                        df_selected = pd.DataFrame([{'Company': company, 'ASN': risultato, 'Company_HE': comp_he, 'Punteggio':re_fuzzy}])

                        df_selected.to_csv(nome_file_csv_raw, sep=',', mode='a', index=False, header=False,
                                           lineterminator='', doublequote=True)
                        print(".")


    except Exception as e:
        print(f"An error occurred: {e}")
        print("This could be due to no tables found, or a network issue.")


dfAS = pd.read_csv("company.csv")
#print(dfAS.values)

intest = ['Company','ASN','Company_HE','Punteggio']
df_intestazione = pd.DataFrame(columns=intest)
nome_file_csv_raw = 'out_asn_company.csv'

df_intestazione.to_csv(nome_file_csv_raw,mode='w',index=False,header=True)


for j in dfAS.values.tolist():
    retrieve_data_company(j[0])