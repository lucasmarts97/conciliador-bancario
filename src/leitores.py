"""
Módulo de leitura e extração de dados dos arquivos de origem:
- Extrato bancário no formato OFX
- Razão contábil em PDF
"""
import io
import re

import pandas as pd
from ofxparse import OfxParser

_PADRAO_VALOR = re.compile(r'[\d]+\.[\d]{3},\d{2}|[\d]+,\d{2}')


def ler_ofx_banco(arquivo) -> pd.DataFrame:
    """Lê um arquivo OFX de extrato bancário e retorna um DataFrame padronizado.

    Args:
        arquivo: objeto de arquivo (ex.: retornado por st.file_uploader) contendo
                 um extrato bancário no formato OFX.

    Returns:
        DataFrame com as colunas DATA_BANCO, HISTORICO_BANCO, VALOR, TIPO e ENCONTRADO.
    """
    conteudo_str = arquivo.getvalue().decode('cp1252', errors='ignore')
    conteudo_bytes = conteudo_str.encode('utf-8')

    ofx = OfxParser.parse(io.BytesIO(conteudo_bytes))
    dados = []

    for mov in ofx.account.statement.transactions:
        valor = round(abs(float(mov.amount)), 2)
        dados.append({
            'DATA_BANCO': mov.date.strftime('%d/%m/%Y'),
            'HISTORICO_BANCO': mov.memo,
            'VALOR': valor,
            'TIPO': 'Entrada' if float(mov.amount) > 0 else 'Saída',
            'ENCONTRADO': False,
        })
    return pd.DataFrame(dados)


def ler_pdf_razao(arquivo) -> pd.DataFrame:
    """Lê um PDF de razão contábil e extrai data, histórico e valor de cada lançamento.

    Args:
        arquivo: objeto de arquivo (ex.: retornado por st.file_uploader) contendo
                 o razão contábil exportado em PDF.

    Returns:
        DataFrame com as colunas DATA_RAZAO, HISTORICO_RAZAO e VALOR.
    """
    import pdfplumber  # import local para manter o custo de import baixo no restante do app

    dados = []

    with pdfplumber.open(arquivo) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if not texto:
                continue

            for linha in texto.split('\n'):
                linha_limpa = linha.replace('|', ' ').strip()

                if not re.match(r'^\d{2}/\d{2}/\d{4}', linha_limpa):
                    continue

                partes = linha_limpa.split()
                data_str = partes[0]
                valores_encontrados = _PADRAO_VALOR.findall(linha_limpa)

                if len(valores_encontrados) >= 2:
                    valor_movimento_str = valores_encontrados[-2]
                    valor_float = float(valor_movimento_str.replace('.', '').replace(',', '.'))
                    historico = " ".join(partes[1:-len(valores_encontrados)])

                    dados.append({
                        'DATA_RAZAO': data_str,
                        'HISTORICO_RAZAO': historico,
                        'VALOR': round(valor_float, 2),
                    })
    return pd.DataFrame(dados)
