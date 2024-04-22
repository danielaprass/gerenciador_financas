import pandas as pd
import numpy as np

from typing import Dict, Any, Optional
from pandas.core.frame import DataFrame

from modulos.utils_pandas.utils_operacoes import padronizar_string


def converter_tipo_cols(df: DataFrame, dic_dtypes: Dict[str, str]) -> DataFrame:
    """
    Converte os tipos de colunas em um DataFrame de acordo com o dicionário de tipos fornecido.

    Args:
        df (DataFrame): DataFrame a ser modificado.
        dic_dtypes (Dict[str, str]): Dicionário onde as chaves são os tipos de dados desejados e os valores
            são os nomes das colunas a serem convertidas para esses tipos.

    Returns:
        DataFrame: DataFrame com as colunas convertidas para os tipos especificados.
    """
    novo_df = df.copy()

    for tp, lst_cols in dic_dtypes.items():
        novo_df[lst_cols] = novo_df[lst_cols].astype(tp)
        
    return novo_df


def mapeia_valores(df: DataFrame, col_mapeada: str, dic_mapeamento: Dict[Any, Any], nm_col_criada: Optional[str] = None) -> DataFrame:
    """
    Mapeia valores de uma coluna em um DataFrame pandas de acordo com um dicionário de mapeamento.

    Parâmetros:
        - df: DataFrame pandas.
        - col_mapeada: Nome da coluna a ser mapeada.
        - dic_mapeamento: Dicionário de mapeamento de valores.

    Retorno:
        - DataFrame pandas com os valores mapeados na coluna especificada.
    """
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = col_mapeada

    novo_df[nm_col_criada] = novo_df[col_mapeada].map(dic_mapeamento)
    return novo_df


def corrigir_valores_col(df: DataFrame, nm_col_corrigida: str, dic_correcao: Dict[str, str], nm_col_criada: Optional[str] = None) -> pd.DataFrame:
    """
    Corrige valores de uma coluna em um DataFrame.

    Args:
        nm_col_corrigida (str): Nome da coluna a ser corrigida.
        dic_correcao (Dict[str, str]): Dicionário contendo os valores a serem corrigidos.
        nm_col_criada (Optional[str], optional): Nome da nova coluna a ser criada. Se não fornecido,
            uma nova coluna será criada com o prefixo 'n_' seguido do nome da coluna original. Default é None.

    Returns:
        pd.DataFrame: DataFrame com os valores corrigidos.
    """
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = nm_col_corrigida

    novo_df[nm_col_criada] = novo_df[nm_col_corrigida].replace(dic_correcao)

    return novo_df

def preencher_ausentes_cols(df, lst_cols, vlr_preenchido):
    
    novo_df = df.copy()
    
    novo_df[lst_cols] = novo_df[lst_cols].fillna(vlr_preenchido)

    return novo_df


def corrigir_valores_col(df, nm_col_corrigida, dic_correcao, nm_col_criada = None):
    """
    Corrige valores de uma coluna em um DataFrame.

    Args:
        nm_col_corrigida (str): Nome da coluna a ser corrigida.
        dic_correcao (Dict[str, str]): Dicionário contendo os valores a serem corrigidos.
        nm_col_criada (Optional[str], optional): Nome da nova coluna a ser criada. Se não fornecido,
            uma nova coluna será criada com o prefixo 'n_' seguido do nome da coluna original. Default é None.

    Returns:
        pd.DataFrame: DataFrame com os valores corrigidos.
    """
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = nm_col_corrigida

    novo_df[nm_col_criada] = novo_df[nm_col_corrigida].astype('str').replace(dic_correcao)

    return novo_df


def converter_tipo_cols(df, dic_dtypes):
    """
    Converte os tipos de colunas em um DataFrame de acordo com o dicionário de tipos fornecido.

    Args:
        df (DataFrame): DataFrame a ser modificado.
        dic_dtypes (Dict[str, str]): Dicionário onde as chaves são os tipos de dados desejados e os valores
            são os nomes das colunas a serem convertidas para esses tipos.

    Returns:
        DataFrame: DataFrame com as colunas convertidas para os tipos especificados.
    """
    novo_df = df.copy()

    for tp, lst_cols in dic_dtypes.items():

        if tp=='datetime':
            novo_df[lst_cols] = novo_df[lst_cols].apply(pd.to_datetime)
        else:
            novo_df[lst_cols] = novo_df[lst_cols].astype(tp)

    return novo_df


def preencher_com_ausente(df, nm_col_preenchida, condicao):

    novo_df = df.copy()
    novo_df.loc[condicao, nm_col_preenchida] = np.nan

    return novo_df



def padronizar_str_cols(df, lst_cols_pad = None, dic_cols_pad = None):

    novo_df = df.copy()

    if lst_cols_pad is not None:
        for nm_col in lst_cols_pad:
            novo_df[nm_col] = novo_df[nm_col].apply(padronizar_string)

    if dic_cols_pad is not None:
        for nm_col in dic_cols_pad.items():
            novo_df[nm_col[1]] = novo_df[nm_col[0]].apply(padronizar_string)
        
    return novo_df


def remover_texto_col(df, nm_col, texto):
    """
    Remove o texto especificado de todas as strings na coluna especificada do DataFrame.
    
    Args:
        df (pandas.DataFrame): O DataFrame.
        nm_col (str): O nome da coluna que contém as strings.
        texto (str): O texto a ser removido das strings.
        
    Returns:
        pandas.Series: A coluna contendo as strings sem o texto especificado.
    """
    novo_df = df.copy()
    novo_df[nm_col] = novo_df[nm_col].str.replace(texto, '')
    return novo_df


def formatar_data_para_ano_mes(df, nm_col_data, nm_col_criada = None):
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = nm_col_data

    novo_df[nm_col_criada] = pd.to_datetime(novo_df[nm_col_data]).dt.strftime('%Y%m')
    return novo_df