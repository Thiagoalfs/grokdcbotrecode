import discord
from discord.ext import commands
from messageTriggers import message_triggers
from dotenv import load_dotenv
from commands.commandshandler import setup_commands

load_dotenv()
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

setup_commands(bot)
message_triggers(bot)

bot.run(os.getenv("TOKEN"))