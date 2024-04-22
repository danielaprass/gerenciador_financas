import numpy as np
import pandas as pd

from pandas.core.frame import DataFrame

from typing import List, Dict


def criar_col_bool(df, nm_col_bool, condicao):

    novo_df = df.copy()
    novo_df[nm_col_bool] = np.where(condicao, True, False)

    return novo_df


def criar_col_chv(df: DataFrame, cols: list) -> DataFrame:
    """
    Cria uma nova coluna 'chv' concatenando os valores das colunas especificadas.

    Parâmetros:
        df (DataFrame): DataFrame onde a coluna será criada.
        cols (list): Lista de nomes das colunas a serem concatenadas.

    Retorno:
        DataFrame: DataFrame com a coluna 'chv' criada.
    """

    novo_df = df.copy()

    novo_df['chv'] = novo_df[cols].apply(lambda x: ' | '.join(x.astype(str)), axis=1)
    return novo_df


def criar_col_dif(df, nm_col1, nm_col2, nm_col_criada = 'dif'):

    novo_df = df.copy()

    novo_df[[nm_col1, nm_col2]] = novo_df[[nm_col1, nm_col2]].astype(float)
    novo_df[nm_col_criada] = novo_df[nm_col1] - novo_df[nm_col2]
    return novo_df


def criar_col_dif_bool(df: DataFrame, nm_col1: str, nm_col2: str, nm_col_criada: str = 'dif') -> DataFrame:
    """
    Cria uma nova coluna em um DataFrame indicando se as colunas especificadas têm valores diferentes.

    Parâmetros:
        df (DataFrame): DataFrame de entrada.
        nm_col1 (str): Nome da primeira coluna.
        nm_col2 (str): Nome da segunda coluna.
        nm_col_criada (str, opcional): Nome da coluna criada para indicar a diferença. Padrão é 'dif'.

    Retorna:
        DataFrame: DataFrame com a coluna adicional indicando a diferença entre as colunas especificadas.
    """
    novo_df = df.copy()
    novo_df[[nm_col1, nm_col2]] = novo_df[[nm_col1, nm_col2]].astype(str)
    novo_df[nm_col_criada] = np.where(novo_df[nm_col1] != novo_df[nm_col2], True, False)
    return novo_df


def criar_col_pct(df: DataFrame, nm_col_num: str, nm_col_criada: str = None, acc: bool = False) -> DataFrame:
    """
    Cria uma nova coluna com a porcentagem dos valores em relação ao total.

    Parâmetros:
        df (DataFrame): DataFrame onde a coluna será criada.
        nm_col_num (str): Nome da coluna contendo os valores numéricos.
        nm_col_criada (str, optional): Nome da coluna criada. Se não especificado, será 'pct_' + nm_col_num.
        acc (bool, optional): Se True, calcula a porcentagem acumulada em relação ao valor máximo; caso contrário, calcula em relação à soma total.

    Retorno:
        DataFrame: DataFrame com a nova coluna criada.
    """
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = 'pct_' + nm_col_num

    total = novo_df[nm_col_num].max() if acc else novo_df[nm_col_num].sum()
    novo_df[nm_col_criada] = round(novo_df[nm_col_num] * 100 / total, 2)

    return novo_df


def criar_col_qtd_digitos(df: DataFrame, nm_col_num: str, nm_col_criada: str = None) -> DataFrame:
    """
    Cria uma nova coluna contendo a quantidade de dígitos em cada valor da coluna especificada.

    Parâmetros:
        df (DataFrame): DataFrame onde a coluna será criada.
        nm_col_num (str): Nome da coluna contendo os valores.

    Retorno:
        DataFrame: DataFrame com a nova coluna criada.
    """
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = 'qtd_digitos'

    novo_df[nm_col_criada] = novo_df[nm_col_num].apply(lambda x: len(str(x)))
    return novo_df


def criar_cols_num_formatadas(df: pd.DataFrame, lst_cols_num: List[str] = None,
                              dic_cols_criadas: Dict[str, str] = None, num_digitos: int = 2) -> pd.DataFrame:
    """
    Formata as colunas numéricas de um DataFrame com um número específico de dígitos decimais.

    Args:
        df (pd.DataFrame): DataFrame a ser formatado.
        lst_cols_num (List[str], optional): Lista das colunas numéricas a serem formatadas. Se não especificado, todas as colunas numéricas serão formatadas. Defaults to None.
        dic_cols_criadas (Dict[str, str], optional): Dicionário que mapeia as colunas originais para as colunas formatadas. Defaults to None.
        num_digitos (int, optional): Número de dígitos decimais a serem mantidos. Defaults to 2.

    Returns:
        pd.DataFrame: DataFrame com as colunas numéricas formatadas.
    """
    novo_df = df.copy()

    if lst_cols_num is None:
        lst_cols_num = novo_df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if dic_cols_criadas is None:
        dic_cols_criadas = {c: c for c in lst_cols_num}

    for col_num in lst_cols_num:
        novo_df[dic_cols_criadas[col_num]] = novo_df[col_num].map(lambda x: f'{x:.{num_digitos}f}')

    return novo_df


def criar_col_soma_acc(df: DataFrame, nm_col_num: str, nm_col_criada: str = None) -> DataFrame:
    """
    Cria uma nova coluna contendo a soma acumulada dos valores da coluna especificada.

    Parâmetros:
        df (DataFrame): DataFrame onde a coluna será criada.
        nm_col_num (str): Nome da coluna contendo os valores numéricos.
        nm_col_criada (str, optional): Nome da coluna criada. Se não especificado, será 'sum_' + nm_col_num + '_acc'.

    Retorno:
        DataFrame: DataFrame com a nova coluna criada.
    """
    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = 'sum_' + nm_col_num + '_acc'

    novo_df[nm_col_criada] = novo_df[nm_col_num].cumsum()

    return novo_df


def criar_col_verdadeira(df: DataFrame, nm_col_criada: str) -> DataFrame:
    """
    Cria uma nova coluna contendo valores booleanos True em todas as linhas.

    Parâmetros:
        df (DataFrame): DataFrame onde a coluna será criada.
        nm_col_criada (str): Nome da coluna criada.

    Retorno:
        DataFrame: DataFrame com a nova coluna criada.
    """
    novo_df = df.copy()

    novo_df[nm_col_criada] = True
    return novo_df


def criar_col_soma_cols(df, lst_cols_somadas, nm_col_criada = None):
    """
    Adiciona uma nova coluna ao DataFrame que é a soma das colunas especificadas.

    Args:
        df (pandas.DataFrame): O DataFrame.
        lst_cols_somadas (list): Lista de nomes das colunas a serem somadas.
        nm_col_criada (str): Nome da coluna a ser criada para armazenar a soma.

    Returns:
        pandas.DataFrame: O DataFrame com a coluna adicionada contendo a soma das colunas especificadas.
    """

    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = 'sum'

    novo_df[nm_col_criada] = novo_df[lst_cols_somadas].sum(axis=1)
    return novo_df


def criar_col_media_cols(df, lst_cols_media, nm_col_criada = None):
    """
    Adiciona uma nova coluna ao DataFrame que é a média das colunas especificadas.

    Args:
        df (pandas.DataFrame): O DataFrame.
        lst_cols_media (list): Lista de nomes das colunas a serem utilizados para calcular a média.
        nm_col_criada (str): Nome da coluna a ser criada para armazenar a média.

    Returns:
        pandas.DataFrame: O DataFrame com a coluna adicionada contendo a média das colunas especificadas.
    """

    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = 'media'

    novo_df[nm_col_criada] = novo_df[lst_cols_media].mean(axis=1)
    return novo_df


def criar_col_moda_cols(df, lst_cols_moda, nm_col_criada = None):
    """
    Adiciona uma nova coluna ao DataFrame que é a média das colunas especificadas.

    Args:
        df (pandas.DataFrame): O DataFrame.
        lst_cols_moda (list): Lista de nomes das colunas a serem utilizados para calcular a média.
        nm_col_criada (str): Nome da coluna a ser criada para armazenar a média.

    Returns:
        pandas.DataFrame: O DataFrame com a coluna adicionada contendo a média das colunas especificadas.
    """

    novo_df = df.copy()

    if nm_col_criada is None:
        nm_col_criada = 'moda'

    novo_df[nm_col_criada] = novo_df[lst_cols_moda].mode(axis=1).loc[:,0]
    return novo_df
