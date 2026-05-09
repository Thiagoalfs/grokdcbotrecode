import discord
from discord.ext import commands
from commands.languageservice import languageservice

def setup_prefix_command(bot):
    @bot.command(name="prefix", aliases=["prefixo", "setprefix"])
    @commands.has_permissions(administrator=True)
    async def prefix(ctx, new_prefix: str = None):
        responses = await languageservice(bot, ctx, "admin", "prefix.json")
        if not new_prefix:
            return await ctx.send(responses["current_prefix"].format(prefix=ctx.prefix))

        if len(new_prefix) > 5:
            return await ctx.send(responses["too_long"])

        await bot.db.execute("""
            INSERT INTO botsettings (guild_id, serverprefix) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE serverprefix = %s
        """, (ctx.guild.id, new_prefix, new_prefix))

        await ctx.send(responses["success"].format(prefix=new_prefix))

    @prefix.error
    async def prefix_error(ctx, error):
        responses = await languageservice(bot, ctx, "admin", "prefix.json")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(responses["no_permission"], delete_after=5)