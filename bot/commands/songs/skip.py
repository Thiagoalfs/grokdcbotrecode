import discord
from commands.languageservice import languageservice

def setup_skip_command(bot):
    @bot.command(name="skip", aliases=["s", "pular"])
    async def skip(ctx):
        responses = await languageservice(bot, ctx, "songs", "skip.json")

        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send(responses['nothing_playing'])

        if not ctx.author.voice or ctx.author.voice.channel != ctx.voice_client.channel:
            return await ctx.send(responses['not_in_vc'])

        # O stop() aciona o after_playing que definimos no vcplay.py, 
        # que por sua vez chama a próxima música da fila automaticamente.
        ctx.voice_client.stop()
        await ctx.send(responses['skipped'])