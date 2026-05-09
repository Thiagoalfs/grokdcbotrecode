import discord
from discord.ui import Button, View
from commands.songs.vcplay import song_queues
from commands.languageservice import languageservice

class QueueView(View):
    def __init__(self, guild_id, pages, responses, current_page=0):
        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.pages = pages
        self.responses = responses
        self.current_page = current_page

    def create_embed(self):
        songs = self.pages[self.current_page]
        description = ""
        for i, song in enumerate(songs):
            index = (self.current_page * 5) + i + 1
            description += f"`{index}.` {song['title']}\n"

        embed = discord.Embed(title=self.responses['title'], description=description, color=discord.Color.blue())
        embed.set_footer(text=self.responses['footer'].format(current=self.current_page + 1, total=len(self.pages)))
        return embed

    @discord.ui.button(label="⬅️ Voltar", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Próximo ➡️", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        else:
            await interaction.response.defer()

def setup_queue_command(bot):
    @bot.command(name="queue", aliases=["q", "fila"])
    async def queue(ctx):
        responses = await languageservice(bot, ctx, "songs", "queue.json")
        state = song_queues.get(ctx.guild.id)
        
        if not state or not state['queue']:
            # Se tiver algo tocando mas a fila estiver vazia
            if state and state['current']:
                return await ctx.send(responses['empty_queue'])
            return await ctx.send(responses['empty_wallet'])

        queue_list = state['queue']
        
        # Divide a lista em páginas de 5
        pages = [queue_list[i:i + 5] for i in range(0, len(queue_list), 5)]
        
        # Se tiver tocando algo, avisa no topo
        current_msg = responses['now_playing'].format(title=state['current']['title']) if state['current'] else ""
        
        view = QueueView(ctx.guild.id, pages, responses)
        embed = view.create_embed()
        embed.description = current_msg + embed.description

        # Só mostra botões se houver mais de uma página
        if len(pages) <= 1:
            # Remove botões se só houver uma página
            view.clear_items()
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, view=view)