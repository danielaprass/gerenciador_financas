from unidecode import unidecode
import re

from typing import Union


def formatar_num(num: Union[int, float], num_digitos: int) -> str:
    """
    Formata um número com a quantidade específica de dígitos decimais.

    Parâmetros:
        num (Union[int, float]): O número a ser formatado.
        num_digitos (int): O número de dígitos decimais desejados.

    Retorno:
        str: O número formatado como string.
    """
    return '{:.{}f}'.format(num, num_digitos)


def padronizar_string(s: str) -> str:
    """
    Padroniza uma string removendo caracteres especiais,
    convertendo para maiúsculas e removendo espaços extras.

    Parâmetros:
        s (str): A string a ser padronizada.

    Retorno:
        str: A string padronizada.
    """

    # Remove acentuação
    s = unidecode(s)  
    # Converte para maiúsculas
    s = s.lower()
    # Substitui traço por espaço
    s = s.replace('-', ' ')
    # Substitui ponto por vazio
    s = s.replace('.', '')
    # Remove espaços extras e une palavras com underline
    s = '_'.join(s.split())
    # Remove espaços em branco do início e do fim
    s = s.strip()
    # # Remove caracteres especiais exceto espaço, nova linha e ponto
    # s = re.sub('[^a-zA-Z0-9 \n\.]', '', s)
    return s
