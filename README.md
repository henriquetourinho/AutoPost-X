# AutoPost-X: Bot para Pblicação Automática no X (Antigo Twitter)

O AutoPost-X é um script em Shell projetado para automatizar a publicação de links das postagens mais recentes de um usuário específico no X (antigo Twitter).

Ele utiliza a API oficial do X para buscar a última publicação feita por um usuário e, em seguida, publica automaticamente o link dessa postagem na sua conta autenticada no X. A publicação ocorre diretamente na conta do usuário que configurou o bot, oferecendo uma forma prática de compartilhar atualizações em tempo real sem a necessidade de interação manual.

Esse bot é perfeito para quem deseja compartilhar automaticamente os links das publicações mais recentes do X, garantindo que a audiência se mantenha informada sobre os novos conteúdos.

---

## Funcionalidades

- **Autenticação OAuth 2.0:** Gerencia o processo de autenticação para acessar a API.
- **Busca de Publicações:** Obtém o último post de um usuário específico.
- **Publicação Automática:** Publica a postagem recuperada no X utilizando a conta autenticada.

---

## Pré-requisitos

1. **Credenciais da API do X:**
   - Crie um aplicativo no [Portal de Desenvolvedores do X](https://developer.twitter.com/en/apps) e obtenha:
     - `API_KEY`
     - `API_SECRET_KEY`
     - `ACCESS_TOKEN`
     - `ACCESS_TOKEN_SECRET`

2. **Dependências:**
   - **`curl`**: Utilizado para requisições HTTP.
   - **`jq`**: Necessário para manipulação de dados JSON.
   - Para instalar no Ubuntu/Debian:
     ```bash
     sudo apt update && sudo apt install curl jq -y
     ```

3. **Sistema Operacional:**
   - Compatível com Linux/macOS. No Windows, utilize WSL (Windows Subsystem for Linux).

---

## Configuração

1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/henriquetourinho/AutoPost-X.git
   cd AutoPost-X
   ```

2. **Configuração das Credenciais:**
   - Abra o arquivo `autopost_x.sh` e insira as credenciais da API:
     ```bash
     API_KEY="SUA_API_KEY"
     API_SECRET_KEY="SEU_API_SECRET_KEY"
     ACCESS_TOKEN="SEU_ACCESS_TOKEN"
     ACCESS_TOKEN_SECRET="SEU_ACCESS_TOKEN_SECRET"
     USER_HANDLE="henriquetourinho"
     ```

3. **Permissão de Execução:**
   - Garanta que o script tenha permissão para execução:
     ```bash
     chmod +x autopost_x.sh
     ```

---

## Uso

1. **Executar o Script:**
   - Para iniciar o bot, execute:
     ```bash
     ./autopost_x.sh
     ```

2. **Fluxo de Execução:**
   - O script autentica com a API do X.
   - Recupera o último post do usuário especificado (`@henriquetourinho`).
   - Publica o conteúdo recuperado na conta autenticada.

---

## Personalização

- **Alterar o Usuário Alvo:**
  - Modifique a variável `USER_HANDLE` no script para o nome de usuário desejado.

- **Publicar um Conteúdo Diferente:**
  - Edite a mensagem na chamada da função `post_to_x` para adicionar ou modificar o texto.

---

## Dicas de Segurança

- **Proteção de Credenciais:**
  - Em vez de armazenar as credenciais no script, utilize variáveis de ambiente:
    ```bash
    export API_KEY="SUA_API_KEY"
    export API_SECRET_KEY="SEU_API_SECRET_KEY"
    export ACCESS_TOKEN="SEU_ACCESS_TOKEN"
    export ACCESS_TOKEN_SECRET="SEU_ACCESS_TOKEN_SECRET"
    ```
  - No script, substitua as credenciais pelo uso das variáveis de ambiente:
    ```bash
    API_KEY=${API_KEY}
    ```

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias ou correções.

---

Caso precise de ajustes ou mais detalhes, estou à disposição! 😊
