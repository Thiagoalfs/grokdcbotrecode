import discord
from discord.ext import commands
from commands.languageservice import languageservice

def setup_ban_command(bot):
    @bot.command(name="ban", aliases=["banir"])
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason: str = None):
        responses = await languageservice(bot, ctx, "admin", "ban.json")
        reason = reason or responses["default_reason"]

        if member == ctx.author:
            return await ctx.send(responses["self_ban"], delete_after=5)
        if member == bot.user:
            return await ctx.send(responses["bot_ban"], delete_after=5)
        if ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id:
            return await ctx.send(responses["role_error"], delete_after=5)

        await member.ban(reason=reason)
        await ctx.send(responses["success"].format(user=member.display_name, reason=reason), delete_after=10)

    @ban.error
    async def ban_error(ctx, error):
        responses = await languageservice(bot, ctx, "admin", "ban.json")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(responses["no_permission"], delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(responses["bad_argument"].format(prefix=ctx.prefix), delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(responses["missing_arg"].format(prefix=ctx.prefix), delete_after=5)