import discord

def userinfo(bot):
    @bot.command(name="userinfo", aliases=["user"])
    async def userinfo(ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        embed = discord.Embed(title=member.display_name, color=discord.Color.blue())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name=f"Informações de **{member.name}**")
        embed.add_field(name="**User**", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Conta criada em", value=f"{discord.utils.format_dt(member.created_at, style='f')} ({discord.utils.format_dt(member.created_at, style='R')})", inline=False)
        embed.add_field(name="Entrou em", value=f"{discord.utils.format_dt(member.joined_at, style='f')} ({discord.utils.format_dt(member.joined_at, style='R')})" if member.joined_at else "N/A", inline=False)
        await ctx.send(embed=embed, reference=ctx.message)