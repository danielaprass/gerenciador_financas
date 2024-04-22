import math
import pandas as pd

from modulos.utils_pandas.utils_criacao_colunas import criar_col_chv

from IPython.display import display

from pandas.core.frame import DataFrame


def mostrar_intervalo(df: DataFrame, col: str) -> None:
    """
    Mostra o intervalo de valores em uma coluna do DataFrame.

    Parâmetros:
        df (DataFrame): O DataFrame.
        col (str): O nome da coluna.

    Retorno:
        None
    """
    print(f'A coluna {col} vai de {df[col].min()} até {df[col].max()}')


def mostrar_n_cols_por_linha(df: pd.DataFrame, n_cols: int = 10, n_linhas_df: int = 5):
    """
    Exibe as primeiras n_linhas_df linhas e agrupa as colunas em grupos de n_cols.
    
    Parâmetros:
        df (pd.DataFrame): O DataFrame a ser exibido.
        n_cols (int): O número de colunas por grupo.
        n_linhas_df (int): O número de linhas a serem exibidas.
    """
    for i in range(0, math.ceil(len(df.columns) / n_cols)):
        display(df.iloc[0:n_linhas_df, (i * n_cols): (i * n_cols) + n_cols])


def mostrar_top_valores(df: DataFrame, col_num: str, cols_dsc: list = None) -> DataFrame:
    """
    Retorna os top valores do DataFrame ordenados por uma coluna numérica e outras colunas descritivas.

    Parâmetros:
        df (DataFrame): O DataFrame.
        col_num (str): O nome da coluna numérica.
        cols_dsc (list): Lista com os nomes das colunas descritivas.

    Retorno:
        DataFrame: DataFrame ordenado pelos top valores.
    """

    if cols_dsc is None:
        cols_dsc = [c for c in cols_dsc if c != col_num]

    return df[[*cols_dsc, col_num]].sort_values(col_num, ascending=False)

def mostrar_visao_geral(df: DataFrame) -> None:
    """
    Mostra uma visão geral do DataFrame, incluindo seu tamanho e os primeiros registros.

    Parâmetros:
        df (DataFrame): O DataFrame.

    Retorno:
        None
    """

    print(f'Tamanho da base: {df.shape}')
    print(f'\nVisualização dos primeiros registros:')
    display(df.head(5))

def obter_duplicatas(df: DataFrame, cols: list) -> DataFrame:
    """
    Retorna as duplicatas no DataFrame, baseado nas colunas fornecidas.

    Parâmetros:
        df (DataFrame): O DataFrame.
        cols (list): Lista com os nomes das colunas.

    Retorno:
        DataFrame: DataFrame contendo as duplicatas.
    """
    novo_df = df.copy()

    novo_df = criar_col_chv(novo_df, cols)
    novo_df[f'qtd_distintos_chv'] = novo_df.groupby('chv')[cols[0]].transform('count')

    return (
        novo_df[novo_df[f'qtd_distintos_chv'] > 1]
        .sort_values(
            [f'qtd_distintos_chv', *[c for c in cols]], 
            ascending=[False, *[True for c in cols]]))

def testa_granularidade(df: DataFrame, cols: list) -> None:
    """
    Testa a granularidade do DataFrame baseado nas colunas fornecidas.

    Parâmetros:
        df (DataFrame): O DataFrame.
        cols (list): Lista com os nomes das colunas.

    Retorno:
        None
    """
    novo_df = df.copy()

    novo_df = criar_col_chv(novo_df, cols)
    
    tam = novo_df.shape[0]
    qtd_combinacoes = novo_df.chv.nunique()

    print('Qtd de linhas da base:')
    print(tam)
    print('Qtd de combinacoes distintas:')
    print(qtd_combinacoes)

    if tam == qtd_combinacoes:
        print(f'\n{cols} é granular')
    else:
        print(f'{cols} não é granular')
        print('\nHá {} duplicatas ({}% da base)'.format(
            tam - qtd_combinacoes,
            round((tam - qtd_combinacoes)*100/tam,2)
        ))
