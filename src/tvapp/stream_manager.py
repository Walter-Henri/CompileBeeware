import logging
from streamlink import Streamlink
from libsql_client import create_client
from dotenv import load_dotenv
import asyncio
import os

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class StreamManager:
    def __init__(self):
        self.session = Streamlink()
        self.session.set_option("stream-timeout", 30)
        self.session.set_option("retry-stream", 3)
        self.session.set_option("http-header", "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        self.session.set_option("stream-segment-threads", 3)

    async def get_db_client(self):
        """Inicializa o cliente do banco de dados Turso."""
        database_url = os.getenv("DATABASE_URL", "").replace("libsql://", "https://")
        auth_token = os.getenv("DATABASE_AUTH_TOKEN")
        if not database_url or not auth_token:
            logger.error("DATABASE_URL ou DATABASE_AUTH_TOKEN não configurados")
            return None
        
        try:
            client = create_client(url=database_url, auth_token=auth_token)
            await client.execute("SELECT 1")
            logger.info(f"Conexão HTTPS com {database_url} estabelecida com sucesso")
            return client
        except Exception as e:
            logger.error(f"Falha ao conectar ao banco: {str(e)}", exc_info=True)
            return None

    def extract_m3u8_with_streamlink(self, url):
        """Extrai link M3U8 usando streamlink."""
        try:
            streams = self.session.streams(url)
            
            # Prioriza o stream "best" (melhor qualidade) se for M3U8
            if "best" in streams and streams["best"].url.endswith(".m3u8"):
                return streams["best"].url
            # Fallback para "worst" (menor qualidade) se "best" não for M3U8
            elif "worst" in streams and streams["worst"].url.endswith(".m3u8"):
                return streams["worst"].url
            else:
                return ""
        except Exception as e:
            logger.error(f"Erro ao extrair stream com streamlink: {str(e)}")
            return ""
    async def update_live_links(self, live_urls):
        """Atualiza os links das lives no banco de dados."""
        client = await self.get_db_client()
        if not client:
            return False

        try:
            # Cria a tabela no banco, se não existir
            await client.execute("CREATE TABLE IF NOT EXISTS live_links (name TEXT PRIMARY KEY, url TEXT)")

            # Processa cada live
            for live in live_urls:
                logger.info(f"Processando {live["name"]} - {live["url"]}")
                
                # Tenta com streamlink
                m3u8_url = self.extract_m3u8_with_streamlink(live["url"])
                
                # Atualiza o banco de dados com o link encontrado
                if m3u8_url:
                    logger.info(f"Link M3U8 para {live["name"]}: {m3u8_url}")
                    await client.execute("INSERT OR REPLACE INTO live_links (name, url) VALUES (?, ?)", (live["name"], m3u8_url))
                else:
                    logger.warning(f"Nenhum link M3U8 válido para {live["name"]}")
                    await client.execute("INSERT OR REPLACE INTO live_links (name, url) VALUES (?, ?)", (live["name"], ""))

            return True
        except Exception as e:
            logger.error(f"Erro ao atualizar links: {str(e)}")
            return False
        finally:
            await client.close()

    async def get_live_link(self, live_name):
        """Busca o link de uma live específica no banco de dados."""
        client = await self.get_db_client()
        if not client:
            return None

        try:
            result = await client.execute(
                "SELECT url FROM live_links WHERE name = ?", (live_name,)
            )
            if result.rows and result.rows[0][0]:
                return result.rows[0][0]
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar link para {live_name}: {str(e)}")
            return None
        finally:
            await client.close()

