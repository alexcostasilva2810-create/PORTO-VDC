import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Log de Operações - Porto VDC", layout="wide")

# --- FUNÇÃO PARA SALVAR OS DADOS ---
def salvar_dados(nova_linha):
    arquivo = "dados_porto.csv"
    # Se o arquivo já existir, lê e adiciona a linha. Se não, cria um novo.
    if os.path.exists(arquivo):
        df_existente = pd.read_csv(arquivo)
        df_final = pd.concat([df_existente, nova_linha], ignore_index=True)
    else:
        df_final = nova_linha
    df_final.to_csv(arquivo, index=False)
    return df_final

st.title("🚢 Registro de Operações (SOF) - Porto VDC")

# --- SIDEBAR: INFORMAÇÕES DO NAVIO ---
with st.sidebar:
    st.header("Informações do Navio")
    navio = st.text_input("Navio", "M/V HB TUCUNARÉ")
    viagem = st.text_input("Viagem", "023/16")
    porto_berco = st.text_input("Porto/Berço", "VILA DO CONDE - PIER 101")
    carga = st.text_input("Carga", "WET BAUXITE IN BULK")

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        data_ev = st.date_input("Data do Evento")
    with col2:
        hora_ev = st.time_input("Hora do Evento")
    with col3:
        # Lógica de Turno
        h = hora_ev.hour
        turno = "1º Turno (00-08h)" if 0<=h<8 else "2º Turno (08-16h)" if 8<=h<16 else "3º Turno (16-00h)"
        st.info(f"Turno Detectado: {turno}")

    evento = st.selectbox("Selecione o Evento", [
        "VESSEL ARRIVED AT MOSQUEIRO P/S", "DROPPED ANCHOR", "NOR TENDERED", 
        "NOR ACCEPTED", "ANCHOR UP", "PILOT ON BOARD FOR BERTHING", 
        "FIRST LINE ASHORE", "ALL FAST ALONGSIDE", "COMMENCED DISCHARGE OPERATION",
        "COMPLETED DISCHARGE OPERATION", "VESSEL UNMOORED"
    ])
    
    comentario = st.text_area("Observações / Comentários")

    # BOTÃO DE LANÇAMENTO
    if st.button("Registrar Evento"):
        nova_entrada = pd.DataFrame([{
            "Data": data_ev.strftime('%Y-%m-%d'),
            "Hora": hora_ev.strftime('%H:%M'),
            "Turno": turno,
            "Evento": evento,
            "Comentario": comentario,
            "Navio": navio
        }])
        df_atualizado = salvar_dados(nova_entrada)
        st.success("✅ Dados lançados e salvos com sucesso!")

# --- EXIBIÇÃO DA TABELA PERMANENTE ---
st.markdown("---")
st.subheader("📋 Log de Eventos Gravados")

if os.path.exists("dados_porto.csv"):
    df_visualizacao = pd.read_csv("dados_porto.csv")
    st.dataframe(df_visualizacao, use_container_width=True)
    
    # Botão para baixar a tabela em Excel/CSV
    csv = df_visualizacao.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Tabela Completa (CSV)",
        data=csv,
        file_name='log_porto_vdc.csv',
        mime='text/csv',
    )
else:
    st.info("Nenhum dado gravado ainda.")
