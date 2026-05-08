import discord

def server_info(bot):
    @bot.command(name="serverinfo")
    async def server_info(ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Dono", value=f"{guild.owner} \n({guild.owner_id})", inline=True)
        embed.add_field(name="Membros", value=guild.member_count, inline=True)   
        embed.add_field(name="Criado em", value=f"{discord.utils.format_dt(guild.created_at, style='f')} ({discord.utils.format_dt(guild.created_at, style='R')})", inline=True)
        await ctx.send(embed=embed)