import discord, json, os

def ping(bot):
    @bot.command(name="ping")
    async def ping(ctx):
        await ctx.send("Pong!" + round(bot.latency * 1000))