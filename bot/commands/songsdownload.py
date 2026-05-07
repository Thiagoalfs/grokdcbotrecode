import discord, os, shutil
from generalFunctions import ytdlp, convert_mp3_ytdlp, upload_to_catbox

def setup_songs_commands(bot):
    @bot.command(name="baixe", aliases=["instale"])
    async def baixe(ctx, formato: str = None, url: str = None):
        if not formato or not url:
            await ctx.send("qual o link do que tu quer baixar? sintaxe: !baixe <mp3/mp4> <url>")
            return
        
        ydl_opts = {
            'noplaylist': True,
            'nocheckcertificate': True,
            'extractor_args': {
                'youtube': {
                    'remote_components': 'ejs:github', 
                    'player_client': ['android', 'web'],
                }
            }
        }

        try:
            if "mp3" in formato.lower():
                convert_mp3_ytdlp(ydl_opts)
                await ctx.send("baixando e convertendo pra mp3, calma ai um cadin...")
                nome_arquivo = await ytdlp(url, ydl_opts)

                nome_final = os.path.splitext(nome_arquivo)[0] + ".mp3"
            
            elif "mp4" in formato.lower():
                ydl_opts['format'] = 'bestvideo[ext=mp4][height=1080]+bestaudio[ext=m4a]/bestvideo[ext=mp4][height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]/bestaudio[ext=m4a]/best[ext=mp4]/best' # Prioriza MP4 em 1080p, depois 720p, com melhor áudio
                await ctx.send("baixando o vídeo em mp4, aguenta ai...")
                nome_arquivo = await ytdlp(url, ydl_opts)
                nome_final = nome_arquivo

                tamanho_bytes = os.path.getsize(nome_final)
                if tamanho_bytes > 8 * 1024 * 1024:
                    await ctx.send(f"Vídeo muito grande ({tamanho_bytes/(1024*1024):.2f}MB). Fazendo upload para o Catbox...")
                    link = await upload_to_catbox(nome_final)

                    if link:
                        await ctx.send(f"Aqui está o link do vídeo: {link}")
                    else:
                        await ctx.send("Erro ao fazer upload para o Catbox.")
                    
                    if os.path.exists("songs"):
                        shutil.rmtree("songs")
                    return
            
            else:
                await ctx.send("formato inválido. use mp3 ou mp4.")
                return

            with open(nome_final, "rb") as f:
                await ctx.send(file=discord.File(f, os.path.basename(nome_final)))
            
            if os.path.exists("songs"):
                shutil.rmtree("songs")
                
        except Exception as e:
            print(f"Erro detalhado no comando baixe: {e}")
            await ctx.send(f"erro ao processar: {type(e).__name__}. Verifique os logs do console para mais detalhes.")

            if os.path.exists("songs"):
                shutil.rmtree("songs")