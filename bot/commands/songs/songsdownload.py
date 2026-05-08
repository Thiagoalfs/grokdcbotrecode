import discord, os, shutil, asyncio
from generalFunctions import ytdlp, convert_mp3_ytdlp, upload_to_catbox

def setup_songs_commands(bot):
    @bot.command(name="baixe", aliases=["instale", "baixar"])
    async def baixe(ctx, formato: str = None, *, url: str = None):
        if not formato or not url:
            await ctx.send("qual o link do que tu quer baixar? sintaxe: .baixe <mp3/mp4> <url>")
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
                await ctx.send("baixando e convertendo pra mp3, calma ai um cadin...")
                nome_final = await ytdlp(url, ydl_opts, folder=baixe_path) # ytdlp agora retorna o caminho final do .mp3 após a conversão
            
            elif "mp4" in formato.lower():
                ydl_opts['format'] = 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]/bestaudio[ext=m4a]/best[ext=mp4]/best' # Prioriza MP4 em 1080p, depois 720p, com melhor áudio
                await ctx.send("baixando o vídeo em mp4, aguenta ai...")
                nome_arquivo = await ytdlp(url, ydl_opts, folder=baixe_path)
                nome_final = nome_arquivo

                tamanho_bytes = os.path.getsize(nome_final)
                if tamanho_bytes > 8 * 1024 * 1024:
                    await ctx.send(f"Vídeo muito grande ({tamanho_bytes/(1024*1024):.2f}MB). Fazendo upload para o Catbox...")
                    try:
                        link = await upload_to_catbox(nome_final)
                        if link:
                            await ctx.send(f"Aqui está o link do vídeo: {link}")
                        else:
                            await ctx.send("Erro ao fazer upload para o Catbox.")
                    finally:
                        if nome_final and os.path.exists(nome_final):
                            os.remove(nome_final)
            
            else:
                await ctx.send("formato inválido. use mp3 ou mp4.")
                return

            # Envia o arquivo passando o path direto, o discord.py gerencia melhor o I/O assim
            await ctx.send(file=discord.File(nome_final))
                
        except Exception as e:
            print(f"Erro detalhado no comando baixe: {e}")
            await ctx.send(f"erro ao processar: {type(e).__name__}. Verifique os logs do console para mais detalhes.")
        finally:
            # Garante que o arquivo seja deletado mesmo se der erro, mas espera um pouco pro Windows liberar
            await asyncio.sleep(2)
            if nome_final and os.path.exists(nome_final):
                os.remove(nome_final)