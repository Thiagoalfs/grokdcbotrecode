import re, io, discord
from generalFunctions import respostas, ytdlp
async def mention_triggers(bot, message):
    if bot.user in message.mentions:
        if message.content == "<@1312115157589037066>":
            await message.channel.send("oi fi po fala")
            return
        
        elif re.search(r'(?<!\w)(salve)(?!\w)', message.content.lower()):
            message.mentions.remove(bot.user)
            if len(message.mentions) == 0:
                await message.channel.send("um salve ai meu mano " + message.author.mention)
            elif len(message.mentions) > 1:
                await message.channel.send("marca só um ai pit. o salve é só pra um de cada vez", reference=message)
            else:
                await message.channel.send("um salve ai pro meu mano " + message.mentions[0].mention)
            return
        
        elif re.search(r'(?<!\w)(smt|se mata)(?!\w)', message.content.lower()):
            await message.channel.send("se mata tu ze oxi", reference=message)
            return

        else:
            await message.channel.send(respostas(), reference=message)
        