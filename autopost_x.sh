#!/bin/bash

# Credenciais da API do X (antigo Twitter)
API_KEY="SUA_API_KEY"
API_SECRET_KEY="SEU_API_SECRET_KEY"
ACCESS_TOKEN="SEU_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET="SEU_ACCESS_TOKEN_SECRET"

# Novo domínio da API
BASE_URL="https://api.x.com/2"
USER_HANDLE="usuario"

# Função para autenticação com OAuth 2.0
get_bearer_token() {
    curl -s -X POST "https://api.x.com/oauth2/token" \
        -u "${API_KEY}:${API_SECRET_KEY}" \
        -d "grant_type=client_credentials" | jq -r '.access_token'
}

# Função para buscar o último tweet (postagem) de um usuário
get_latest_post() {
    local bearer_token=$1
    local user_id=$(curl -s -X GET "${BASE_URL}/users/by/username/${USER_HANDLE}" \
        -H "Authorization: Bearer ${bearer_token}" | jq -r '.data.id')

    curl -s -X GET "${BASE_URL}/users/${user_id}/tweets?max_results=1" \
        -H "Authorization: Bearer ${bearer_token}" | jq -r '.data[0].text'
}

# Função para postar no X
post_to_x() {
    local bearer_token=$1
    local post_content=$2
    curl -s -X POST "${BASE_URL}/tweets" \
        -H "Authorization: Bearer ${bearer_token}" \
        -H "Content-Type: application/json" \
        -d "{\"text\":\"${post_content}\"}"
}

# Autenticação e execução
BEARER_TOKEN=$(get_bearer_token)

if [[ -z "$BEARER_TOKEN" ]]; then
    echo "Erro ao obter token de autenticação."
    exit 1
fi

# Obter o último post do usuário
LATEST_POST=$(get_latest_post "$BEARER_TOKEN")

if [[ -z "$LATEST_POST" ]]; then
    echo "Erro ao buscar o último post de @${USER_HANDLE}."
    exit 1
fi

# Publicar o último post no X
RESPONSE=$(post_to_x "$BEARER_TOKEN" "Última publicação de @${USER_HANDLE}: $LATEST_POST")

if echo "$RESPONSE" | grep -q '"id":'; then
    echo "Última publicação de @${USER_HANDLE} publicada com sucesso."
else
    echo "Erro ao publicar no X: $RESPONSE"
fi

