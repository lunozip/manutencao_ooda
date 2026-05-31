"""
OODA Loop com LLM - FASE 1: OBSERVAR
-------------------------------------
Lê o dataset de ordens de serviço e solicita ao LLM local
uma sumarização estruturada, identificando padrões de falha.

Pré-requisitos:
  - Ollama instalado e rodando (ollama serve)
  - Modelo llama3.2 baixado (ollama pull llama3.2)
  - Arquivo ordens.json na mesma pasta (gerado por gera_dataset.py)

Execução:
  python observar.py
  python observar.py > resultado_observar.txt   (salva em arquivo)
"""

import json
import requests
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"


def verificar_ollama():
    try:
        r = requests.get("http://localhost:11434/", timeout=5)
        return True
    except Exception:
        print("ERRO: Ollama não está rodando.")
        print("Solução: abra o Ollama pela bandeja do sistema ou execute 'ollama serve' em outro terminal.")
        sys.exit(1)


def carregar_ordens():
    try:
        with open("ordens.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERRO: arquivo ordens.json não encontrado.")
        print("Solução: execute primeiro o script gera_dataset.py")
        sys.exit(1)


def chamar_llm(prompt):
    print("Aguardando resposta do LLM (pode levar 30-60 segundos)...\n")
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=180
        )
        r.raise_for_status()
        return r.json()["response"]
    except requests.exceptions.Timeout:
        print("ERRO: timeout. O modelo está demorando demais. Tente novamente.")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO ao chamar o LLM: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("OODA LOOP + LLM  |  FASE 1: OBSERVAR")
    print("=" * 60)

    verificar_ollama()
    ordens = carregar_ordens()

    print(f"Dataset carregado: {len(ordens)} ordens de serviço\n")

    # Formatar as OS para o prompt
    linhas = []
    for o in ordens:
        linhas.append(
            f"[{o['id']}] Ativo: {o['ativo']} | Data: {o['data']} | "
            f"Criticidade: {o['criticidade']} | TTR: {o['ttr_horas']}h\n"
            f"   Sintoma: {o['sintoma']}"
        )
    texto_os = "\n".join(linhas)

    prompt = f"""Você é um especialista em gestão da manutenção industrial com 20 anos de experiência.

Analise as ordens de serviço abaixo e forneça uma análise estruturada contendo:

1. FREQUÊNCIA DE FALHAS POR ATIVO: liste cada ativo e quantas OS possui, do mais crítico ao menos crítico.

2. PADRÕES DE SINTOMAS: identifique os tipos de falha mais recorrentes (vibração, vazamento, temperatura, etc.).

3. ATIVOS EM ALERTA: indique quais ativos merecem atenção imediata e por quê.

4. INDICADORES PRELIMINARES: estime o impacto em disponibilidade com base no TTR total por ativo.

5. ANOMALIAS IDENTIFICADAS: aponte qualquer padrão incomum, como reincidências rápidas ou falhas em cascata.

--- ORDENS DE SERVIÇO ---
{texto_os}
--- FIM DAS ORDENS ---

Responda em português, de forma objetiva e estruturada."""

    resposta = chamar_llm(prompt)

    print("-" * 60)
    print("RESULTADO DA FASE OBSERVAR:")
    print("-" * 60)
    print(resposta)
    print("-" * 60)
    print("\nFase Observar concluída. Execute agora: python orientar.py")


if __name__ == "__main__":
    main()
