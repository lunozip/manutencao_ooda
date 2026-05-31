import json

ordens = [
    {"id": "OS-001", "ativo": "Bomba-01", "sintoma": "Vibração excessiva no mancal dianteiro, ruído metálico intermitente", "data": "2025-08-10", "ttr_horas": 4, "criticidade": "Alta"},
    {"id": "OS-002", "ativo": "Bomba-01", "sintoma": "Vazamento de selo mecânico, presença de líquido no piso abaixo da bomba", "data": "2025-09-03", "ttr_horas": 6, "criticidade": "Alta"},
    {"id": "OS-003", "ativo": "Compressor-02", "sintoma": "Alta temperatura na descarga, pressão abaixo do setpoint de 8 bar", "data": "2025-09-15", "ttr_horas": 8, "criticidade": "Crítica"},
    {"id": "OS-004", "ativo": "Bomba-02", "sintoma": "Queda de vazão, cavitação suspeita, ruído de estalidos na sucção", "data": "2025-09-20", "ttr_horas": 3, "criticidade": "Média"},
    {"id": "OS-005", "ativo": "Bomba-01", "sintoma": "Vibração elevada após reparo anterior, desalinhamento suspeito, temperatura no rolamento acima do normal", "data": "2025-10-01", "ttr_horas": 2, "criticidade": "Alta"},
    {"id": "OS-006", "ativo": "Motor-03", "sintoma": "Superaquecimento do enrolamento, trip por sobretemperatura, proteção térmica atuou", "data": "2025-10-08", "ttr_horas": 12, "criticidade": "Crítica"},
    {"id": "OS-007", "ativo": "Compressor-02", "sintoma": "Ruído de batença nas válvulas de sucção, perda de eficiência volumétrica", "data": "2025-10-22", "ttr_horas": 10, "criticidade": "Alta"},
    {"id": "OS-008", "ativo": "Bomba-01", "sintoma": "Desgaste acelerado do rolamento 6205, reincidência em menos de 90 dias após substituição", "data": "2025-11-05", "ttr_horas": 3, "criticidade": "Alta"},
    {"id": "OS-009", "ativo": "Bomba-03", "sintoma": "Falha no inversor de frequência, bomba parou sem alarme prévio", "data": "2025-11-10", "ttr_horas": 5, "criticidade": "Média"},
    {"id": "OS-010", "ativo": "Compressor-02", "sintoma": "Vazamento no resfriador intermediário, perda de carga no circuito de ar", "data": "2025-11-18", "ttr_horas": 7, "criticidade": "Alta"},
]

with open("ordens.json", "w", encoding="utf-8") as f:
    json.dump(ordens, f, ensure_ascii=False, indent=2)

print("Dataset gerado com sucesso: ordens.json")
print(f"Total de ordens de serviço: {len(ordens)}")
print("\nAtivos no dataset:")
ativos = {}
for o in ordens:
    ativos[o["ativo"]] = ativos.get(o["ativo"], 0) + 1
for ativo, qtd in sorted(ativos.items(), key=lambda x: -x[1]):
    print(f"  {ativo}: {qtd} OS")
