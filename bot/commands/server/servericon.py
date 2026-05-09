import discord, json, os

def server_icon(bot):
    @bot.command(name="servericon")
    async def server_icon(ctx):
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "languages", "ptbr", "servericon.json")
        with open(json_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        guild = ctx.guild
        icon_url = guild.icon.url if guild.icon else None
        if icon_url:
            embed = discord.Embed(title=f"{guild.name}", color=discord.Color.blue())
            embed.set_image(url=icon_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(responses["no_icon"])