from ast import Index
from tkinter.constants import FALSE
from typing import Union

import pandas as pd

from pandas.core.arrays import ExtensionArray


def retrieve_data_ASN(asn):

    url = "https://bgp.he.net/AS"+str(asn)  # Example URL with tables

    try:
        # read_html returns a list of DataFrames, one for each table found
        tables = pd.read_html(url)

        #print(f"Found {len(tables)} tables on the page.")

        for i, df in enumerate(tables):
            extracted_header = df.columns
            if not(isinstance(extracted_header, pd.MultiIndex)):
#                print(f"\n--- Table {i} Head ---")
#                print(df.head())
                if ("Exchange" in extracted_header.tolist()):
                    print(".")
                    df['ASN'] = str(asn)
                    desired_columns = ['ASN', 'Exchange', 'CC', 'City']
                    df_selected = df[desired_columns]
                    df_selected.to_csv(nome_file_csv_raw, sep=',', mode='a', index=False, header=False,
                                       lineterminator='',doublequote=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("This could be due to no tables found, or a network issue.")


dfAS = pd.read_csv("asn.csv")
#print(dfAS.values)

intest = ['ASN','Exchange','CC','City']
df_intestazione = pd.DataFrame(columns=intest)
nome_file_csv_raw = 'out_asn.csv'

df_intestazione.to_csv(nome_file_csv_raw,mode='w',index=False,header=True)


for j in dfAS.values.tolist():
    retrieve_data_ASN(j[0])