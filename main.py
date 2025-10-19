"""
Case Técnico - Automação da Triagem de RH
Candidato: Geilson Machado
"""

import os
import shutil
import pandas as pd

# --- 1. CONSTANTES GLOBAIS ---
PASTA_EMAILS = "simulacao/emails_a_processar/"
PASTA_ANEXO_BASE = "simulacao/anexos_base/"
PASTA_CURRICULOS_SALVOS = "arquivos_processados/curriculos_salvos/"
ARQUIVO_RELATORIO = "arquivos_processados/relatorio_candidatos.xlsx"
ARQUIVO_ANEXO_SIMULADO = "curriculo_simulado.docx"


# --- 2. FUNÇÕES ---

def ler_conteudo_email(caminho_arquivo: str) -> str:
    """Abre e lê o arquivo .txt simulado com encoding 'utf-8'."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        return f.read()

def validar_e_separar_email(conteudo_email_completo: str) -> tuple:
    """
    Verifica o 'Assunto:' (filtro) e, se for válido,
    separa e retorna o corpo do e-mail.
    A ideia é seria que esse primeiro filtro 
    fosse feito através do N8N, com um gatilho
    """
    try:
        primeira_linha, resto_do_email = conteudo_email_completo.split('\n', 1)
        
        if "assunto: candidatura -" in primeira_linha.lower():
            corpo = resto_do_email.split('---CORPO---', 1)[1]
            return True, corpo
        else:
            return False, None
            
    except Exception as e:
        print(f"ERRO: Arquivo mal formatado, não foi possível validar. {e}")
        return False, None
    
def extrair_dados_candidato(corpo_email: str) -> dict:
    """
    Extrai os dados do candidato (Nome, Vaga, Telefone) do corpo.
    """
    dados = {"Nome": None, "Vaga": None, "Telefone": None}
    
    linhas = corpo_email.split('\n')
    
    # Meu raciocínio aqui foi ler linha por linha em vez de
    # esperar uma ordem fixa. Acredito que isso deixe a extração robusta
    # para os casos de "campos fora de ordem" e variações
    # como 'celular' ou 'nome completo'.
    for linha in linhas:
        linha_limpa = linha.lower().strip() 

        if (linha_limpa.startswith("nome:") or 
            linha_limpa.startswith("nome completo:")):
            dados["Nome"] = linha.split(':', 1)[1].strip()
            
        elif linha_limpa.startswith("vaga:"):
            dados["Vaga"] = linha.split(':', 1)[1].strip()
        
        elif (linha_limpa.startswith("telefone:") or 
              linha_limpa.startswith("celular:") or 
              linha_limpa.startswith("whatsapp:")):
            dados["Telefone"] = linha.split(':', 1)[1].strip()
            
    return dados

def processar_anexo_candidato(dados_candidato: dict, nome_arquivo_email: str) -> str:
    """
    Verifica a lógica de anexo (se existe, se o nome foi extraído)
    e simula o salvamento, retornando um status.
    """
    if "sem_anexo" in nome_arquivo_email.lower():
        return "ERRO: E-mail sem anexo"
        
    nome_candidato = dados_candidato.get("Nome")
    if not nome_candidato:
        return "ERRO: Nome não encontrado, não foi possível salvar o anexo"
        
    try:
        nome_novo_arquivo = f"{nome_candidato}.docx"
        
        caminho_origem = os.path.join(PASTA_ANEXO_BASE, ARQUIVO_ANEXO_SIMULADO)
        caminho_destino = os.path.join(PASTA_CURRICULOS_SALVOS, nome_novo_arquivo)
        
        shutil.copy(caminho_origem, caminho_destino)
        
        return "Sucesso"
        
    except Exception as e:
        print(f"ERRO: Falha ao copiar/salvar anexo: {e}")
        return f"ERRO: Falha ao salvar arquivo (verificar nome)"

def atualizar_relatorio_excel(dados: dict, status: str):
    """
    Atualiza a planilha de candidatos (relatorio_candidatos.xlsx).
    Se o arquivo não existir, ele é criado.
    """
    
    # Essa é a implementação do "Alertar o RH" do fluxograma.
    # Em um projeto real, aqui entraria a chamada pra uma API
    # de e-mail. Para esse protótipo, eu optei por usar 
    # um print no console simulando o alerta.
    
    if "ERRO" in status:
        nome_alerta = dados.get("Nome") or "Candidato Desconhecido"
        print(f"\n[ALERTA PARA O RH]: Detectado um erro: {status} | Candidato: {nome_alerta}\n")
    
    # Usei "or 'Não informado'" para garantir que o Excel
    # não fique com células vazias.
    nova_linha = {
        "Nome_Candidato": dados.get("Nome") or "Não informado",
        "Vaga_Desejada": dados.get("Vaga") or "Não informado",
        "Telefone": dados.get("Telefone") or "Não informado",
        "Status_Processamento": status
    }
    df_nova_linha = pd.DataFrame([nova_linha])
    
    try:
        df_existente = pd.read_excel(ARQUIVO_RELATORIO)
        df_final = pd.concat([df_existente, df_nova_linha], ignore_index=True)
        
    except FileNotFoundError:
        print(f"Arquivo '{ARQUIVO_RELATORIO}' não encontrado. Criando um novo...")
        df_final = df_nova_linha
    
    except Exception as e:
        print(f"ERRO ao ler o arquivo Excel: {e}")
        return 

    try:
        df_final.to_excel(ARQUIVO_RELATORIO, index=False)
    except Exception as e:
        print(f"ERRO ao salvar o arquivo Excel: {e}")

# --- 3. FUNÇÃO PRINCIPAL ---

def main():
    """
    Função principal que administra todo o processo.
    """
    print("--- INICIANDO AUTOMAÇÃO DE TRIAGEM de CURRÍCULOS ---")

    try:
        # Garante que as pastas de destino existam
        os.makedirs(PASTA_CURRICULOS_SALVOS, exist_ok=True)
        os.makedirs(os.path.dirname(ARQUIVO_RELATORIO), exist_ok=True) 
    except Exception as e:
        print(f"ERRO CRÍTICO: Não foi possível criar as pastas de destino: {e}")
        return

    try:
        arquivos_email = os.listdir(PASTA_EMAILS)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: A pasta '{PASTA_EMAILS}' não foi encontrada.")
        print("Verifique se a estrutura de pastas está correta.")
        return
    
    for nome_arquivo in arquivos_email:

        if not nome_arquivo.endswith(".txt"):
            continue

        print(f"\n--- Processando arquivo: {nome_arquivo} ---")
        
        # Meu raciocínio ao usar 'try...except' foi garantir que,
        # se um único e-mail falhar, a automação inteira não pare.
        # Ela registra o erro e continua para o próximo arquivo.
        
        try:
            caminho_completo = os.path.join(PASTA_EMAILS, nome_arquivo)
            
            conteudo_email_completo = ler_conteudo_email(caminho_completo)
            
            filtro_passou, corpo_do_email = validar_e_separar_email(conteudo_email_completo)
            
            if not filtro_passou:
                print(f"E-mail IGNORADO (Assunto não corresponde ao filtro).")
                continue

            print("E-mail APROVADO no filtro. Iniciando extração...")

            dados_candidato = extrair_dados_candidato(corpo_do_email)
            
            status_anexo = processar_anexo_candidato(dados_candidato, nome_arquivo)

            atualizar_relatorio_excel(dados_candidato, status_anexo)

            print(f"Processamento concluído para: {nome_arquivo}")

        except Exception as e:
            print(f"ERRO CRÍTICO ao processar {nome_arquivo}: {e}")
            dados_erro = {"Nome": f"Erro no arquivo {nome_arquivo}", "Vaga": "Não informado", "Telefone": "Não informado"}
            atualizar_relatorio_excel(dados_erro, f"ERRO CRÍTICO: {e}")
        
    print("\n--- PROCESSAMENTO DE TODOS OS E-MAILS CONCLUÍDO ---")

# --- 4. INICIAR FUNÇÃO MAIN ---
if __name__ == "__main__":
    main()