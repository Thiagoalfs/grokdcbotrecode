import random, discord, asyncio
from commands.languageservice import languageservice

def setup_gambling_command(bot):
    @bot.command(name="gambling", aliases=["gamble", "apostar"])
    async def gambling(ctx):
        # Busca as traduções baseadas no servidor/idioma
        responses = await languageservice(bot, ctx, "fun", "gambling.json")
        emojis = ["🎲", "🎰", "🃏", "💰", "💸", "🤑"]

        # Sorteia os 3 emojis que serão mostrados
        results = [random.choice(emojis) for _ in range(3)]

        # Cria o embed inicial com o primeiro emoji e placeholders (❓)
        embed = discord.Embed(title=responses['title'], color=discord.Color.gold())
        embed.description = f"**{results[0]}** | ❓ | ❓"
        msg = await ctx.send(embed=embed, reference=ctx.message)

        # Aguarda 1 segundo e revela o segundo emoji
        await asyncio.sleep(1)
        embed.description = f"**{results[0]}** | **{results[1]}** | ❓"
        await msg.edit(embed=embed)

        # Aguarda mais 1 segundo e revela o terceiro emoji
        await asyncio.sleep(1)
        embed.description = f"**{results[0]}** | **{results[1]}** | **{results[2]}**"

        # Lógica de vitória: verifica se todos os emojis são iguais
        if results[0] == results[1] == results[2]:
            embed.color = discord.Color.green()
            embed.add_field(name=responses['result_label'], value=responses['win'])
        else:
            embed.color = discord.Color.red()
            embed.add_field(name=responses['result_label'], value=responses['lose'])

        await msg.edit(embed=embed)
