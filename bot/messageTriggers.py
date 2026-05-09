import re, random, os
from mentionTriggers import mention_triggers

try:
    from hiddentriggers.hiddenMessageTriggers import hidden_message_triggers
except (ImportError, ModuleNotFoundError):
    hidden_message_triggers = None

def message_triggers(bot):
    @bot.event
    async def on_ready():
        print(f"Loguei como {bot.user}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return True
        
        await bot.process_commands(message)
            
        await mention_triggers(bot, message)

        if bot.user not in message.mentions:

            if hidden_message_triggers and await hidden_message_triggers(bot, message):
                return True
            
            if re.search(r'(?<!\w)(:3)(?!\w)', message.content.lower()):
                await message.channel.send("https://cdn.discordapp.com/attachments/435174265516458024/1357417638338236567/pellegrini7_-_1906183618713493636.gif?ex=69b1b0b0&is=69b05f30&hm=0daf26fd8cbbf09308a9dab5bf0f3350b67fe5b2e7b808c26ffb0aa42610194a&", reference=message)
                        
            elif re.search(r'(?<!\w)(ué|ue)(?!\w)', message.content.lower()):
                await message.channel.send("ué o que?", reference=message)
                return True
                       
            elif re.search(r'(?<!\w)(ijo)(?!\w)', message.content.lower()):
                await message.channel.send("tu se acha o engraçadao ne pnc", reference=message)
                return True
                        