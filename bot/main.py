import discord
from discord.ext import commands
from messageTriggers import message_triggers
from dotenv import load_dotenv
from commands.commandshandler import setup_commands
import os
import shutil
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"Loguei como {bot.user}")
    # Limpa a pasta 'songs' ao iniciar o bot
    songs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "songs")
    try:
        if os.path.exists(songs_folder):
            shutil.rmtree(songs_folder)
        os.makedirs(songs_folder)
        print(f"Pasta '{songs_folder}' reiniciada com sucesso ao iniciar.")
    except Exception as e:
        print(f"Erro ao limpar a pasta '{songs_folder}' no on_ready: {e}")

setup_commands(bot)
message_triggers(bot)

bot.run(os.getenv("TOKEN"))