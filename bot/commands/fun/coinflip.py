import random, discord
from commands.languageservice import languageservice

def coin_flip(bot):
    @bot.command(name="coinflip", aliases=["coin"])
    async def coin_flip(ctx):
        responses = await languageservice(bot, ctx, "fun", "coinflip.json")

        result = random.choice(["cara", "coroa"])
        await ctx.send(result, reference=ctx.message)