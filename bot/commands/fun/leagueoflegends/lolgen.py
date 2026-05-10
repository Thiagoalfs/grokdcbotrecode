import discord, random, json, os
from commands.languageservice import languageservice

def setup_lolgen_command(bot):
    @bot.command(name="lolgen")
    async def lolgen(ctx, *, champion_input: str = None):
        lol_data = await languageservice(bot, ctx, "fun/league of legends", "lolgen.json")
        if not lol_data:
            # Fallback message if translation data cannot be loaded
            return await ctx.send(f"{lol_data['error_loading_json_data']}")

        champions = lol_data["champions"]
        roles = lol_data["roles"]
        summoners_pool = lol_data["summoners"] # Renamed to avoid conflict with selected_summoners
        boots = lol_data["boots"]
        items = lol_data["items"]
        messages = lol_data["messages"]
        
        # Se um campeão foi passado como argumento, tenta encontrá-lo na lista
        if champion_input:
            champion = next((c for c in champions if c.lower() == champion_input.lower()), None)
            if not champion:
                return await ctx.send(messages["champion_not_found"].format(champion_input=champion_input))
        else:
            # Caso contrário, sorteia um aleatório
            champion = random.choice(champions)
        
        selected_role = random.choice(roles)
        
        selected_summoners = []
        # Assuming "Selva" (Jungle) is always the second element (index 1) in the roles list
        jungle_role_name = lol_data["roles"][1]
        # Assuming "Atirador" (Marksman/ADC) is always the fourth element (index 3) in the roles list
        marksman_role_name = lol_data["roles"][3]
        # Assuming "Suporte" (Support) is always the fifth element (index 4) in the roles list
        support_role_name = lol_data["roles"][4]
        # Assuming "Golpear" (Smite) is always the last element (index 8) in the summoners list
        smite_spell_name = lol_data["summoners"][8]

        if selected_role == jungle_role_name:
            selected_summoners.append(smite_spell_name)
            # Pick one more spell from the pool, excluding Smite
            remaining_summoners = [s for s in summoners_pool if s != smite_spell_name]
            if remaining_summoners: # Ensure there are other spells to pick
                selected_summoners.append(random.choice(remaining_summoners))
            random.shuffle(selected_summoners) # Shuffle to make the order random
        else:
            # Para outras rotas, escolha dois feitiços distintos do pool, excluindo "Golpear"
            non_jungle_summoners_pool = [s for s in summoners_pool if s != smite_spell_name]
            # Garante que há feitiços suficientes para escolher após excluir o Golpear
            selected_summoners = random.sample(non_jungle_summoners_pool, 2)
        
        # Formata o nome para a URL do Data Dragon (Riot Games)
        # Remove espaços, apóstrofos e pontos
        champ_id = champion.replace("'", "").replace(" ", "").replace(".", "")
        
        # Casos especiais onde o ID da imagem é diferente do nome exibido
        if champion == "Nunu & Willump": champ_id = "Nunu"
        if champion == "Wukong": champ_id = "MonkeyKing"
        if champion == "Renata Glasc": champ_id = "Renata"
        
        embed = discord.Embed(title=messages["challenge_title"], color=discord.Color.blue())
        embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_id}_0.jpg")
        
        embed.add_field(name=messages["champion_field"], value=champion, inline=True)
        embed.add_field(name=messages["role_field"], value=selected_role, inline=False)
        embed.add_field(name=messages["summoners_field"], value=" & ".join(selected_summoners), inline=True)
        
        if selected_role == marksman_role_name:
            selected_items = random.sample(items, 6)
        elif selected_role == support_role_name:
            # Seleciona 3 itens aleatórios + 1 item de suporte fixo (total 4).
            # O item de suporte é colocado no início da lista para aparecer logo abaixo da bota.
            selected_items = [messages["support_item_name"]] + random.sample(items, 4)
        else:
            selected_items = random.sample(items, 5)

        embed.add_field(name=messages["items_field"], value=f"• {random.choice(boots)}\n"+"\n".join([f"• {i}" for i in selected_items]), inline=True)
        
        embed.set_footer(text=messages["footer_text"].format(user_display_name=ctx.author.display_name))
        await ctx.send(embed=embed)