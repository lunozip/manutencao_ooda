"""
OODA Loop com LLM - FASE 2: ORIENTAR
--------------------------------------
Aplica chain-of-thought prompting para análise de causa raiz
do ativo com maior frequência de falhas (Bomba-01).

Pré-requisitos:
  - Ollama instalado e rodando
  - Modelo llama3.2 baixado
  - Fase Observar já executada (observar.py)

Execução:
  python orientar.py
  python orientar.py > resultado_orientar.txt
"""

import json
import requests
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"


def verificar_ollama():
    try:
        requests.get("http://localhost:11434/", timeout=5)
    except Exception:
        print("ERRO: Ollama não está rodando.")
        print("Solução: abra o Ollama pela bandeja do sistema ou execute 'ollama serve'.")
        sys.exit(1)


def chamar_llm(prompt):
    print("Aguardando resposta do LLM (esta fase pode levar 60-90 segundos)...\n")
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=300
        )
        r.raise_for_status()
        return r.json()["response"]
    except requests.exceptions.Timeout:
        print("ERRO: timeout. Tente novamente ou use um modelo menor.")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO ao chamar o LLM: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("OODA LOOP + LLM  |  FASE 2: ORIENTAR")
    print("=" * 60)

    verificar_ollama()

    # Histórico de falhas da Bomba-01 extraído do dataset
    historico_bomba01 = [
        {"id": "OS-001", "data": "2025-08-10", "sintoma": "Vibração excessiva no mancal dianteiro, ruído metálico intermitente", "ttr_horas": 4},
        {"id": "OS-002", "data": "2025-09-03", "sintoma": "Vazamento de selo mecânico, presença de líquido no piso abaixo da bomba", "ttr_horas": 6},
        {"id": "OS-005", "data": "2025-10-01", "sintoma": "Vibração elevada após reparo anterior, desalinhamento suspeito, temperatura no rolamento acima do normal", "ttr_horas": 2},
        {"id": "OS-008", "data": "2025-11-05", "sintoma": "Desgaste acelerado do rolamento 6205, reincidência em menos de 90 dias após substituição", "ttr_horas": 3},
    ]

    linhas = [f"  {o['id']} ({o['data']}) — TTR: {o['ttr_horas']}h\n    Sintoma: {o['sintoma']}" for o in historico_bomba01]
    historico_texto = "\n".join(linhas)

    ttr_total = sum(o["ttr_horas"] for o in historico_bomba01)

    # Chain-of-thought prompt estruturado
    prompt = f"""Você é um engenheiro de confiabilidade sênior com especialização em análise de causa raiz (RCA) e metodologia RCM.

A Bomba-01 acumulou {len(historico_bomba01)} falhas nos últimos 90 dias, totalizando {ttr_total} horas de indisponibilidade.

HISTÓRICO CRONOLÓGICO DE FALHAS:
{historico_texto}

Realize uma análise de causa raiz completa seguindo rigorosamente este raciocínio passo a passo (chain-of-thought):

PASSO 1 — PROGRESSÃO CRONOLÓGICA
Descreva como os sintomas evoluíram ao longo do tempo. Existe uma sequência lógica de deterioração?

PASSO 2 — ANÁLISE DE CADA SINTOMA
Para cada OS, identifique:
- Modo de falha provável
- Mecanismo de dano associado
- Se é falha primária ou consequência de outra falha

PASSO 3 — IDENTIFICAÇÃO DA CAUSA RAIZ
Com base nos passos anteriores, qual é a causa raiz mais provável que explica TODOS os sintomas observados? Justifique.

PASSO 4 — CAUSAS CONTRIBUINTES
Liste fatores contribuintes que podem estar agravando o problema (manutenção, operação, projeto, lubrificação, etc.).

PASSO 5 — RECOMENDAÇÃO DE AÇÃO CORRETIVA
Qual intervenção definitiva eliminaria a causa raiz? Seja específico sobre o procedimento técnico.

PASSO 6 — AÇÃO PREVENTIVA DE LONGO PRAZO
Que mudança de prática ou tecnologia preditiva poderia detectar essa causa raiz antes da falha?

Responda em português, com linguagem técnica e objetiva."""

    resposta = chamar_llm(prompt)

    print("-" * 60)
    print("RESULTADO DA FASE ORIENTAR (Análise de Causa Raiz):")
    print("-" * 60)
    print(resposta)
    print("-" * 60)
    print(f"\nResumo do ativo analisado: Bomba-01")
    print(f"Total de falhas: {len(historico_bomba01)} | TTR acumulado: {ttr_total}h")
    print("\nFase Orientar concluída. Execute agora: python decidir_agir.py")


if __name__ == "__main__":
    main()
