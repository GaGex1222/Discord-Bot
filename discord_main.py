import asyncio
import discord
import requests
from hello_ways import hello_ways
import random
from discord.ext import commands
import time
from commands import commands_text
from dotenv import load_dotenv
import os
load_dotenv()



TOKEN = os.getenv('TOKEN_DISCORD')
print(TOKEN)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
bot_commands = commands.Bot(command_prefix="?", intents=intents)

@bot_commands.event
async def on_ready():
    channel = bot_commands.get_channel(1215685731301986364)
    await channel.send("Bot is ready!")
    print('Bot Is Ready For Use!')

@bot_commands.event
async def on_member_join(member):
    channel = bot_commands.get_channel(1207642900314460160)
    time.sleep(1)
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response_url = requests.get(url=joke_url)
    result = response_url.json()
    try:
        joke_setup = result["setup"]
        joke_delivery = result["delivery"]
        joke_formatted = f"{joke_setup} {joke_delivery}"
        time.sleep(1)
    except KeyError:
        joke_formatted = result["joke"]
        time.sleep(1)
    await channel.send(f"{member.mention} here is a joke for you to cheer up!\n{joke_formatted}")


@bot_commands.command()
async def test(ctx, *args):
    argss = ",".join(args)
    await ctx.send(f'Number of args : {len(args)} and they are : {argss}')


@bot_commands.command()
async def joke(ctx):
    await ctx.send("Looking for a joke...")
    time.sleep(1)
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response_url = requests.get(url=joke_url)
    result = response_url.json()
    try:
        joke_setup = result["setup"]
        joke_delivery = result["delivery"]
        joke_formatted = f"{joke_setup} {joke_delivery}"
        await ctx.send("Found!")
        time.sleep(1)
    except KeyError:
        joke_formatted = result["joke"]
        await ctx.send("Found!")
        time.sleep(1)
    await ctx.send(joke_formatted)


@bot_commands.command()
async def commands(ctx):
    await ctx.send(commands_text)


@bot_commands.command()
async def users(ctx):
    await ctx.send(f"The server have {ctx.guild.member_count} users")


@bot_commands.command()
async def hello(ctx):
    await ctx.send(f"{ctx.author} {random.choice(hello_ways)}")


@bot_commands.command()
async def roll(ctx):
    await ctx.send(f"{ctx.author} You got the number {random.randint(1, 6)}")



@bot_commands.command()
async def textchannels(ctx):
    guild = bot_commands.get_guild(1007094713347743775)
    if guild:
        voice_channels = guild.text_channels
        if voice_channels:
            voice_channels_names = []
            for voice_channel in voice_channels:
                voice_channels_names.append(voice_channel.name)
            voice_channels_names_organized = "\n".join(voice_channels_names)
            await ctx.send(
                f"There are {len(voice_channels_names)} Text channels and they are :\n{voice_channels_names_organized}")
        else:
            await ctx.send("There are no voice channels!")
    else:
        await ctx.send("Guild not found (Server)")


@bot_commands.command()
async def joinvc(ctx):
    user = ctx.author
    if user.voice:
        channel = user.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel")


@bot_commands.command()
async def mention(ctx):
    user = ctx.author
    await ctx.send(f"Hey {str(user).capitalize()} I Will mention you in 3 Seconds...")
    time.sleep(3)
    await ctx.send(str(user.mention).capitalize())


@bot_commands.command()
async def mentionroles(ctx, *args):
    for roles in args:
        role = discord.utils.get(ctx.guild.roles, name=roles)
        if role:
            await ctx.send(role.mention)
        else:
            await ctx.send(f"Role '{role}' not found.")



rooms = {}


@bot_commands.command()
async def play(ctx, channel_name):
    random_channel_num = ""
    game_channel = discord.utils.get(ctx.guild.channels, name="game-channel")

    for _ in range(5):
        random_channel_num += str(random.randint(1, 6))
    category_name = "GAME CHANNELS"
    guild = ctx.guild
    channel_name_low = str(channel_name).lower()
    final_text_name = f"{channel_name_low + random_channel_num}"
    channel = discord.utils.get(guild.channels, name=final_text_name)
    category = discord.utils.get(guild.categories, name=category_name)
    user = str(ctx.author)
    if ctx.channel == game_channel:
        if not category:
            category = await guild.create_category(category_name)


        if not channel:
            role = discord.utils.get(ctx.guild.roles, name=channel_name_low)
            rooms[random_channel_num] = {
                "user": [user],
                "channel_final_name": final_text_name
            }
            await guild.create_text_channel(final_text_name, category=category)
            try:
                await ctx.send(role.mention)
            except:
                await ctx.send(f"There is no role named {channel_name_low} to mention")
            finally:
                await ctx.send(
                    f"Channel for the game {channel_name_low} has been created\nowner : {ctx.author.mention}\nchannel id: {random_channel_num}\nthere are currently {len(rooms[random_channel_num]['user'])}/5 players.\nPlayers: {". ".join(rooms[random_channel_num]['user'])}.\nwaiting for {5 - len(rooms[random_channel_num]['user'])} more people...")

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

                while random_channel_num in rooms:
                    await asyncio.sleep(1800)
                    current_game_channel = discord.utils.get(guild.text_channels, name=final_text_name)
                    await current_game_channel.send(f"{ctx.author.mention}30 minutes have passed since you opened the room, do you still play? (you have 1 minute to answer)")
                    channel = discord.utils.get(guild.channels, name=final_text_name)
                    try:
                        msg = await bot_commands.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        delete_channels_channel = bot_commands.get_channel(1215976026627248158)
                        await delete_channels_channel.send(f"{ctx.author.mention} 1 minutes have passed, and you havent answered, we are deleting your game channel {final_text_name}!.")
                        rooms.pop(random_channel_num)
                        await channel.delete()
                    else:
                        if msg.content.lower() == "y":
                            await ctx.send("alright, i will not remove your channel!")
                        else:
                            delete_channels_channel = bot_commands.get_channel(1215976026627248158)
                            await delete_channels_channel.send(f"Alright, deleting {final_text_name}!")
                            await channel.delete()

        else:
            await ctx.send(f"Channel {final_text_name} already exists")
    else:
        await ctx.send("You are in the wrong channel, for this command go to 'game-channel'")

@bot_commands.command()
async def join(ctx, channel_id):
    user = str(ctx.author)

    if len(rooms[channel_id]['user']) == 5:
        await ctx.send("The room is full, please try another one!")
    else:
        if user in rooms[channel_id]["user"]:
            await ctx.send(f"{user} is already in the game channel")
        else:
            rooms[channel_id]['user'].append(user)
            players = ", ".join(rooms[channel_id]['user'])
            remaining_players = 5 - len(rooms[channel_id]['user'])
            await ctx.send(
                f"{user} have been added to {channel_id}\n"
                f"there are currently {len(rooms[channel_id]['user'])}/5 players.\n"
                f"Players: {players}.\n"
                f"waiting for {remaining_players} more people..."
            )


@bot_commands.command()
async def categorydelete(ctx, category_id):
    guild = ctx.guild
    category_name = "GAME CHANNELS"
    category = guild.get_channel(int(category_id))
    if not category:
        await ctx.send(f"{category_id} does not exist")

    for channel in category.channels:
        await channel.delete()

@bot_commands.command()
async def finishedplaying(ctx, channel_id):
    user = ctx.author
    if channel_id in rooms:
        await ctx.send(f"{channel_id} exist!!")
        if str(user) == rooms[channel_id]["user"][0]:
            guild = ctx.guild
            channel = discord.utils.get(guild.text_channels, name=rooms[channel_id]["channel_final_name"])
            await channel.delete()
            await ctx.send(f"Room {rooms[channel_id]["channel_final_name"]} has been removed, hope you had fun!")




bot_commands.run(TOKEN)
