import discord
import os
import asyncio
import cloudscraper
import re
from bs4 import BeautifulSoup
from discord.ext import commands
from commands.languageservice import languageservice
from generalFunctions import upload_to_litterbox, ytdlp

class AnimeScraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.base_url = "https://anime.nexus" # Migrado para Anime Nexus

    def search_and_get_link(self, query):
        """Busca o anime e retorna o link da página principal."""
        print(f"[ANIME] Buscando: {query}", flush=True)
        # Anime Nexus usa query string: pesquisar?q=nome+do+anime
        search_url = f"{self.base_url}/pesquisar?q={query.replace(' ', '+')}"
        
        try:
            response = self.scraper.get(search_url, timeout=15)
            if response.status_code != 200: return None
        except Exception as e:
            print(f"[ANIME ERROR] Falha na busca: {e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # No Anime Nexus, os resultados ficam geralmente em cards
        result = soup.find('div', class_='anime-card') or soup.find('div', class_='card')
        if result and result.find('a'):
            href = result.find('a')['href']
            return href if href.startswith('http') else self.base_url + href
        return None

    def download_episode(self, url, path, bot):
        """Navega até o player e usa yt-dlp para baixar."""
        print(f"[ANIME] Acessando página: {url}", flush=True)
        try:
            response = self.scraper.get(url, timeout=15)
        except Exception as e:
            print(f"[ANIME ERROR] Erro ao acessar página do anime: {e}")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')

        # Pega o título real do anime
        title_tag = soup.find('h1') or soup.find('div', class_='anime-title')
        self.current_title = title_tag.text.strip() if title_tag else "Anime"

        # Procura o primeiro episódio na grade de episódios
        ep_tag = soup.find('div', class_='episodes-list') or soup.find('div', class_='grid')
        if ep_tag:
            ep_tag = ep_tag.find('a', href=True)
        
        if not ep_tag: 
            # Fallback: Procura qualquer link que pareça um episódio
            ep_tag = soup.find('a', href=re.compile(r'/(assistir|episodio)'))

        if not ep_tag:
            print("[ANIME] Erro: Nenhum episódio encontrado.", flush=True)
            return None

        player_url = ep_tag['href']
        if player_url.startswith('/'): player_url = self.base_url + player_url
        
        print(f"[ANIME] Episódio encontrado: {player_url}. Iniciando extração com yt-dlp...", flush=True)
        
        # Usamos o yt-dlp para baixar a partir do player
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{path}/anime_episode.mp4',
            'nocheckcertificate': True,
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        try:
            # Chama a sua função ytdlp que usa run_in_executor
            file_path = asyncio.run_coroutine_threadsafe(
                ytdlp(player_url, ydl_opts, folder=path), 
                bot.loop
            ).result()
            return file_path
        except Exception as e:
            print(f"[ANIME] Erro no download yt-dlp: {e}", flush=True)
            return None

scraper = AnimeScraper()

def setup_goanime_command(bot):
    @bot.command(name="goanime", aliases=["baixaranime", "animedl"])
    async def goanime_cmd(ctx, *, query: str = None):
        print(f"[DEBUG CMD] Comando goanime iniciado com query: {query}", flush=True)
        responses = await languageservice(bot, ctx, "fun", "goanime.json")

        if not query:
            return await ctx.send(responses["no_query"].format(prefix=ctx.prefix))

        # Pasta temporária para o anime
        anime_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "downloadedsongs", str(ctx.guild.id), "anime")
        os.makedirs(anime_path, exist_ok=True)

        msg = await ctx.send(responses["searching"].format(query=query))

        try:
            # Busca o anime (usando executor para não travar o bot)
            loop = asyncio.get_event_loop()
            anime_url = await loop.run_in_executor(None, scraper.search_and_get_link, query)

            if not anime_url:
                return await msg.edit(content=responses["not_found"])

            await msg.edit(content=responses["downloading"])

            # Realiza o download do episódio
            file_path = await loop.run_in_executor(None, scraper.download_episode, anime_url, anime_path, bot)

            if not file_path:
                return await msg.edit(content=responses["error"].format(error="Video source not found"))

            await msg.edit(content=responses["uploading"])

            # Upload para o Litterbox
            link = await upload_to_litterbox(file_path)

            if link:
                anime_display_name = getattr(scraper, 'current_title', query.title())
                await ctx.send(responses["success"].format(title=anime_display_name, link=link))
            else:
                await ctx.send(responses["error"].format(error="Upload failed"))

            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            print(f"[GOANIME ERROR] {e}")
            await ctx.send(responses["error"].format(error=str(e)))
        finally:
            try: await msg.delete()
            except: pass