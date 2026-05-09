import discord, os, shutil
from commands.songs.vcplay import song_queues

def setup_stop_command(bot):
    @bot.command(name="stop", aliases=["parar", "sair", "dc"])
    async def stop(ctx):
        guild_id = ctx.guild.id

        if not ctx.voice_client:
            return await ctx.send("eu nem tô em call nenhuma, ze.")

        if not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.send("tu tem que tá na call pra me parar, pnc.")

        # Para a música e desconecta
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

        # Remove o servidor da fila global
        if guild_id in song_queues:
            del song_queues[guild_id]

        # Limpa os arquivos temporários do servidor
        guild_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "downloadedsongs", str(guild_id))
        try:
            if os.path.exists(guild_folder):
                shutil.rmtree(guild_folder)
            print(f"[CLEANUP] Pasta de áudio do servidor {guild_id} removida com sucesso.")
        except Exception as e:
            print(f"[ERROR] Falha ao limpar pasta do servidor {guild_id}: {e}")

        await ctx.send("parei tudo e saí da call. fé!")