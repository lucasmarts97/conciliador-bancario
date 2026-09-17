"""
Motor de conciliação: cruza os lançamentos do razão contábil com o extrato
bancário e classifica as pendências, incluindo lançamentos futuros no banco.
"""
import pandas as pd


def conciliar(df_razao: pd.DataFrame, df_ofx: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cruza os lançamentos do razão com o extrato bancário pelo valor.

    Args:
        df_razao: DataFrame retornado por ler_pdf_razao (colunas DATA_RAZAO,
                   HISTORICO_RAZAO, VALOR).
        df_ofx: DataFrame retornado por ler_ofx_banco (colunas DATA_BANCO,
                 HISTORICO_BANCO, VALOR, TIPO, ENCONTRADO).

    Returns:
        Tupla (df_pendencias_razao, df_sobras_ofx):
            df_pendencias_razao: lançamentos do razão não encontrados no banco.
            df_sobras_ofx: lançamentos do banco não encontrados no razão, com
                            uma coluna OBSERVAÇÃO indicando se é uma pendência
                            real ("Falta lançar no Razão") ou um lançamento
                            futuro ("Lançamento Futuro 🗓️") em relação à
                            última data presente no razão.
    """
    df_ofx = df_ofx.copy()
    pendencias_razao = []

    for _, row in df_razao.iterrows():
        valor_busca = row['VALOR']
        match = df_ofx[(df_ofx['VALOR'] == valor_busca) & (~df_ofx['ENCONTRADO'])]

        if not match.empty:
            idx_match = match.index[0]
            df_ofx.at[idx_match, 'ENCONTRADO'] = True
        else:
            pendencias_razao.append(row)

    df_pendencias_razao = pd.DataFrame(pendencias_razao)
    df_sobras_ofx = df_ofx[~df_ofx['ENCONTRADO']].copy()

    if not df_sobras_ofx.empty and not df_razao.empty:
        df_razao = df_razao.copy()
        df_razao['DATA_TEMP'] = pd.to_datetime(df_razao['DATA_RAZAO'], format='%d/%m/%Y')
        data_maxima_razao = df_razao['DATA_TEMP'].max()

        df_sobras_ofx['DATA_TEMP'] = pd.to_datetime(df_sobras_ofx['DATA_BANCO'], format='%d/%m/%Y')

        df_sobras_ofx['OBSERVAÇÃO'] = 'Falta lançar no Razão'
        df_sobras_ofx.loc[df_sobras_ofx['DATA_TEMP'] > data_maxima_razao, 'OBSERVAÇÃO'] = 'Lançamento Futuro 🗓️'

        df_sobras_ofx = df_sobras_ofx.drop(columns=['ENCONTRADO', 'DATA_TEMP'])

    return df_pendencias_razao, df_sobras_ofx
