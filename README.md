Scripts usado para gerar o artigo para submeter a 41º CBMGA
# OODA Loop + LLM para Gestão da Manutenção
## Prova de Conceito — CBMGA 2026

---

## Pré-requisitos

1. **Ollama** — https://ollama.com/download
   - Após instalar, abra um terminal e execute:
     ```
     ollama pull llama3.2
     ```

2. **Python 3.10+** — https://www.python.org/downloads/
   - Durante a instalação, marque "Add Python to PATH"
   - A única dependência externa é `requests`:
     ```
     pip install requests
     ```

---

## Execução (na ordem)

Coloque todos os arquivos .py na mesma pasta. Abra o terminal nessa pasta.

```
python gera_dataset.py      # Gera ordens.json
python observar.py          # Fase 1: Observar
python orientar.py          # Fase 2: Orientar
python decidir_agir.py      # Fases 3 e 4: Decidir e Agir
```

Para salvar as saídas em arquivo:
```
python observar.py      > resultado_observar.txt
python orientar.py      > resultado_orientar.txt
python decidir_agir.py  > resultado_ciclo_completo.txt
```

---

## Mapeamento OODA Loop

| Script            | Fase OODA | O que faz                                      |
|-------------------|-----------|------------------------------------------------|
| gera_dataset.py   | —         | Cria dataset sintético de OS                   |
| observar.py       | Observar  | Sumariza falhas e identifica padrões           |
| orientar.py       | Orientar  | Análise de causa raiz via chain-of-thought     |
| decidir_agir.py   | Decidir + Agir | Plano priorizado + rascunho de OS CMMS   |

---

## Requisitos de hardware

- RAM: 8GB mínimo (o modelo Llama 3.2 3B ocupa ~2GB)
- CPU: qualquer processador moderno (sem GPU necessária)
- Espaço em disco: ~3GB para o modelo
- OS: Windows 10/11, macOS 12+, Linux

---

## Solução de problemas

**"Connection refused" nos scripts Python**
→ O Ollama não está rodando. Abra o ícone na bandeja do sistema
  ou execute em outro terminal: `ollama serve`

**Resposta muito lenta**
→ Normal em CPU. O modelo 3B leva 30-90 segundos por chamada.
  Se quiser mais velocidade, use um PC com mais RAM ou GPU.

**"model not found"**
→ Execute: `ollama pull llama3.2`

---
