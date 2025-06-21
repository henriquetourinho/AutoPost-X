# /*********************************************************************************
# * Projeto:   AutoPost-X
# * Script:    autopost-x.py
# * Autor:     Carlos Henrique Tourinho Santana
# * GitHub:    https://github.com/henriquetourinho/AutoPost-X
# *
# * Colaboração: Código gerado, aprimorado e documentado pela IA do Google,
# * a pedido e sob a direção do autor.
# * Data da Versão: 20 de junho de 2025
# *
# * Descrição:
# * Este é um bot multifuncional para a plataforma X (antigo Twitter), capaz
# * de automatizar postagens a partir de diversas fontes de conteúdo. Ele foi
# * projetado para ser altamente configurável e amigável, com um setup
# * interativo na primeira execução e um sistema de logs detalhado em português
# * para monitoramento completo de suas operações.
# *
# * Funcionalidades Principais:
# * - Setup Interativo: Configura o bot através de um diálogo no terminal.
# * - Múltiplas Fontes: Monitora usuários do X e feeds RSS.
# * - Modos de Ação: Pode tuitar, citar, gerar imagem, repostar ou curtir.
# * - Filtragem Inteligente: Filtra conteúdo por palavras-chave.
# * - Memória Persistente: Evita a repetição de posts já processados.
# * - Logs Detalhados: Exibe cada passo da execução de forma clara e colorida.
# *********************************************************************************/

import tweepy
import feedparser
from PIL import Image, ImageDraw, ImageFont
import json
import os
import textwrap
from datetime import datetime

# ==============================================================================
# --- MÓDULO DE LOG ---
# ==============================================================================

# Cores para o terminal
class Cores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(nivel, mensagem):
    """Exibe uma mensagem de log formatada e colorida."""
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    niveis = {
        "INFO": Cores.OKCYAN,
        "SUCESSO": Cores.OKGREEN,
        "AVISO": Cores.WARNING,
        "ERRO": Cores.FAIL,
        "ACAO": Cores.BOLD + Cores.HEADER
    }
    cor = niveis.get(nivel.upper(), Cores.ENDC)
    print(f"{cor}[{agora}] [{nivel.upper()}] {mensagem}{Cores.ENDC}")

# ==============================================================================
# --- MÓDULO DE CONFIGURAÇÃO INTERATIVA ---
# ==============================================================================

CONFIG_FILE = "config.json"

def pedir_lista(prompt):
    """Pede ao usuário para inserir itens para uma lista até ele dar Enter em branco."""
    items = []
    log("INFO", f"{prompt} (deixe em branco e tecle Enter quando terminar):")
    while True:
        item = input(f"  -> ")
        if not item:
            break
        items.append(item)
    return items

def setup_interativo():
    """Realiza uma entrevista com o usuário para criar o arquivo de configuração."""
    log("INFO", "Bem-vindo ao setup do AutoPost-X! Vamos configurar tudo para o primeiro uso.")
    config = {}

    log("ACAO", "--- Credenciais da API do X (Twitter) ---")
    log("AVISO", "Você pode encontrar todas estas chaves em https://developer.x.com/")
    config["API_KEY"] = input("API Key: ")
    config["API_SECRET_KEY"] = input("API Secret Key: ")
    config["ACCESS_TOKEN"] = input("Access Token: ")
    config["ACCESS_TOKEN_SECRET"] = input("Access Token Secret: ")
    config["BEARER_TOKEN"] = input("Bearer Token: ")

    log("ACAO", "--- Modo de Ação Principal ---")
    print("  1: TWEET      (Publica o texto diretamente)")
    print("  2: QUOTE      (Cita o post original com um comentário)")
    print("  3: IMAGE      (Cria uma imagem com o texto e a publica)")
    print("  4: RETWEET    (Apenas dá retweet no post original)")
    print("  5: LIKE       (Apenas curte o post original)")
    
    modo_map = {"1": "TWEET", "2": "QUOTE", "3": "IMAGE", "4": "RETWEET", "5": "LIKE"}
    while True:
        choice = input("Escolha o número do modo de ação padrão: ")
        if choice in modo_map:
            config["ACTION_MODE"] = modo_map[choice]
            break
        else:
            log("ERRO", "Escolha inválida. Por favor, digite um número de 1 a 5.")

    log("ACAO", "--- Fontes de Conteúdo ---")
    config["SOURCES"] = {}
    config["SOURCES"]["twitter_users"] = pedir_lista("Digite os @usuários do X que você quer monitorar, um por vez.")
    
    rss_dict = {}
    log("INFO", "Digite os Feeds RSS que você quer monitorar.")
    while True:
        nome = input("  Nome do Feed (ex: G1 Tecnologia) (deixe em branco para pular): ")
        if not nome:
            break
        url = input(f"  URL do Feed para '{nome}': ")
        if url:
            rss_dict[nome] = url
    config["SOURCES"]["rss_feeds"] = rss_dict

    log("ACAO", "--- Filtros de Conteúdo ---")
    config["FILTERS"] = {}
    config["FILTERS"]["include_keywords"] = pedir_lista("Palavras-chave de INCLUSÃO (o post DEVE ter uma delas).")
    config["FILTERS"]["exclude_keywords"] = pedir_lista("Palavras-chave de EXCLUSÃO (o post NÃO PODE ter nenhuma delas).")

    log("ACAO", "--- Configurações Adicionais ---")
    config["COMMENT_FOR_QUOTE_TWEET"] = input("Comentário padrão para o modo 'QUOTE': ") or "Olha que interessante isso aqui! 👇"
    config["IMAGE_SETTINGS"] = {
        "font_path": input("Caminho para o arquivo da fonte .ttf (ex: Roboto-Regular.ttf): ") or "Roboto-Regular.ttf",
        "font_size": 40, "image_width": 1080, "image_height": 1080,
        "bg_color": "#15202B", "text_color": "#FFFFFF",
        "temp_image_name": "temp_post_image.png"
    }

    try:
        with open(CONFIG_FILE, "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        log("SUCESSO", f"Configuração salva com sucesso em '{CONFIG_FILE}'!")
        return config
    except Exception as e:
        log("ERRO", f"Não foi possível salvar o arquivo de configuração: {e}")
        return None

def carregar_config():
    """Carrega a configuração do arquivo JSON, ou inicia o setup se ele não existir."""
    if not os.path.exists(CONFIG_FILE):
        log("AVISO", f"Arquivo '{CONFIG_FILE}' não encontrado.")
        return setup_interativo()
    else:
        try:
            with open(CONFIG_FILE, "r", encoding='utf-8') as f:
                config = json.load(f)
                log("INFO", f"Configuração carregada de '{CONFIG_FILE}'.")
                return config
        except Exception as e:
            log("ERRO", f"Não foi possível ler o arquivo de configuração: {e}")
            return None

# ==============================================================================
# --- LÓGICA PRINCIPAL DO BOT (COM LOGS DETALHADOS) ---
# ==============================================================================
            
def create_tweet_image(config, text, author):
    """Cria uma imagem a partir de um texto usando Pillow."""
    cfg = config["IMAGE_SETTINGS"]
    try:
        font = ImageFont.truetype(cfg["font_path"], cfg["font_size"])
        author_font = ImageFont.truetype(cfg["font_path"], int(cfg["font_size"] * 0.75))
    except IOError:
        log("ERRO", f"Fonte não encontrada em '{cfg['font_path']}'. Verifique o caminho no config.json.")
        return None

    img = Image.new('RGB', (cfg["image_width"], cfg["image_height"]), color=cfg["bg_color"])
    draw = ImageDraw.Draw(img)
    margin, max_width = 60, cfg["image_width"] - 120
    lines = textwrap.wrap(text, width=int(max_width / (cfg["font_size"] * 0.5)))
    y_text = margin
    for line in lines:
        draw.text((margin, y_text), line, font=font, fill=cfg["text_color"])
        y_text += font.getbbox(line)[3] + 10
    draw.text((margin, y_text + 20), f"- {author}", font=author_font, fill=cfg["text_color"])
    img.save(cfg["temp_image_name"])
    log("INFO", f"Imagem temporária '{cfg['temp_image_name']}' criada com sucesso.")
    return cfg["temp_image_name"]

def main():
    log("INFO", "========================================")
    log("INFO", "Iniciando execução do AutoPost-X...")
    log("INFO", "========================================")
    
    config = carregar_config()
    if not config:
        log("ERRO", "Falha ao carregar a configuração. Encerrando o script.")
        return

    # Autenticação
    try:
        client_write = tweepy.Client(
            consumer_key=config["API_KEY"], consumer_secret=config["API_SECRET_KEY"],
            access_token=config["ACCESS_TOKEN"], access_token_secret=config["ACCESS_TOKEN_SECRET"]
        )
        client_read = tweepy.Client(config["BEARER_TOKEN"])
        auth_v1 = tweepy.OAuth1UserHandler(
            consumer_key=config["API_KEY"], consumer_secret=config["API_SECRET_KEY"],
            access_token=config["ACCESS_TOKEN"], access_token_secret=config["ACCESS_TOKEN_SECRET"]
        )
        api_v1 = tweepy.API(auth_v1)
        log("SUCESSO", "Autenticação com a API do X realizada.")
    except Exception as e:
        log("ERRO", f"Falha fatal na autenticação: {e}")
        return

    # Carregar IDs já processados
    STATE_FILE = "processed_ids.json"
    try:
        with open(STATE_FILE, 'r') as f: processed_ids = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        processed_ids = set()
    log("INFO", f"{len(processed_ids)} IDs já processados foram carregados.")

    # Coleta de conteúdo
    content_queue = []
    for username in config["SOURCES"]["twitter_users"]:
        log("INFO", f"Buscando posts de @{username}...")
        try:
            user_info = client_read.get_user(username=username)
            if not user_info.data: 
                log("AVISO", f"Usuário @{username} não encontrado."); continue
            
            tweets = client_read.get_users_tweets(id=user_info.data.id, max_results=10, exclude=["retweets", "replies"])
            if tweets.data:
                for tweet in tweets.data:
                    if str(tweet.id) in processed_ids: continue
                    
                    text_lower = tweet.text.lower()
                    exclude_list = config["FILTERS"].get("exclude_keywords", [])
                    include_list = config["FILTERS"].get("include_keywords", [])

                    if exclude_list and any(k.lower() in text_lower for k in exclude_list):
                        log("AVISO", f"Post de @{username} ignorado por filtro de exclusão.")
                        continue
                    if include_list and not any(k.lower() in text_lower for k in include_list):
                        log("AVISO", f"Post de @{username} ignorado por não conter palavra-chave de inclusão.")
                        continue
                        
                    content_queue.append({"id": str(tweet.id), "text": tweet.text, "author": f"@{username}", "source": "twitter"})
        except Exception as e:
            log("ERRO", f"Não foi possível buscar tweets de @{username}: {e}")

    for name, url in config["SOURCES"]["rss_feeds"].items():
        log("INFO", f"Verificando feed RSS: {name}")
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            entry_id = entry.get("id", entry.get("link"))
            if entry_id not in processed_ids:
                text = f"{entry.title}\n\n{entry.link}"
                text_lower = text.lower()
                exclude_list = config["FILTERS"].get("exclude_keywords", [])
                include_list = config["FILTERS"].get("include_keywords", [])

                if exclude_list and any(k.lower() in text_lower for k in exclude_list):
                    log("AVISO", f"Item RSS '{entry.title}' ignorado por filtro de exclusão.")
                    continue
                if include_list and not any(k.lower() in text_lower for k in include_list):
                    log("AVISO", f"Item RSS '{entry.title}' ignorado por não conter palavra-chave de inclusão.")
                    continue
                
                content_queue.append({"id": entry_id, "text": text, "author": name, "source": "rss"})


    if not content_queue:
        log("INFO", "Nenhum post novo encontrado nas fontes. Nenhuma ação a ser tomada.")
    else:
        log("SUCESSO", f"{len(content_queue)} novo(s) item(ns) encontrado(s) e válidos!")
        item = content_queue[0]
        log("ACAO", f"Tentando executar a ação '{config['ACTION_MODE']}' para o item de '{item['author']}'...")
        log("INFO", f"Conteúdo: {item['text'][:100]}...")
        
        try:
            mode = config['ACTION_MODE'].upper()
            response = None
            if mode == 'TWEET':
                response = client_write.create_tweet(text=item['text'])
            elif mode == 'QUOTE' and item['source'] == 'twitter':
                response = client_write.create_tweet(text=config["COMMENT_FOR_QUOTE_TWEET"], quote_tweet_id=item['id'])
            elif mode == 'IMAGE':
                image_path = create_tweet_image(config, item['text'], item['author'])
                if image_path:
                    media = api_v1.media_upload(filename=image_path)
                    response = client_write.create_tweet(media_ids=[media.media_id_string])
                    os.remove(image_path)
            elif mode == 'RETWEET' and item['source'] == 'twitter':
                response = client_write.retweet(item['id'])
            elif mode == 'LIKE' and item['source'] == 'twitter':
                response = client_write.like(item['id'])
            
            if response and response.data:
                tweet_id = response.data.get('id') or item.get('id')
                log("SUCESSO", f"Ação '{mode}' executada! ID: {tweet_id}")
                if tweet_id: log("SUCESSO", f"Link: https://x.com/any/status/{tweet_id}")
                processed_ids.add(item['id'])
            else:
                log("AVISO", f"A ação '{mode}' não produziu um resultado válido ou não é compatível com a fonte '{item['source']}'.")

        except Exception as e:
            log("ERRO", f"Falha ao executar a ação '{mode}': {e}")

    with open(STATE_FILE, 'w') as f: json.dump(list(processed_ids), f)
    log("INFO", "IDs processados foram salvos.")
    log("INFO", "Execução do AutoPost-X finalizada.")


if __name__ == "__main__":
    main()