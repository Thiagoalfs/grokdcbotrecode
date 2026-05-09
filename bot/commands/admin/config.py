import discord
from discord.ext import commands
from commands.languageservice import languageservice

def setup_config_command(bot):
    @bot.command(name="config", aliases=["settings", "configurar"])
    @commands.has_permissions(administrator=True)
    async def config(ctx):
        responses = await languageservice(bot, ctx, "admin", "config.json")
        if not responses: return

        embed = discord.Embed(
            title=responses["title"],
            description=responses["desc"],
            color=discord.Color.blue()
        )

        # Mostra os comandos de prefixo e linguagem
        embed.add_field(name=f"{responses['field_prefix']} (`{ctx.prefix}prefix`)", value=responses["field_prefix_desc"], inline=False)
        embed.add_field(name=f"{responses['field_lang']} (`{ctx.prefix}language`)", value=responses["field_lang_desc"], inline=False)

        embed.set_footer(text=responses["footer"].format(prefix=ctx.prefix))

        await ctx.send(embed=embed)