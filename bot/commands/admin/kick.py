import discord
from discord.ext import commands
from commands.languageservice import languageservice

def setup_kick_command(bot):
    @bot.command(name="kick", aliases=["expulsar"])
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason: str = None):
        responses = await languageservice(bot, ctx, "admin", "kick.json")
        reason = reason or responses["default_reason"]

        if member == ctx.author:
            return await ctx.send(responses["self_kick"], delete_after=5)
        if member == bot.user:
            return await ctx.send(responses["bot_kick"], delete_after=5)
        if ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(responses["role_error"], delete_after=5)

        await member.kick(reason=reason)
        await ctx.send(responses["success"].format(user=member.display_name, reason=reason), delete_after=10)

    @kick.error
    async def kick_error(ctx, error):
        responses = await languageservice(bot, ctx, "admin", "kick.json")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(responses["no_permission"], delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(responses["bad_argument"].format(prefix=ctx.prefix), delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(responses["missing_arg"].format(prefix=ctx.prefix), delete_after=5)