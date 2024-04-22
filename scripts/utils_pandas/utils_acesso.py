import os
import pandas as pd

def le_csv(pasta_arquivo, nm_arquivo):

    caminho_arquivo = os.path.join(pasta_arquivo, nm_arquivo)

    try:
        df = pd.read_csv(caminho_arquivo, sep = ',', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(caminho_arquivo, sep = ',', encoding='latin1')
    finally:
        df['Tabela'] = nm_arquivo
    
    return df

def le_pastas_csv(lst_pastas):

    lst_dfs = []

    for pasta in lst_pastas:

        for nm_arquivo in os.listdir(pasta):
            if nm_arquivo.endswith('.csv'):
                
                df = le_csv(pasta, nm_arquivo)
                lst_dfs.append(df)

    return pd.concat(lst_dfs)
