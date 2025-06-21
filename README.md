# 🤖 AutoPost-X — Automação Avançada para X (antigo Twitter)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/) [![Shell](https://img.shields.io/badge/Shell-Bash-green.svg)](https://www.gnu.org/software/bash/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

**Automatize postagens, monitore perfis, feeds RSS, publique imagens e muito mais no X (antigo Twitter) — agora com setup interativo, filtros inteligentes e logs detalhados!**

---

## 📖 Visão Geral

O **AutoPost-X** é um bot open source multifuncional para automação de postagens no X (antigo Twitter). O projeto evoluiu para atender diferentes públicos:

- **Versão Clássica:** Shell Script (`autopost_x.sh`) — simples, direta, para quem quer automatizar apenas o repost do último tweet de um usuário.
- **Versão Atual (Python):** Script Python avançado (`autopost_x.py`) — altamente configurável, suporta múltiplas fontes, modos de ação, filtros, geração de imagens, memória persistente e logs coloridos.

---

## 🎬 Funcionamento do Bot

Veja abaixo uma demonstração visual do funcionamento do AutoPost-X:

![Funcionamento do Bot](https://github.com/henriquetourinho/AutoPost-X/blob/main/media/funcionamento.gif?raw=true)

---

## 🆚 Comparativo: Versão Bash/Shell x Versão Python

| Recurso                              | `autopost_x.sh` (Shell) | `autopost_x.py` (Python)        |
|---------------------------------------|:-----------------------:|:-------------------------------:|
| Autenticação OAuth 2.0                | ✔️                      | ✔️                              |
| Busca e repost automático             | ✔️ (último tweet)       | ✔️ (vários modos e fontes)      |
| Setup interativo                      | ❌                      | ✔️                              |
| Monitoramento de múltiplos perfis     | ❌ (apenas 1 por vez)   | ✔️ (quantos quiser)             |
| Suporte a RSS                         | ❌                      | ✔️                              |
| Filtros por palavras-chave            | ❌                      | ✔️ (inclusão/exclusão)          |
| Modos de ação (Tweet, Quote, Imagem…) | ❌                      | ✔️ (5 modos: tweet, quote, imagem, retweet, like) |
| Geração de imagem                     | ❌                      | ✔️ (texto vira imagem com Pillow)|
| Memória persistente de posts           | ❌                      | ✔️ (evita repetir)              |
| Logs coloridos e detalhados           | ❌                      | ✔️ (terminal em português)      |
| Fácil evolução                        | ❌                      | ✔️ (código modular e comentado) |

---

## ⚡ Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/henriquetourinho/AutoPost-X.git
cd AutoPost-X
```

### 2. Escolha sua versão

#### 🐚 Versão Bash/Shell (`autopost_x.sh`)

- **Pré-requisitos:** `bash`, `curl`, `jq`
- **Configure:** Edite suas credenciais no início do arquivo `autopost_x.sh`.
- **Uso:**
    ```bash
    chmod +x autopost_x.sh
    ./autopost_x.sh
    ```
- **O que faz:**  
    - Busca o último post de um usuário do X e publica esse conteúdo em sua própria conta.
    - Simples, sem filtros, sem memória persistente.

---

#### 🐍 Versão Python (`autopost_x.py`)

- **Pré-requisitos:**  
    - Python 3.8 ou superior  
    - Instale as dependências:
        ```bash
        pip install tweepy feedparser Pillow
        ```
- **Primeira execução:**  
    ```bash
    python autopost_x.py
    ```
    - Você será guiado por um setup interativo no terminal (não precisa editar arquivos).
    - O arquivo `config.json` é gerado automaticamente para salvar suas preferências.
- **Principais recursos:**  
    - Monitora qualquer número de perfis do X **e** feeds RSS.
    - Permite definir filtros por palavras-chave (inclusão/exclusão).
    - Escolha o modo de ação: tweet, quote, imagem, retweet ou like.
    - Gera imagens com o texto do post e publica automaticamente (modo imagem).
    - Salva IDs de posts já processados para nunca repetir ação.
    - Logs coloridos e detalhados em português, facilitando o acompanhamento e troubleshooting.

---

## 📝 Exemplo de Configuração (Python)

Na primeira execução, o AutoPost-X vai perguntar:

- Suas chaves e tokens da API do X/Twitter
- Quais perfis e feeds RSS monitorar
- Palavras-chave para filtrar conteúdo
- Modo de ação padrão
- Opções de fonte e cor para geração de imagem (se desejar)

Tudo é salvo no `config.json`!

---

## 📦 Estrutura do Projeto

```
.
├── autopost_x.sh      # Script Shell clássico (simples)
├── autopost_x.py      # Script Python multifuncional (avançado)
├── config.json        # Configuração interativa (Python, gerado pelo usuário)
├── processed_ids.json # Posts já processados (Python, gerado automaticamente)
├── LICENSE            # Licença GNU GPL v3
└── README.md
```

---

## 📝 Requisitos

- **Python:** 3.8 ou superior
- **Dependências Python:**  
    ```bash
    pip install tweepy feedparser Pillow
    ```
- **Chaves da API do X/Twitter:**  
    Crie as suas em [developer.x.com](https://developer.x.com/)
- **Para Shell Script:**  
    - `bash`, `curl`, `jq`

---

## 📜 Licença

Este projeto é distribuído sob a **Licença GNU GPL v3**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🙋‍♂️ Autor e Colaboração

**Carlos Henrique Tourinho Santana**  
📍 Salvador - Bahia  
🔗 [Wiki Debian](https://wiki.debian.org/henriquetourinho)  
🔗 [LinkedIn](https://br.linkedin.com/in/carloshenriquetourinhosantana)  
🔗 [GitHub](https://github.com/henriquetourinho)

**Colaboração:**  
Código gerado, aprimorado e documentado pela IA do Google, sob direção do autor.

---

📢 **Projeto vivo: contribua, sugira melhorias ou abra uma issue!**