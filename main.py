import discord
from discord.ext import commands
from discord import app_commands
from pathlib import Path
import logging 
import os
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)

intents = discord.Intents().default()
bot = commands.Bot(command_prefix = ".", case_insensitive=True, owner_id=583200866631155714, intents=intents)
bot.remove_command("help")

logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    await bot.load_extension("cogs.commands")
    await bot.tree.sync()
    print("Bot Ready!")

@bot.tree.command(name="reload", description="[OWNER COMMAND] Reloads all Dendy Commands")
async def reload(interaction : discord.Interaction):
    if interaction.user.id != 583200866631155714:
        return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

    await bot.unload_extension("cogs.commands")
    await bot.load_extension("cogs.commands")
    await bot.tree.sync()
    await interaction.response.send_message("Successfully reloaded commands!")

@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await interaction.response.send_message(f"`/{interaction.command.name}` is on cooldown. Please try again in **{int(s)}** seconds.", ephemeral=True)
        elif int(h) == 0 and int(m) != 0:
            await interaction.response.send_message(f"`/{interaction.command.name}` is on cooldown. Please try again in **{int(m)}** minutes and **{int(s)}** seconds.", ephemeral=True)
        else:
            await interaction.response.send_message(f"`/{interaction.command.name}` is on cooldown. Please try again in **{int(h)}** hours, **{int(m)}** minutes and **{int(s)}** seconds.", ephemeral=True)

    if isinstance(error, discord.InteractionResponded):
        return

bot.run(os.environ['token'])