'''
Fa lo scraping di PeeringDB a partire dall'ID dell IXP
'''


import requests
import pandas as pd
import time

# Configurazione
API_KEY = "S5PPmhCP.dZxSiElpB3SNoLoXua2uYJ3ADi4ggnrs"
headers = {"Authorization": f"Api-Key {API_KEY}"}
nome_file_csv_raw = 'out_asn_peeringDB.csv'

def retrieve_data_company(IX_id):
    # Assicuriamoci che IX_id sia una stringa pulita per l'URL
    clean_id = str(IX_id).strip()
    url = f"https://www.peeringdb.com/api/net?ix={clean_id}&not_ix=121"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_res = response.json()
        networks = json_res.get('data', [])

        if networks:
            for net in networks:
                # Mappatura campi JSON PeeringDB con IX_id in prima posizione
                riga = {
                    'IX_id': clean_id,
                    'Name': net.get('name', ''),
                    'Also known as': net.get('aka', ''),
                    'ASN': net.get('asn', ''),
                    'General Policy': net.get('policy_general', ''),
                    'Network Type': net.get('info_type', ''),
                    'Network Scope': net.get('info_scope', ''),
                    'Traffic Levels': net.get('info_traffic', ''),
                    'Traffic Ratio': net.get('info_ratio', ''),
                    'Exchanges': net.get('ix_count', ''),
                    'Facilities': net.get('fac_count', '')
                }

                df_row = pd.DataFrame([riga])
                # Salvataggio in append con separatore ";"
                df_row.to_csv(
                    nome_file_csv_raw,
                    mode='a',
                    index=False,
                    header=False,
                    sep=';',
                    encoding='utf-8',
                    lineterminator='\n'
                )
            print(f"ID {clean_id}: salvati {len(networks)} record.")
        else:
            print(f"ID {clean_id}: nessun dato trovato.")

    except Exception as e:
        print(f"Errore su ID {IX_id}: {e}")

# --- MAIN ---

# 1. Inizializzazione del file di output con IX_id come prima colonna
intest = ['IX_id', 'Name', 'Also known as', 'ASN', 'General Policy', 'Network Type',
          'Network Scope', 'Traffic Levels', 'Traffic Ratio', 'Exchanges', 'Facilities']

pd.DataFrame(columns=intest).to_csv(
    nome_file_csv_raw,
    mode='w',
    index=False,
    header=True,
    sep=';',
    encoding='utf-8',
    lineterminator='\n'
)

# 2. Lettura del file sorgente senza header
try:
    # header=None per non saltare la prima riga del file
    df_ix = pd.read_csv("ixp_PeeringDB.csv", header=None, names=['id'])

    # 3. Ciclo sugli ID presenti nel file
    for val in df_ix['id']:
        if pd.notna(val):
            retrieve_data_company(val)
            # Pausa di sicurezza per i limiti dell'API
            time.sleep(0.5)

except FileNotFoundError:
    print("Errore: il file ixp_PeeringDB.csv non è stato trovato.")