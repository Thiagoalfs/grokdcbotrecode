import discord, json, os

def ping(bot):
    @bot.command(name="ping")
    async def ping(ctx):
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "languages", "ptbr", "ping.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)
            
        await ctx.send(responses["response"].format(latency=round(bot.latency * 1000)))