# Análise do Case Técnico - Geilson Machado

Este é um breve resumo do meu raciocínio para resolver o case, respondendo às quatro perguntas propostas da documentação.

---

### 1. Qual ferramenta ou linguagem usaria para resolver esse problema e por quê? 

Para este protótipo, eu escolhi focar 100% em **Python**, que é a ferramenta que eu mais domino. Como o desafio principal era a lógica de extração de dados (e não a conexão real com o e-mail), achei que o Python era a opção ideal pois me daria flexibilidade processar os dados e tratar os erros.

Em um cenário de produção real, eu imagino que o **N8N** seria ótimo para ser o "gatilho" (monitorar a caixa de entrada) e ele então chamaria o script em **Python** para fazer o trabalho pesado de processar o texto. Acredito que seria uma boa forma de integrar os dois.

### 2. Quais desafios encontrou (ou imagina que encontraria)? 

Meu maior desafio foi pensar na extração dos dados. Eu vi o "Email 2 - Campos Fora de Ordem" e sabia que os candidatos não seguiriam um padrão fixo.

Pensei em usar Regex, mas honestamente, achei que poderia complicar demais o código e deixá-lo difícil de ler. Por isso, decidi fazer uma leitura linha por linha (como na função `extrair_dados_candidato`) e procurar por chaves com `startswith` e `or`. Achei que essa solução ficou mais simples, mais fácil de entender e robusta o suficiente para lidar com variações como "celular" ou "nome completo".

### 3. Como garantiria a confiabilidade dessa automação? 

Para a confiabilidade, minha maior preocupação era o script "morrer" no meio do caminho se um e-mail desse erro.

Por isso, minha principal decisão foi colocar o processamento de cada e-mail dentro de um bloco `try...except`, pois se um arquivo falhar, o script registra o erro no Excel e continua para o próximo, em vez de parar a automação inteira.

Além disso, fiz o script criar as próprias pastas (`os.makedirs`) e o arquivo Excel (`FileNotFoundError`) para que ele rode em qualquer lugar, mesmo que as pastas de destino não tenham sido criadas ainda.

Por fim, para ser fiel ao fluxograma, meu script também simula o 'Alerta ao RH'. Na função atualizar_relatorio_excel, se um status de 'ERRO' é detectado, ele imprime um alerta no console, mostrando onde a integração real com um e-mail seria colocada.

### 4. Quais melhorias futuras implementaria? 

1.  O passo mais óbvio seria fazer o script ler o conteúdo do curriculo em anexo (o PDF ou DOCX), e não só salvá-lo.

2.  A melhoria que eu mais gostaria de implementar, e que se conecta com a vaga, seria usar IA/LLMs. A ideia seria enviar o texto do currículo pra uma API (OpenAI, Gemini ou outra) e pedir para ela classificar o candidato (ex: "Júnior", "Pleno") ou extrair as skills dele. Isso seria salvo em novas colunas no Excel e automatizaria ainda mais a triagem.