from discord.ext import commands
from commands.languageservice import languageservice

def setup_league_link_command(bot):
    @bot.command(name="leaguelink", aliases=["vincularlol", "linkleague", "lollink", "linklol"])
    async def linkleague(ctx, *, riot_id: str = None):
        """Vincula sua conta do LoL ao Discord (Formato: Nome#Tag)"""
        responses = await languageservice(bot, ctx, "fun", "league_link.json")
        if riot_id is None:
            data = await bot.db.fetch_one("SELECT riot_id FROM leagueconfig WHERE user_id = %s", (ctx.author.id,))
            if data:
                return await ctx.send(responses["current_account"].format(riot_id=data['riot_id']))
            else:
                return await ctx.send(responses["no_account"].format(prefix=ctx.prefix))

        if "#" not in riot_id:
            return await ctx.send(responses["invalid_format"])

        await bot.db.execute("""
            INSERT INTO leagueconfig (user_id, riot_id) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE riot_id = %s
        """, (ctx.author.id, riot_id, riot_id))

        await ctx.send(responses["success"].format(riot_id=riot_id))