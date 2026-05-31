"""
OODA Loop com LLM - FASES 3 e 4: DECIDIR e AGIR
--------------------------------------------------
Com base na causa raiz identificada na fase Orientar,
gera um plano de ação priorizado e o rascunho da
Ordem de Serviço em formato CMMS-ready.

Pré-requisitos:
  - Ollama instalado e rodando
  - Modelo llama3.2 baixado
  - Fases anteriores já executadas

Execução:
  python decidir_agir.py
  python decidir_agir.py > resultado_decidir_agir.txt
"""

import requests
import sys
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"

# ------------------------------------------------------------------
# ENTRADA: resultado da fase Orientar
# Em uma aplicação real, isso viria automaticamente do script anterior.
# Aqui está fixo para garantir reprodutibilidade do experimento.
# ------------------------------------------------------------------
CAUSA_RAIZ = "Desalinhamento crônico do eixo da Bomba-01 causado por base/fundação inadequada ou procedimento de alinhamento deficiente após intervenções."

CAUSAS_CONTRIBUINTES = [
    "Procedimento de alinhamento não verificado com precisão após OS-002",
    "Possível ausência de análise de vibração preditiva como rotina",
    "Rolamento 6205 substituído sem investigação da causa do desgaste acelerado (OS-008)",
]

ATIVO = "Bomba-01"
CRITICIDADE = "Alta"
TTR_ACUMULADO_HORAS = 15
# ------------------------------------------------------------------


def verificar_ollama():
    try:
        requests.get("http://localhost:11434/", timeout=5)
    except Exception:
        print("ERRO: Ollama não está rodando.")
        print("Solução: abra o Ollama pela bandeja do sistema ou execute 'ollama serve'.")
        sys.exit(1)


def chamar_llm(prompt, descricao=""):
    if descricao:
        print(f"Gerando: {descricao} (aguarde ~30 segundos)...\n")
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False},
            timeout=240
        )
        r.raise_for_status()
        return r.json()["response"]
    except requests.exceptions.Timeout:
        print("ERRO: timeout. Tente novamente.")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO ao chamar o LLM: {e}")
        sys.exit(1)


def fase_decidir():
    causas_texto = "\n".join(f"  - {c}" for c in CAUSAS_CONTRIBUINTES)

    prompt = f"""Você é um gerente de manutenção industrial responsável por priorizar intervenções.

ATIVO: {ATIVO}
CRITICIDADE: {CRITICIDADE}
CAUSA RAIZ IDENTIFICADA: {CAUSA_RAIZ}

CAUSAS CONTRIBUINTES:
{causas_texto}

IMPACTO ACUMULADO: {TTR_ACUMULADO_HORAS} horas de indisponibilidade nos últimos 90 dias.

Elabore um PLANO DE AÇÃO PRIORIZADO em três horizontes de tempo:

IMEDIATO (próximas 48h):
- Liste as ações emergenciais necessárias
- Indique os recursos humanos e materiais mínimos necessários

CURTO PRAZO (próximos 30 dias):
- Liste as ações corretivas definitivas
- Inclua procedimentos técnicos específicos
- Estime janela de parada necessária (horas)

LONGO PRAZO (próximos 6 meses):
- Liste melhorias de processo e práticas preventivas
- Indique tecnologias preditivas recomendadas

Para cada ação, indique: RESPONSÁVEL SUGERIDO | PRAZO | CRITÉRIO DE CONCLUSÃO

Responda em português, de forma objetiva e estruturada."""

    return chamar_llm(prompt, "plano de ação priorizado")


def fase_agir():
    data_hoje = datetime.date.today().strftime("%d/%m/%Y")

    prompt = f"""Você é um planejador de manutenção industrial experiente em sistemas CMMS.

Gere uma Ordem de Serviço completa e estruturada com base nas informações abaixo:

ATIVO: {ATIVO}
DATA DE ABERTURA: {data_hoje}
CAUSA RAIZ: {CAUSA_RAIZ}
CRITICIDADE: {CRITICIDADE}

A OS deve conter EXATAMENTE os seguintes campos, preenchidos com dados técnicos precisos:

ORDEM DE SERVIÇO
================
NÚMERO OS: [gere um número sequencial]
DATA DE ABERTURA: {data_hoje}
PRIORIDADE: [Urgente / Alta / Média / Baixa]

IDENTIFICAÇÃO DO ATIVO
Ativo: {ATIVO}
Tag/Localização: [sugira uma tag padrão]
Sistema: [sistema ao qual pertence]

DESCRIÇÃO DO SERVIÇO
Tipo de Manutenção: [Corretiva / Preventiva / Preditiva]
Descrição Detalhada: [descreva o serviço com precisão técnica, em 3-5 linhas]

CAUSA RAIZ IDENTIFICADA
[repita a causa raiz de forma concisa]

RECURSOS NECESSÁRIOS
Equipe: [função e quantidade de técnicos]
Ferramentas: [lista de ferramentas específicas]
Peças/Materiais: [lista com especificações técnicas]
EPI Necessário: [equipamentos de proteção]

PROCEDIMENTO RESUMIDO
[liste de 5 a 8 passos numerados do procedimento de execução]

CRITÉRIO DE ACEITAÇÃO
[condições mensuráveis para considerar o serviço concluído, ex: vibração < X mm/s]

ESTIMATIVA
Tempo de parada do ativo: [horas]
Janela de manutenção recomendada: [turno/período]

Responda em português. Seja específico e técnico — esta OS será usada diretamente pela equipe de campo."""

    return chamar_llm(prompt, "rascunho da Ordem de Serviço")


def main():
    print("=" * 60)
    print("OODA LOOP + LLM  |  FASES 3 e 4: DECIDIR e AGIR")
    print("=" * 60)
    print(f"\nAtivo analisado: {ATIVO}")
    print(f"Causa raiz: {CAUSA_RAIZ}\n")

    verificar_ollama()

    # FASE DECIDIR
    print("-" * 60)
    print("FASE 3 — DECIDIR: Plano de Ação Priorizado")
    print("-" * 60)
    plano = fase_decidir()
    print(plano)

    print("\n" + "=" * 60 + "\n")

    # FASE AGIR
    print("-" * 60)
    print("FASE 4 — AGIR: Rascunho da Ordem de Serviço")
    print("-" * 60)
    os_gerada = fase_agir()
    print(os_gerada)

    print("-" * 60)
    print("\nCiclo OODA completo!")
    print("Fases executadas: Observar → Orientar → Decidir → Agir")
    print(f"Ativo tratado: {ATIVO} | TTR acumulado evitado nas próximas intervenções: a mensurar")
    print("\nDica: salve os resultados com:")
    print("  python decidir_agir.py > resultado_ciclo_completo.txt")


if __name__ == "__main__":
    main()
