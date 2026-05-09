import discord, random, json, os

def setup_lolgen_command(bot):
    @bot.command(name="lolgen")
    async def lolgen(ctx, *, champion_input: str = None):
        # Caminho subindo dois níveis (de commands/fun/ para bot/) para achar a pasta languages
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "languages", "ptbr", "lolgen.json")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                lol_data = json.load(f)
        except Exception as e:
            return await ctx.send(f"Erro ao ler o arquivo de dados do LoL: {e}")

        champions = lol_data["champions"]
        roles = lol_data["roles"]
        summoners = lol_data["summoners"]
        boots = lol_data["boots"]
        items = lol_data["items"]
        
        # Se um campeão foi passado como argumento, tenta encontrá-lo na lista
        if champion_input:
            champion = next((c for c in champions if c.lower() == champion_input.lower()), None)
            if not champion:
                return await ctx.send(f"❌ Não encontrei o campeão `{champion_input}` na minha lista.")
        else:
            # Caso contrário, sorteia um aleatório
            champion = random.choice(champions)
        
        # Formata o nome para a URL do Data Dragon (Riot Games)
        # Remove espaços, apóstrofos e pontos
        champ_id = champion.replace("'", "").replace(" ", "").replace(".", "")
        
        # Casos especiais onde o ID da imagem é diferente do nome exibido
        if champion == "Nunu & Willump": champ_id = "Nunu"
        if champion == "Wukong": champ_id = "MonkeyKing"
        if champion == "Renata Glasc": champ_id = "Renata"

        embed = discord.Embed(title="🎮 Desafio de Build", color=discord.Color.blue())
        embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_id}_0.jpg")
        
        embed.add_field(name="👤 Campeão", value=champion, inline=True)
        embed.add_field(name="🗺️ Rota", value=random.choice(roles), inline=False)
        embed.add_field(name="⚡ Feitiços", value=" & ".join(random.sample(summoners, 2)), inline=True)
        embed.add_field(name="⚔️ Itens", value=f"• {random.choice(boots)}\n"+"\n".join([f"• {i}" for i in random.sample(items, 5)]), inline=True)
        
        embed.set_footer(text=f"Boa sorte no Rift, {ctx.author.display_name}!")
        await ctx.send(embed=embed)