import pandas as pd

from modulos.utils_pandas.utils_criacao_colunas import (
    criar_col_pct,
    criar_col_qtd_digitos,
    criar_col_soma_acc)


from typing import List, Optional
from pandas.core.frame import DataFrame


def agrupar_chv_lista(df, lst_col_chv):
    
    novo_df = df.copy()
    
    novo_df = (
        novo_df
        .groupby(lst_col_chv)
        .agg(lambda x: list(x.unique()))
    )

    return novo_df


def soma_agg(df: DataFrame, lst_cols_id: list, lst_cols_somadas: list) -> DataFrame:
    """
    Soma as colunas especificadas do DataFrame agrupando por colunas de identificação.

    Parâmetros:
        df (DataFrame): DataFrame original.
        lst_cols_id (list): Lista das colunas de identificação.
        lst_cols_somadas (list): Lista das colunas a serem somadas.

    Retorno:
        DataFrame: DataFrame resultante da agregação.
    """
    novo_df = df.copy()
    
    return (
        novo_df
        .groupby(lst_cols_id)
        .agg({c: 'sum' for c in lst_cols_somadas})
        .reset_index()
        .sort_values(lst_cols_somadas, ascending=False))


def tb_ausentes(df: DataFrame, cols: list = None) -> DataFrame:
    """
    Retorna uma tabela com a quantidade e percentual de valores ausentes por coluna.

    Parâmetros:
        df (DataFrame): DataFrame original.
        cols (list, optional): Lista das colunas a serem consideradas. Se não especificado, usa todas as colunas.

    Retorno:
        DataFrame: Tabela de valores ausentes por coluna.
    """
    novo_df = df.copy()

    if cols is None:
        cols = novo_df.columns

    qtd_ausentes = novo_df[cols].isnull().sum()
    pct_ausentes = (novo_df[cols].isnull().sum() * 100) / len(novo_df)

    tb_ausentes = pd.concat([qtd_ausentes, pct_ausentes], axis=1)
    tb_ausentes = tb_ausentes.rename(columns={0: 'qtd_ausentes', 1: 'pct_ausentes'})
    tb_ausentes = tb_ausentes.sort_values('pct_ausentes', ascending=False).round(2)

    qtd_cols_ausentes = tb_ausentes[tb_ausentes['qtd_ausentes'] > 0].shape[0]
    print(f'Há {qtd_cols_ausentes} colunas com valores ausentes.')

    return (
        tb_ausentes
        .reset_index()
        .rename(columns={'index': 'col'}))


def tb_ausentes_distintos(df: DataFrame, cols: list = None) -> DataFrame:
    """
    Retorna uma tabela com valores ausentes e distintos por coluna.

    Parâmetros:
        df (DataFrame): DataFrame original.
        cols (list, optional): Lista das colunas a serem consideradas. Se não especificado, usa todas as colunas.

    Retorno:
        DataFrame: Tabela de valores ausentes e distintos por coluna.
    """

    novo_df = df.copy()

    if cols is None:
        cols = novo_df.columns

    return (
        novo_df
        .pipe(tb_ausentes, cols)
        .merge(
            novo_df
            .pipe(tb_distintos, cols),
            on='col',
            how='inner'))


def tb_distintos(df: DataFrame, cols: list = None) -> DataFrame:
    """
    Retorna uma tabela com a quantidade e percentual de valores distintos por coluna.

    Parâmetros:
        df (DataFrame): DataFrame original.
        cols (list, optional): Lista das colunas a serem consideradas. Se não especificado, usa todas as colunas.

    Retorno:
        DataFrame: Tabela de valores distintos por coluna.
    """

    novo_df = df.copy()

    if cols is None:
        cols = novo_df.columns

    qtd_distintos = novo_df[cols].nunique()
    pct_distintos = round(novo_df[cols].nunique() / novo_df.shape[0] * 100, 2)

    return pd.DataFrame({
        'col': qtd_distintos.index,
        'qtd_distintos': qtd_distintos.values,
        'pct_distintos': pct_distintos.values
    }).sort_values('pct_distintos', ascending=False)


def tb_distrib(df: DataFrame, cols_num: list = None, qtd_zerados: bool = False) -> DataFrame:
    """
    Retorna um DataFrame com estatísticas descritivas das colunas numéricas.

    Parâmetros:
        df (DataFrame): DataFrame a ser analisado.
        cols_num (list, optional): Lista das colunas numéricas a serem consideradas. Se não especificado, todas as colunas numéricas serão consideradas. Defaults to None.
        qtd_zerados (bool, optional): Indica se as estatísticas de valores zerados devem ser incluídas. Defaults to False.

    Retorno:
        DataFrame: DataFrame contendo as estatísticas descritivas.
    """
    novo_df = df.copy()

    if cols_num is None:
        cols_num = novo_df.select_dtypes(include='number').columns
    
    novo_df = (
        novo_df[cols_num]
        .describe()
        .reset_index())

    if qtd_zerados:
        return pd.concat([novo_df, tb_zerados(novo_df, cols_num)])
    else:
        return novo_df


def tb_distrib_data(df: DataFrame, col_dat: str) -> DataFrame:
    """
    Retorna um DataFrame com os percentis de uma coluna de data.

    Parâmetros:
        df (DataFrame): DataFrame a ser analisado.
        col_dat (str): Nome da coluna de data.

    Retorno:
        DataFrame: DataFrame contendo os percentis da coluna de data.
    """
    novo_df = df.copy()

    novo_df[col_dat] = pd.to_datetime(novo_df[col_dat]).dt.date
    quartis = novo_df[col_dat].quantile([0, 0.25, 0.5, 0.75, 1])

    return pd.DataFrame({'percentil': quartis.index, col_dat: quartis.values})


def tb_freq(df: DataFrame, cols: list, freq_acc: bool = False) -> DataFrame:
    """
    Retorna um DataFrame com as frequências absolutas e relativas das colunas especificadas.

    Parâmetros:
        df (DataFrame): DataFrame a ser analisado.
        cols (list): Lista das colunas para calcular as frequências.
        freq_acc (bool, optional): Indica se as frequências acumuladas devem ser incluídas. Defaults to False.

    Retorno:
        DataFrame: DataFrame contendo as frequências absolutas e relativas.
    """
    novo_df = df.copy()

    novo_df = (
        novo_df[cols]
        .value_counts()
        .reset_index()
        .rename(columns={0:'freq_abs','count':'freq_abs'})
        .pipe(criar_col_pct, 'freq_abs', 'freq_rel'))

    if freq_acc:
        return (
            novo_df 
            .pipe(criar_col_soma_acc, 'freq_abs', 'freq_acc')
            .pipe(criar_col_pct, 'freq_acc', 'freq_acc_rel', acc=True))
    else:
        return novo_df


def tb_freq_data(df, col_dat: str, col_chv: str, periodo: str = 'a'):
    """
    Calcula a frequência dos dados.

    Parâmetros:
        df (DataFrame): DataFrame de entrada.
        col_dat (str): Nome da coluna contendo datas.
        col_chv (str): Nome da coluna chave para contar a frequência.
        periodo (str, optional): Período de frequência. Defaults to 'a' (ano).

    Retorno:
        DataFrame: DataFrame com a frequência calculada.
    """

    novo_df = df.copy()

    nm_col_criada = {
        'a':'ano',
        'm':'mes'
    }[periodo]

    func_formatacao = {
        'a': pd.to_datetime(novo_df[col_dat]).dt.year,
        'm': pd.to_datetime(novo_df[col_dat]).dt.to_period('M')
    }[periodo]

    novo_df[nm_col_criada] = func_formatacao

    return (
        novo_df
        .groupby(nm_col_criada)[col_chv]
        .count()
        .reset_index()
        .rename(columns={col_chv: 'qtd_registros'})
        .pipe(criar_col_pct, 'qtd_registros', 'pct_registros'))


def tb_freq_digitos(df: DataFrame, col: str) -> DataFrame:
    """
    Calcula a frequência dos dígitos.

    Parâmetros:
        df (DataFrame): DataFrame de entrada.
        col (str): Nome da coluna contendo os valores a serem analisados.

    Retorno:
        DataFrame: DataFrame com a frequência dos dígitos calculada.
    """
    novo_df = df.copy()
    
    return (
        novo_df
        .pipe(criar_col_qtd_digitos, col)
        .pipe(tb_freq, ['qtd_digitos']))

def tb_soma_agg(df: DataFrame, lst_cols_id: List[str], nm_col_somada: str) -> DataFrame:
    """
    Calcula a soma agregada de colunas.

    Parâmetros:
        df (DataFrame): DataFrame de entrada.
        lst_cols_id (List[str]): Lista de nomes de colunas a serem agrupadas.
        nm_col_somada (str): Nome da coluna a ser somada.

    Retorno:
        DataFrame: DataFrame com a soma agregada calculada.
    """
    novo_df = df.copy()

    return (
        novo_df
        .pipe(soma_agg, lst_cols_id, [nm_col_somada])
        .pipe(criar_col_pct, nm_col_somada)
        .pipe(criar_col_soma_acc, nm_col_somada)
        .pipe(criar_col_pct, f'sum_{nm_col_somada}_acc', acc=True))

def tb_visao_geral(df: DataFrame, cols: Optional[List[str]] = None) -> DataFrame:
    """
    Cria uma visão geral do DataFrame.

    Parâmetros:
        df (DataFrame): DataFrame de entrada.
        cols (List[str], optional): Lista de colunas a serem incluídas na visão geral. Defaults to None.

    Retorno:
        DataFrame: DataFrame com a visão geral criada.
    """
    novo_df = df.copy()

    if cols is None:
        cols = df.columns

    return (
        novo_df
        .pipe(tb_ausentes, cols)

        .merge(
            novo_df
            .pipe(tb_distintos, cols),

            on='col',
            how='inner')

        .merge(
            novo_df.dtypes
            .reset_index()
            .rename(columns={'index': 'col', 0: 'tipo_col'}),

            on='col',
            how='inner'))

def tb_zerados(df: DataFrame, cols_num: Optional[List[str]] = None) -> DataFrame:
    """
    Conta as ocorrências de valores zero.

    Parâmetros:
        df (DataFrame): DataFrame de entrada.
        cols_num (List[str], optional): Lista de colunas numéricas a serem consideradas. Defaults to None.

    Retorno:
        DataFrame: DataFrame contendo as colunas e a quantidade de zeros encontrados.
    """
    novo_df = df.copy()

    if cols_num is None:
        cols_num = novo_df.select_dtypes(include='number').columns

    novo_df = (
        (df[cols_num] < 1e-6)
        .sum()
        .reset_index()
        .rename(columns={'index': 'col', 0: 'qtd_zerados'})
        .transpose())

    novo_df.columns = novo_df.iloc[0]
    return novo_df.iloc[1:]


def transformar_linhas_em_colunas(df, nm_col_chv, lst_cols_id, lst_cols_vlr):

    novo_df = df.copy()

    novo_df = (
        novo_df
        .pivot_table(
            index=nm_col_chv,
            columns=lst_cols_id,
            values=lst_cols_vlr,
            aggfunc='sum')
    )


    novo_df.columns = [c for c in novo_df.columns]
    novo_df = novo_df.reset_index()

    return novo_df


def conta_distintos_cols_nao_chave(df, lst_cols_chv):

    lst_cols = [c for c in df.columns if c not in lst_cols_chv]
    dic_col_func = {c:'nunique' for c in df.columns if c not in lst_cols_chv}
    
    return (df
    
        .groupby(lst_cols_chv)
        .agg(dic_col_func)
        .reset_index())