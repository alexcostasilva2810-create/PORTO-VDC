import pandas as pd
from datetime import datetime

class SOFManager:
    def __init__(self):
        # Definição dos eventos padrão conforme sua imagem
        self.lista_eventos = [
            "VESSEL SAILED FROM TROMBETAS", "VESSEL ARRIVAL AT FAZENDINHA",
            "VESSEL SAILED FROM FAZENDINHA", "VESSEL ARRIVED AT MOSQUEIRO P/S",
            "DROPPED ANCHOR", "NOR TENDERED", "NOR ACCEPTED", "ANCHOR UP",
            "PILOT ON BOARD FOR BERTHING", "ARRIVAL AT VDC ROADS",
            "FIRST LINE ASHORE", "ALL FAST ALONGSIDE", "GANGWAY ASHORE",
            "CARGO AGENT ON BOARD", "INITIAL DRAFT SURVEY", "CLEARED TO DISCHARGE",
            "COMMENCED DISCHARGE OPERATION", "COMPLETED DISCHARGE OPERATION",
            "FINAL DRAFT SURVEY PERFORMED", "PILOT ON BOARD FOR SAILING",
            "UNBERTHING MANEUVER STARTED", "VESSEL UNMOORED"
        ]
        self.dados_log = []

    def identificar_turno(self, hora_str):
        """Identifica o turno com base na hora (HH:MM)"""
        hora = int(hora_str.split(':')[0])
        if 0 <= hora < 8:
            return "1º Turno (00-08h)"
        elif 8 <= hora < 16:
            return "2º Turno (08-16h)"
        else:
            return "3º Turno (16-00h)"

    def registrar_evento(self, evento_idx, data, hora, comentario=""):
        """Adiciona um novo registro ao log"""
        evento_nome = self.lista_eventos[evento_idx]
        turno = self.identificar_turno(hora)
        
        registro = {
            "Data": data,
            "Hora": hora,
            "Turno": turno,
            "Evento": evento_nome,
            "Comentário": comentario
        }
        self.dados_log.append(registro)
        print(f"✅ Evento '{evento_nome}' registrado no {turno}.")

    def gerar_relatorio(self):
        """Transforma os registros em um DataFrame organizado"""
        df = pd.DataFrame(self.dados_log)
        if not df.empty:
            # Ordena por data e hora cronologicamente
            df['Aux_Time'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'])
            df = df.sort_values(by='Aux_Time').drop(columns=['Aux_Time'])
        return df

# --- SIMULAÇÃO DE USO ---

sof = SOFManager()

print("--- SISTEMA DE REGISTRO DE TURNOS ---")
# Exemplo: Usuário escolhe o evento 10 (FIRST LINE ASHORE)
# No mundo real, você teria um input() para capturar esses dados
sof.registrar_evento(10, "2023-12-31", "17:15", "Condições climáticas boas")
sof.registrar_evento(11, "2023-12-31", "17:40", "Atracação concluída")
sof.registrar_evento(4, "2023-12-31", "07:00", "Aguardando prático")

# Gerando a tabela final
relatorio_final = sof.gerar_relatorio()
print("\nRelatório Consolidado por Turno:")
print(relatorio_final)

# Exportar para Excel (opcional)
# relatorio_final.to_excel("SOF_Turnos.xlsx", index=False)
