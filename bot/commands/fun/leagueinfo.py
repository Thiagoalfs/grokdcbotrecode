import discord
from discord.ext import commands
import aiohttp
from urllib.parse import quote
from commands.fun.leagueoflegends.riot_api_utils import fetch_riot_api
from commands.languageservice import languageservice

def setup_league_info_command(bot):
    @bot.command(name="leagueinfo", aliases=["lol", "lolstats", "lolprofile", "leagueprofile"])
    async def leagueinfo(ctx, member: discord.Member = None):
        """Mostra informações de LoL de um usuário vinculado"""
        responses = await languageservice(bot, ctx, "fun", "league_info.json")
        member = member or ctx.author
        data = await bot.db.fetch_one("SELECT riot_id FROM leagueconfig WHERE user_id = %s", (member.id,))
        if not data:
            return await ctx.send(responses["not_linked"].format(user=member.display_name, prefix=ctx.prefix))

        riot_id = data['riot_id']
        if "#" not in riot_id:
            return await ctx.send(responses["invalid_db_format"])
            
        name, tag = riot_id.rsplit("#", 1)
        name_encoded, tag_encoded = quote(name), quote(tag)

        # 1. Pegar PUUID (Account-V1)
        acc_data = await fetch_riot_api(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name_encoded}/{tag_encoded}")
        if not acc_data: 
            return await ctx.send(responses["account_not_found"].format(riot_id=riot_id))
        puuid = acc_data['puuid']

        # 2. Pegar Elos Diretamente por PUUID (League-V4)
        # O uso de by-puuid é o padrão atual da Riot para evitar a necessidade do summoner_id
        league_data = await fetch_riot_api(f"https://br1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}")
        
        if league_data is None:
            return await ctx.send(responses["rank_data_error"].format(riot_id=riot_id))
        
        solo_rank = responses["unranked"]
        flex_rank = responses["unranked"]

        for entry in league_data:
            wins = entry['wins']
            losses = entry['losses']
            total = wins + losses
            wr = (wins / total) * 100 if total > 0 else 0
            
            rank_str = f"{entry['tier']} {entry['rank']} ({entry['leaguePoints']} LP)\n{wins}W/{losses}L ({wr:.1f}%)"
            if entry['queueType'] == "RANKED_SOLO_5x5": solo_rank = rank_str
            elif entry['queueType'] == "RANKED_FLEX_SR": flex_rank = rank_str

        # 4. Pegar Maestria (Champion-Mastery-V4)
        mastery_data = await fetch_riot_api(f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count=1")
        
        champ_name = responses["unknown_champion"]
        champ_img = ""
        
        if mastery_data:
            champ_id = mastery_data[0]['championId']
            async with aiohttp.ClientSession() as session:
                async with session.get("https://ddragon.leagueoflegends.com/cdn/15.1.1/data/pt_BR/champion.json") as r:
                    if r.status == 200:
                        champions_data = await r.json()
                        for c_name, c_info in champions_data['data'].items():
                            if c_info['key'] == str(champ_id):
                                champ_name = c_name
                                champ_img = f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{c_name}_0.jpg"
                                break

        embed = discord.Embed(title=f"📊 {riot_id}", color=discord.Color.blue())
        if ctx.guild.icon:
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
            
        embed.add_field(name=responses["solo_rank"], value=solo_rank, inline=True)
        embed.add_field(name=responses["flex_rank"], value=flex_rank, inline=True)
        
        if mastery_data:
            mastery_pts = mastery_data[0]['championPoints']
            embed.add_field(name=responses["top_mastery"], value=responses["mastery_value"].format(champ=champ_name, pts=f"{mastery_pts:,}"), inline=False)
            embed.set_thumbnail(url=champ_img)

        await ctx.send(embed=embed)