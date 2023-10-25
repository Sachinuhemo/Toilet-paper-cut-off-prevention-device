import discord
from discord.ext import commands
import RPi.GPIO as GPIO
import asyncio
import time

GPIO_PAPER = 2
GPIO_LED = 17
GPIO_BUZZER = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PAPER, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_BUZZER, GPIO.OUT)
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

notice = None

# 起動
@client.event
async def on_ready():
    global notice
    notice = client.get_channel(1124950061038706770)
    print("起動完了")
    GPIO.output(GPIO_BUZZER, True)
    time.sleep(0.01)
    GPIO.output(GPIO_BUZZER, False)
    await main()

async def main():
    while True:
        await asyncio.sleep(0.1)
        if GPIO.input(GPIO_PAPER) == GPIO.LOW:
            await notice.send("```diff\n- トイレットペーパーがなくなりそうです。ストックがあるか確認してください。-\n```")
            GPIO.output(GPIO_LED, True)
            await client.change_presence(status=discord.Status.dnd)
            for _ in range(3):
                GPIO.output(GPIO_BUZZER, True)
                time.sleep(0.1)
                GPIO.output(GPIO_BUZZER, False)
                time.sleep(0.1)
            time.sleep(1)
            break

@client.command()
async def con():
    await client.change_presence(status=discord.Status.online)
    GPIO.output(GPIO_LED, False)
    await notice.send("OK")
    await main()

client.run("TOKEN") 
