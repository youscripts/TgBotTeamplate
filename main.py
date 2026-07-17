import os
import discord
from discord.ext import commands

# Настраиваем доступы (Intents)
intents = discord.Intents.default()
intents.message_content = True  # Разрешаем чтение содержимого сообщений

# Создаем бота. Префикс команд будет "!"
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"=======================================")
    print(f"Бот {bot.user.name} успешно запущен!")
    print(f"Готов к работе на всех серверах.")
    print(f"=======================================")

@bot.command()
async def hello(ctx):
    """Команда приветствия"""
    await ctx.send(f"Привет, {ctx.author.mention}! Я твой новый Дискорд-бот, созданный на заказ. 🚀")

@bot.command()
async def ping(ctx):
    """Проверка пинга (задержки) бота"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Понг! Задержка сервера: {latency}мс")

@bot.command()
async def info(ctx):
    """Информация о боте для покупателя"""
    embed = discord.Embed(
        title="ℹ️ Информация о боте", 
        description="Этот бот полностью готов к работе и настроен для хостинга.", 
        color=0x00ff00
    )
    embed.add_field(name="Разработчик", value="Выполнено на заказ", inline=True)
    embed.add_field(name="Статус", value="Стабилен 24/7", inline=True)
    await ctx.send(embed=embed)

# Получаем токен из переменных окружения (для безопасности)
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("Ошибка: Переменная DISCORD_TOKEN не найдена! Проверьте настройки.")
