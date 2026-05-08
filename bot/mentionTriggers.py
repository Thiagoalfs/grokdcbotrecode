import re, discord
from generalFunctions import respostas, ytdlp

try:
    from hiddentriggers.hiddenMentionTriggers import hidden_mention_triggers
except (ImportError, ModuleNotFoundError):
    hidden_mention_triggers = None

async def mention_triggers(bot, message):
    if bot.user in message.mentions:

        if hidden_mention_triggers and await hidden_mention_triggers(bot, message):
            return True
    
        elif message.content in (f"<@{bot.user.id}>", f"<@!{bot.user.id}>"):
            await message.channel.send("oi fi po fala")
            return True
        
        elif re.search(r'(?<!\w)(salve)(?!\w)', message.content.lower()):
            message.mentions.remove(bot.user)
            if len(message.mentions) == 0:
                await message.channel.send("um salve ai meu mano " + message.author.mention)
            elif len(message.mentions) > 1:
                await message.channel.send("marca só um ai pit. o salve é só pra um de cada vez", reference=message)
            else:
                await message.channel.send("um salve ai pro meu mano " + message.mentions[0].mention)
            return True

        else:
            await message.channel.send(respostas(), reference=message)
            return True

    return False