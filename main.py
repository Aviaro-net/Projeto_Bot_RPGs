import discord
import random
import re
import os

from dotenv import load_dotenv

from discord.ext import commands
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix= "-", intents=permissoes)

@bot.event
async def on_ready():
    print(f"Estou on BB!!! Bora botar pra quebrar {bot.user}")

@bot.command()
async def ola(ctx:commands.Context):
    canal = ctx.channel
    await ctx.send(f"Eai, tudo bem?\n{canal.name}")

@bot.command()
async def soma(ctx:commands.Context, num1:int, num2:int):
    sum = num1 + num2
    await ctx.reply(sum)

@bot.event
async def on_message(message):
    # Não responder às mensagens de outros bots
    if message.author.bot:
        return

    # Ler a expressão enviada pelo usuário
    expressao = message.content.strip().lower()

    # Reconhecer expressões como 1d20, 3d6 ou 2d17
    resultado = re.fullmatch(r"(\d*)d(\d+)", expressao)

    if not resultado:
        return

    quantidade_texto, lados_texto = resultado.groups()

    # Se o usuário digitar apenas d20, considerar 1d20
    quantidade = int(quantidade_texto) if quantidade_texto else 1
    lados = int(lados_texto)

    # Impedir entradas inválidas ou excessivas
    if quantidade < 1 or quantidade > 100:
        await message.channel.send(
            "A quantidade de dados deve estar entre 1 e 100."
        )
        return

    if lados < 2 or lados > 100000:
        await message.channel.send(
            "O dado deve ter entre 2 e 100000 lados."
        )
        return

    # Rolar os dados
    resultados = [
        random.randint(1, lados)
        for _ in range(quantidade)
    ]

    total = sum(resultados)

    # Montar a resposta
    valores = " + ".join(map(str, resultados))

    resposta = (
        f"🎲 **Rolagem: {quantidade}d{lados}**\n"
        f"Resultados: {valores}\n"
        f"**Total: {total}**"
    )

    await message.channel.send(resposta)

load_dotenv()

token = os.getenv("DISCORD_TOLKIEN")

bot.run(token)
