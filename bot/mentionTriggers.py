import re, io, discord
from aiRequests import perguntar_groq
from generalFunctions import respostas
async def mention_triggers(bot, message):
    if bot.user in message.mentions:
        if message.content == "<@1312115157589037066>":
            await message.channel.send("oi fi po fala")
            return
        
        elif message.reference:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            
            if referenced_message.author == bot.user and "<@1312115157589037066>" not in message.content:
                return
            
            anexo_url = None
            attachments_para_checar = referenced_message.attachments or message.attachments
            for attachment in attachments_para_checar:
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    anexo_url = attachment.url
                    break
            
            if anexo_url:
                resposta = await perguntar_groq(anexo_url, "imagem")
            else:
                resposta = await perguntar_groq(referenced_message.content, "texto")
            
            if not resposta:
                await message.channel.send("não consigo te ajudar com isso")
                return
            if len(resposta) > 1900:
                arquivo = io.BytesIO(resposta.encode('utf-8'))
                await message.channel.send(file=discord.File(arquivo, filename="resposta.txt"))
            else:
                await message.channel.send(resposta)
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
        