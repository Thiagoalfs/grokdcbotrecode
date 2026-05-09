import random, discord, json, os

def coin_flip(bot):
    @bot.command(name="coinflip", aliases=["coin"])
    async def coin_flip(ctx):
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "languages", "ptbr", "coinflip.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        result = random.choice("cara", "coroa")
        await ctx.send(result, reference=ctx.message)