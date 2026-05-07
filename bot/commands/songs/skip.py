import discord

def setup_skip_command(bot):
    @bot.command(name="skip", aliases=["s", "pular"])
    async def skip(ctx):
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send("Não tem nada tocando pra eu pular, ze.")

        if not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.send("Entra na call pra pular a música, engraçadinho.")

        # O stop() aciona o after_playing que definimos no vcplay.py, 
        # que por sua vez chama a próxima música da fila automaticamente.
        ctx.voice_client.stop()
        await ctx.send("Pulei! Próxima...")