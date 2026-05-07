import discord
import os
import shutil # Importado para remover diretórios, se houver
from commands.songs.vcplay import song_queues

def setup_stop_command(bot):
    @bot.command(name="stop", aliases=["parar", "sair"])
    async def stop(ctx):
        guild_id = ctx.guild.id

        if not ctx.voice_client:
            return await ctx.send("Não estou em nenhum canal de voz, ze.")

        if not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.send("Entra na call pra me parar, engraçadinho.")

        # Stop current playback
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

        # Limpa a fila de músicas para este servidor
        if guild_id in song_queues:
            del song_queues[guild_id] # Remove the guild's entry entirely

        # Deleta todos os arquivos e subpastas na pasta 'songs'
        songs_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "songs")
        try:
            if os.path.exists(songs_folder):
                shutil.rmtree(songs_folder)
            os.makedirs(songs_folder)
            print(f"Pasta '{songs_folder}' reiniciada pelo comando !stop.")
        except Exception as e:
            print(f"Erro ao reiniciar a pasta '{songs_folder}' no !stop: {e}")

        await ctx.send("Parei de tocar, saí da call e limpei a fila e a pasta de músicas. Até mais!")