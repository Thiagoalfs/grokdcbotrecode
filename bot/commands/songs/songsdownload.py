import discord, os, shutil, asyncio
from generalFunctions import ytdlp, convert_mp3_ytdlp, upload_to_catbox
from commands.languageservice import languageservice

def setup_songs_commands(bot):
    @bot.command(name="baixe", aliases=["instale", "baixar"])
    async def baixe(ctx, formato: str = None, *, url: str = None):
        responses = await languageservice(bot, ctx, "songs", "songsdownload.json")

        if not formato or not url:
            await ctx.send(responses['no_args'].format(prefix=ctx.prefix))
            return
        
        baixe_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "downloadedsongs", str(ctx.guild.id), "baixe")

        ydl_opts = {
            'noplaylist': True,
            'concurrent_fragment_downloads': 2,
            'ratelimit': 3145728, # Limite de 3MiB/s
            'nocheckcertificate': True,
            'default_search': 'ytsearch', # Permite pesquisar por nome se não for link
            'extractor_args': {
                'youtube': {
                    'remote_components': 'ejs:github', 
                    'player_client': ['ios', 'web', 'android'],
                }
            }
        }

        try:
            nome_final = None
            if "mp3" in formato.lower():
                convert_mp3_ytdlp(ydl_opts)
                await ctx.send(responses['downloading_mp3'])
                nome_final = await ytdlp(url, ydl_opts, folder=baixe_path) # ytdlp agora retorna o caminho final do .mp3 após a conversão
            
            elif "mp4" in formato.lower():
                ydl_opts['format'] = 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]/bestaudio[ext=m4a]/best[ext=mp4]/best' # Prioriza MP4 em 1080p, depois 720p, com melhor áudio
                await ctx.send(responses['downloading_mp4'])
                nome_arquivo = await ytdlp(url, ydl_opts, folder=baixe_path)
                nome_final = nome_arquivo

                tamanho_bytes = os.path.getsize(nome_final)
                if tamanho_bytes > 8 * 1024 * 1024:
                    await ctx.send(responses['video_too_large'].format(size=tamanho_bytes/(1024*1024)))
                    try:
                        link = await upload_to_catbox(nome_final)
                        if link:
                            await ctx.send(responses['catbox_link'].format(link=link))
                        else:
                            await ctx.send(responses['catbox_error'])
                    finally:
                        if nome_final and os.path.exists(nome_final):
                            os.remove(nome_final)
            
            else:
                await ctx.send(responses['invalid_format'])
                return

            # Envia o arquivo passando o path direto, o discord.py gerencia melhor o I/O assim
            await ctx.send(file=discord.File(nome_final))
                
        except Exception as e:
            print(f"Erro detalhado no comando baixe: {e}")
            await ctx.send(responses['error_processing'].format(error=type(e).__name__))
        finally:
            # Garante que o arquivo seja deletado mesmo se der erro, mas espera um pouco pro Windows liberar
            await asyncio.sleep(2)
            if nome_final and os.path.exists(nome_final):
                os.remove(nome_final)