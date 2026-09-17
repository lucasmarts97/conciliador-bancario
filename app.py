import streamlit as st

from src.leitores import ler_ofx_banco, ler_pdf_razao
from src.motor_conciliacao import conciliar

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Conciliador Bancário", layout="wide")

# --- MENU LATERAL (SELEÇÃO DE BANCO) ---
with st.sidebar:
    st.header("⚙️ Parâmetros")
    banco_selecionado = st.radio(
        "Selecione o Banco para Conciliar:",
        ["Sicredi", "Bradesco", "Caixa Econômica"],
    )
    st.markdown("---")
    st.caption("🤖 Conciliador Bancário — projeto de portfólio")

# --- INTERFACE PRINCIPAL ---
st.title(f"📊 Conciliador Bancário: {banco_selecionado}")
st.markdown("Valide instantaneamente os lançamentos contábeis contra o extrato bancário.")

col1, col2 = st.columns(2)
with col1:
    arq_razao = st.file_uploader(f"📄 Anexe o RAZÃO ({banco_selecionado}) - PDF", type=['pdf'])
with col2:
    arq_ofx = st.file_uploader(f"🏦 Anexe o Extrato {banco_selecionado} - OFX", type=['ofx'])

if arq_razao and arq_ofx:
    if st.button(f"🚀 Processar Conciliação - {banco_selecionado}", use_container_width=True, type="primary"):
        with st.spinner("Lendo arquivos e cruzando valores..."):

            df_razao = ler_pdf_razao(arq_razao)
            df_ofx = ler_ofx_banco(arq_ofx)

            if df_razao.empty:
                st.error("Não foi possível extrair movimentações do PDF. Verifique se o layout do arquivo é válido.")
                st.stop()

            df_pendencias_razao, df_sobras_ofx = conciliar(df_razao, df_ofx)

            st.success(f"✅ Cruzamento do {banco_selecionado} finalizado!")
            st.markdown("---")

            c1, c2, c3 = st.columns(3)
            c1.metric(label="Total de Títulos no Razão", value=len(df_razao))
            c2.metric(
                label="Faltam no Banco (Pendências)",
                value=len(df_pendencias_razao) if not df_pendencias_razao.empty else 0,
            )
            c3.metric(
                label="Sobraram no Banco",
                value=len(df_sobras_ofx) if not df_sobras_ofx.empty else 0,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(f"⚠️ Títulos no RAZÃO não encontrados no {banco_selecionado}")
            if not df_pendencias_razao.empty:
                st.dataframe(df_pendencias_razao, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhuma pendência! Todos os lançamentos do Razão estão no banco.")

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader(f"⚠️ Títulos no {banco_selecionado} que não estão no RAZÃO")
            if not df_sobras_ofx.empty:
                st.dataframe(df_sobras_ofx, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum lançamento sobrou no extrato bancário.")
