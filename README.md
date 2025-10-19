# [Case Técnico] Automação da Triagem de RH - Geilson Machado

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)

Este repositório contém a minha solução completa para o case de Estágio em Automação e Desenvolvimento. O projeto é um protótipo em Python que simula um processo de RPA: ele lê uma pasta de e-mails simulados (na pasta `/simulacao`), filtra por assunto, extrai dados do corpo, processa os anexos e gera um relatório dos candidatos em Excel (`.xlsx`) com o status de cada candidatura.

## 🚀 Tecnologias Utilizadas

* **Python 3**
* **Pandas:** Para a criação e atualização da planilha Excel.
* **OS / Shutil:** Para a manipulação de arquivos e pastas.

## ⚙️ Como Executar o Protótipo

Para rodar este projeto e testar a automação, basta seguir os 5 passos abaixo.

### 1. Clonar o Repositório

```bash
# Clone o repositório usando o comando abaixo.
git clone https://github.com/gtmachado/case-automacao-liber-geilson-machado.git

# Entre na pasta do projeto
cd case-automacao-liber-geilson-machado
```
### 2. Criar e Ativar o Ambiente Virtual (venv)

```bash
# Crie o ambiente virtual (funciona em todos os terminais)
python -m venv venv
```
```bash
# No Windows (CMD ou PowerShell)
.\venv\Scripts\activate
```
```bash
# No Windows (Git Bash)
source venv/Scripts/activate
```
```bash
# No macOS/Linux
python3 -m venv venv  # (Use python3 se 'python' não funcionar)
source venv/bin/activate
```

### 3. Instalar as Dependências

Todas as bibliotecas necessárias estão listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```
### 4. Executar a Automação

O script `main.py` executará todo o processo. Os arquivos de e-mail de teste (incluindo alguns cenários extras) já estão incluídos na pasta `/simulacao/emails_a_processar/`.

```bash
python main.py
```
### 5. Verificar os Resultados

Após a execução (que leva 1-2 segundos), o script criará a pasta `/arquivos_processados/`. Dentro dela, você encontrará:

* **`relatorio_candidatos.xlsx`**: A planilha em Excel com o log de todos os e-mails processados (incluindo sucessos e erros).
* **`/curriculos_salvos/`**: Os arquivos de anexo que foram salvos com sucesso (com o nome do candidato).

---

## 📂 Entregáveis do Case

Este repositório está organizado com todos os entregáveis obrigatórios do desafio:

* **Parte 1: Desenho da Solução:** O fluxograma do processo está localizado em:
    * `./entregaveis/Fluxograma_Triagem_RH.pdf`

* **Parte 2: Implementação:** O código-fonte completo da solução em Python está em:
    * `./main.py`

* **Parte 3: Documentação Curta:** A análise estratégica respondendo às quatro perguntas está em:
    * `./entregaveis/DOCUMENTACAO.MD`