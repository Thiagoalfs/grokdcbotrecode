import discord
import os
import shutil # Importado para remover diretórios, se houver
from commands.songs.vcplay import song_queues

def setup_stop_command(bot):
    @bot.command(name="stop", aliases=["parar", "sair"])
    async def stop(ctx):
        guild_id = ctx.guild.id

        if not ctx.voice_client:
            return await ctx.send("não estou em nenhuma call ze")

        if not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.send("entra na call pra parar as músicas")

        # Stop current playback
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

        # Limpa a fila de músicas para este servidor
        if guild_id in song_queues:
            del song_queues[guild_id] # Remove the guild's entry entirely

        # Deleta a pasta específica deste servidor dentro de 'downloadedsongs'
        guild_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "downloadedsongs", str(guild_id))
        try:
            if os.path.exists(guild_folder):
                shutil.rmtree(guild_folder)
            print(f"Pasta do servidor '{guild_id}' limpa pelo comando !stop.")
        except Exception as e:
            print(f"Erro ao limpar a pasta do servidor no !stop: {e}")

        await ctx.send("flw")