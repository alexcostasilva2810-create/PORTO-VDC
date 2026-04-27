import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Log de Operações - Porto VDC", layout="wide")

st.title("🚢 Registro de Operações (SOF) - Porto VDC")
st.subheader("Controle Diário por Turnos")

# --- Dados Fixos do Navio (Baseado na sua imagem) ---
with st.sidebar:
    st.header("Informações do Navio")
    navio = st.text_input("Navio", "M/V HB TUCUNARÉ")
    viagem = st.text_input("Viagem", "023/16")
    porto = st.text_input("Porto/Berço", "VILA DO CONDE - PIER 101")
    carga = st.text_input("Carga", "WET BAUXITE IN BULK")

# --- Lógica de Turnos ---
def obter_turno():
    hora_atual = datetime.now().hour
    if 0 <= hora_atual < 8: return "1º Turno (00:00 - 08:00)"
    if 8 <= hora_atual < 16: return "2º Turno (08:00 - 16:00)"
    return "3º Turno (16:00 - 00:00)"

# --- Interface de Preenchimento ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    data_ev = st.date_input("Data do Evento")
with col2:
    hora_ev = st.time_input("Hora do Evento")
with col3:
    turno_atual = st.info(f"Turno Atual: {obter_turno()}")

evento_selecionado = st.selectbox("Selecione o Evento", [
    "VESSEL ARRIVED AT MOSQUEIRO P/S", "DROPPED ANCHOR", "NOR TENDERED", 
    "NOR ACCEPTED", "ANCHOR UP", "PILOT ON BOARD FOR BERTHING", 
    "FIRST LINE ASHORE", "ALL FAST ALONGSIDE", "COMMENCED DISCHARGE OPERATION",
    "COMPLETED DISCHARGE OPERATION", "VESSEL UNMOORED"
])

comentario = st.text_area("Observações / Comentários")

if st.button("Registrar Evento"):
    st.success(f"Evento '{evento_selecionado}' registrado com sucesso!")
    # Aqui os dados seriam salvos em um banco de dados ou CSV

# --- Tabela de Visualização (Exemplo) ---
st.markdown("---")
st.write("### Log de Eventos Registrados")
# Criando uma tabela exemplo para mostrar como fica
dados_exemplo = pd.DataFrame({
    'Data': [data_ev],
    'Hora': [hora_ev.strftime('%H:%M')],
    'Turno': [obter_turno()],
    'Evento': [evento_selecionado],
    'Comentário': [comentario]
})
st.table(dados_exemplo)
