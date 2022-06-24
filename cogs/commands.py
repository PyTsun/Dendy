from discord.ui import Button, View, Modal, TextInput
from discord import app_commands, Interaction
from discord.app_commands import Choice
from discord.ext import commands
from typing import Optional
import discord
import discord
import asyncio
import random
import json
import math

class mView(discord.ui.View):
    def __init__(self, user: discord.User, timeout: int = None):
        super().__init__(timeout=timeout)
        self.user = user

    async def interaction_check(self, interaction: Interaction):
        if interaction.user and interaction.user.id == self.user.id:
            return interaction.user and interaction.user.id == self.user.id
        else:
            await interaction.response.defer()
    
    async def on_timeout(self) -> None:
        return await super().on_timeout()

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.req = 750000
        self.exc = False

        # Image Links
        self.crashing_icon  = "https://cdn.discordapp.com/attachments/966939831294889994/976685662155726878/unknown.png"
        self.multwheel_icon = "https://cdn.discordapp.com/attachments/966939831294889994/976685661908271114/unknown.png"
        self.tokenshop_icon = "https://cdn.discordapp.com/attachments/966939831294889994/976685662352834590/unknown.png"
        self.wallet_icon    = "https://cdn.discordapp.com/attachments/966939831294889994/976709603612033084/unknown.png"

    # Registration Command
    @app_commands.command(name="register", description="Registers you from Dendy to access All Dendy Commands and More!")
    async def register(self, interaction: Interaction):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)

        user = str(interaction.user.id)
        p = self.points

        if user in self.points:
            return await interaction.response.send_message("You are already registered!", ephemeral=True)

        class registration_form(Modal, title="Dendy Account Registration"):
            password = TextInput(label=f"Dendy Password", style=discord.TextStyle.short, required = True, max_length=32, min_length=6)

            async def on_submit(self, interaction: discord.Interaction):
                p[user] = {}
                p[user]["points"] = 0
                p[user]["pending_points"] = 0
                p[user]["tokens"] = 0
                p[user]["crashMult"] = 0
                p[user]["crashing"] = False
                p[user]["mining"] = False
                p[user]["onqueue"] = False
                p[user]["password"] = str(self.password)

                with open(r"points.json", "w") as f: 
                    json.dump(p, f, indent=4)
                
                await interaction.response.send_message("Registration Success!", ephemeral=True)

        await interaction.response.send_modal(registration_form())
    
    # User Config Commands
    @app_commands.command(name="exchange", description="Creates a exchange request to convert your tokens to robux.")
    async def exchange(self, interaction: Interaction, amount: app_commands.Range[int, 2, 50], gamepasslink: str):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if self.exc == False:
            return await interaction.response.send_message("Exchanging tokens is currently not being accepted yet. Please try again soon!")

        if gamepasslink.startswith("https://roblox.com/game-pass"):
            print("Normal Roblox Link")
        elif gamepasslink.startswith("https://www.roblox.com/game-pass"):
            print("Normal Roblox Link")
        elif gamepasslink.startswith("https://web.roblox.com/game-pass"):
            print("Underage Roblox Link")
        else:
            return await interaction.response.send_message("Invalid Roblox Link! make sure the link starts with `https://` to recognise the link!", ephemeral=True)

        if self.points[str(interaction.user.id)]["tokens"] >= amount + 1:
            return await interaction.response.send_message("You can't exchange tokens higher than you currently have!", ephemeral=True)

        queue = self.bot.get_channel(984357716954845204)

        self.points[str(interaction.user.id)]["tokens"] -= amount
        self.points[str(interaction.user.id)]["onqueue"] = True

        embed=discord.Embed(title="🚧 Pending Token Exchange", color=0xffe100)
        embed.add_field(name=f"Link: {gamepasslink}", value=f"Requested by: {interaction.user.mention} ({interaction.user})\nAmount: **{amount}**", inline=False)
        await queue.send(embed=embed)
        await interaction.response.send_message("Token Exchange Done! Please wait for me to buy it, it may take longer until i get robux.", ephemeral=True)

    # Commands
    @app_commands.command(name="wallet", description="Shows how many points and tokens you have.")
    @app_commands.describe(member="Shows the mentioned member's points ant tokens")
    async def wallet(self, interaction : Interaction, member : Optional[discord.Member] = None):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)

        if member == None:
            points = self.points[str(interaction.user.id)]["points"]
            tokens = self.points[str(interaction.user.id)]["tokens"]
            ppoints = self.points[str(interaction.user.id)]["pending_points"]
            embed=discord.Embed(title=f"{interaction.user.name}'s Wallet")
            embed.set_thumbnail(url=self.wallet_icon)
            embed.add_field(name="Dendy Points", value=f"**{points:,}**", inline=True)
            embed.add_field(name="Dendy Tokens", value=f"**{tokens}**", inline=True)
            embed.add_field(name="Pending Points", value=f"**{ppoints:,}**", inline=False)
            await interaction.response.send_message(embed=embed)
        
        else:
            points = self.points[str(member.id)]["points"]
            tokens = self.points[str(member.id)]["tokens"]
            ppoints = self.points[str(member.id)]["pending_points"]
            embed=discord.Embed(title=f"{member.name}'s Wallet")
            embed.set_thumbnail(url=self.wallet_icon)
            embed.add_field(name="Dendy Points", value=f"**{points:,}**", inline=True)
            embed.add_field(name="Dendy Tokens", value=f"**{tokens}**", inline=True)
            embed.add_field(name="Pending Points", value=f"**{ppoints:,}**", inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tokenshop", description="Opens the Token Shop Panel where you can exchange your points to tokens.")
    async def tokenshop(self, interaction: Interaction):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)

        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)

        if self.points[str(interaction.user.id)]["onqueue"] == True:
            return await interaction.response.send_message("Sorry! you are unable to exchange tokens since you recently placed yourself on queue!", ephemeral=True)
            
        view = mView(interaction.user, timeout=30)

        convert1 = Button(label="+1 Token", style=discord.ButtonStyle.green)
        convert5 = Button(label="+5 Tokens", style=discord.ButtonStyle.green)
        convert10 = Button(label="+10 Tokens", style=discord.ButtonStyle.green)
        convert25 = Button(label="+25 Tokens", style=discord.ButtonStyle.green)

        tk = self.points[str(interaction.user.id)]["tokens"]
        embed=discord.Embed(title="Dendy Token Shop", description="Welcome to the **Dendy Token Shop!**\nExchange your **Dendy Points** to **Dendy Tokens** here!")
        embed.set_thumbnail(url=self.tokenshop_icon)
        embed.add_field(name="Current Price", value=f"**{self.req:,} Points**", inline=True) 
        embed.add_field(name="Your Tokens", value=f"**{tk:,}**", inline=True)

        async def convert_1(interaction):
            if self.points[str(interaction.user.id)]["points"] <= self.req:
                return await interaction.response.send_message(content=f"You don't have enough points to convert it into tickets!", ephemeral=True)

            self.points[str(interaction.user.id)]["points"] -= self.req
            self.points[str(interaction.user.id)]["tokens"] += 1

            newtk = self.points[str(interaction.user.id)]["tokens"]
            embed=discord.Embed(title="Dendy Token Shop", description="Welcome to the **Dendy Token Shop!**\nExchange your **Dendy Points** to **Dendy Tokens** here!")
            embed.set_thumbnail(url=self.tokenshop_icon)
            embed.add_field(name="Current Price", value=f"**{self.req:,} Points**", inline=True) 
            embed.add_field(name="Your Tokens", value=f"**{newtk:,}**", inline=True)
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
            await interaction.response.edit_message(embed=embed, view=view)
        
        async def convert_5(interaction):
            if self.points[str(interaction.user.id)]["points"] <= 5 * self.req:
                return await interaction.response.send_message(content=f"You don't have enough points to convert it into tickets!", ephemeral=True)

            self.points[str(interaction.user.id)]["points"] -= 5 * self.req
            self.points[str(interaction.user.id)]["tokens"] += 5

            newtk = self.points[str(interaction.user.id)]["tokens"]
            embed=discord.Embed(title="Dendy Token Shop", description="Welcome to the **Dendy Token Shop!**\nExchange your **Dendy Points** to **Dendy Tokens** here!")
            embed.set_thumbnail(url=self.tokenshop_icon)
            embed.add_field(name="Current Price", value=f"**{self.req:,} Points**", inline=True) 
            embed.add_field(name="Your Tokens", value=f"**{newtk:,}**", inline=True)
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
            await interaction.response.edit_message(embed=embed, view=view)
        
        async def convert_10(interaction):
            if self.points[str(interaction.user.id)]["points"] <= 10 * self.req:
                return await interaction.response.send_message(content=f"You don't have enough points to convert it into tickets!", ephemeral=True)

            self.points[str(interaction.user.id)]["points"] -= 10 * self.req
            self.points[str(interaction.user.id)]["tokens"] += 10

            newtk = self.points[str(interaction.user.id)]["tokens"]
            embed=discord.Embed(title="Dendy Token Shop", description="Welcome to the **Dendy Token Shop!**\nExchange your **Dendy Points** to **Dendy Tokens** here!")
            embed.set_thumbnail(url=self.tokenshop_icon)
            embed.add_field(name="Current Price", value=f"**{self.req:,} Points**", inline=True) 
            embed.add_field(name="Your Tokens", value=f"**{newtk:,}**", inline=True)
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
            await interaction.response.edit_message(embed=embed, view=view)
        
        async def convert_25(interaction):
            if self.points[str(interaction.user.id)]["points"] <= 25 * self.req:
                return await interaction.response.send_message(content=f"You don't have enough points to convert it into tickets!", ephemeral=True)

            self.points[str(interaction.user.id)]["points"] -= 25 * self.req
            self.points[str(interaction.user.id)]["tokens"] += 25

            newtk = self.points[str(interaction.user.id)]["tokens"]
            embed=discord.Embed(title="Dendy Token Shop", description="Welcome to the **Dendy Token Shop!**\nExchange your **Dendy Points** to **Dendy Tokens** here!")
            embed.set_thumbnail(url=self.tokenshop_icon)
            embed.add_field(name="Current Price", value=f"**{self.req:,} Points**", inline=True) 
            embed.add_field(name="Your Tokens", value=f"**{newtk:,}**", inline=True)
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
            await interaction.response.edit_message(embed=embed, view=view)
        
        async def exitshop():
            newtk = self.points[str(interaction.user.id)]["tokens"]
            embed=discord.Embed(title="Dendy Token Shop", description="Welcome to the **Dendy Token Shop!**\nExchange your **Dendy Points** to **Dendy Tokens** here!")
            embed.set_thumbnail(url=self.tokenshop_icon)
            embed.add_field(name="Current Price", value=f"**{self.req:,} Points**", inline=True) 
            embed.add_field(name="Your Tokens", value=f"**{newtk:,}**", inline=True)
            await interaction.edit_original_message(embed=embed, view=None)

        view.on_timeout = exitshop
        convert1.callback = convert_1
        convert5.callback = convert_5
        convert10.callback = convert_10
        convert25.callback = convert_25

        view.add_item(convert1)
        view.add_item(convert5)
        view.add_item(convert10)
        view.add_item(convert25)
        await interaction.response.send_message(embed=embed, view=view)

    # Farming Commands
    @app_commands.command(name="mine", description="Mine for points!")
    @app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
    async def mine(self, interaction : Interaction):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)

        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)

        m = random.randint(2500, 7500)
        self.points[str(interaction.user.id)]["points"] += m
        await interaction.response.send_message(f"You mined **{m:,}** points!")
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)
    
    @app_commands.command(name="deliver", description="Deliver packages for points!")
    @app_commands.checks.cooldown(1, 60, key=lambda i: i.user.id)
    async def deliver(self, interaction : Interaction):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)

        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)

        m = random.randint(7500, 10000)
        self.points[str(interaction.user.id)]["points"] += m
        await interaction.response.send_message(f"You delivered packages and got **{m:,}** points!")
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)
    
    # Gambling Commands
    @app_commands.command(name="crash", description="Crash your points for points!")
    @app_commands.describe(bet="Amount of points you want to bet for Crashing")
    async def crash(self, interaction : Interaction, bet : app_commands.Range[int, 50000, 750000]):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)
            
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
            
        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)

        view = mView(interaction.user)

        crash1  = Button(label="Crash (0.05x)", style=discord.ButtonStyle.green)
        crash2  = Button(label="Crash (0.50x)", style=discord.ButtonStyle.red)
        cashout = Button(label="Cashout", style=discord.ButtonStyle.grey)
        
        if bet >= self.points[str(interaction.user.id)]["points"] + 1:
            return await interaction.response.send_message("You cant bet higher than you currently have!", ephemeral=True)

        if self.points[str(interaction.user.id)]["crashing"] != False:
            return await interaction.response.send_message("You currently have an ongoing crash session. Please finish that one first!", ephemeral=True)

        self.points[str(interaction.user.id)]["crashing"] = True
        self.points[str(interaction.user.id)]["crashMult"] = 1
        self.points[str(interaction.user.id)]["points"] -= bet

        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)

        async def addmulti1(interaction):
            crash = random.randint(1, 20)

            if crash != 13:
                self.points[str(interaction.user.id)]["crashMult"] += 0.05
                mult = self.points[str(interaction.user.id)]["crashMult"]
                embed=discord.Embed(title=f"{interaction.user.name}'s Dendy Crash")
                embed.set_thumbnail(url=self.crashing_icon)
                embed.add_field(name="Points", value=f"**{round(bet * mult):,}**", inline=False)
                embed.add_field(name="Multiplier", value=f"**{math.floor(mult * 100)/100.0}x**", inline=False)
                await interaction.response.edit_message(embed=embed)
            else:
                self.points[str(interaction.user.id)]["crashMult"] += 0.05
                self.points[str(interaction.user.id)]["crashing"] = False
                mult = self.points[str(interaction.user.id)]["crashMult"]
                embed=discord.Embed(title=f"{interaction.user.name}'s Dendy Crash - Crashed")
                embed.set_thumbnail(url=self.crashing_icon)
                embed.add_field(name="Points", value=f"**{round(bet * mult):,}**", inline=False)
                embed.add_field(name="Multiplier", value=f"**{math.floor(mult * 100)/100.0}x**", inline=False)
                with open(r"points.json", "w") as f: 
                    json.dump(self.points, f, indent=4)
                await interaction.response.edit_message(embed=embed, view=None)
        
        async def addmulti2(interaction):
            crash = random.randint(1, 3)

            if crash != 2:
                self.points[str(interaction.user.id)]["crashMult"] += 0.50
                mult = self.points[str(interaction.user.id)]["crashMult"]
                embed=discord.Embed(title=f"{interaction.user.name}'s Dendy Crash")
                embed.set_thumbnail(url=self.crashing_icon)
                embed.add_field(name="Points", value=f"**{round(bet * mult):,}**", inline=False)
                embed.add_field(name="Multiplier", value=f"**{math.floor(mult * 100)/100.0}x**", inline=False)
                await interaction.response.edit_message(embed=embed)
            else:
                self.points[str(interaction.user.id)]["crashMult"] += 0.50
                self.points[str(interaction.user.id)]["crashing"] = False
                mult = self.points[str(interaction.user.id)]["crashMult"]
                embed=discord.Embed(title=f"{interaction.user.name}'s Dendy Crash - Crashed")
                embed.set_thumbnail(url=self.crashing_icon)
                embed.add_field(name="Points", value=f"**{round(bet * mult):,}**", inline=False)
                embed.add_field(name="Multiplier", value=f"**{math.floor(mult * 100)/100.0}x**", inline=False)
                with open(r"points.json", "w") as f: 
                    json.dump(self.points, f, indent=4)
                await interaction.response.edit_message(embed=embed, view=None)
        
        async def cashout_points(interaction):
            mult = self.points[str(interaction.user.id)]["crashMult"]

            self.points[str(interaction.user.id)]["points"] += round(bet * mult)

            embed=discord.Embed(title=f"{interaction.user.name}'s Dendy Crash - Cashed Out")
            embed.set_thumbnail(url=self.crashing_icon)
            embed.add_field(name="Points", value=f"**{round(bet * mult):,}**", inline=False)
            embed.add_field(name="Multiplier", value=f"**{int( mult * 100 ) / 100}x**", inline=False)
            
            if mult == 1:
                return await interaction.response.send_message("You currently cannot **Cashout**. Please start crashing first!", ephemeral=True)
                
            self.points[str(interaction.user.id)]["crashing"] = False
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
            await interaction.response.edit_message(embed=embed, view=None)

        crash1.callback = addmulti1
        crash2.callback = addmulti2
        cashout.callback = cashout_points
        view.add_item(crash1)
        view.add_item(crash2)
        view.add_item(cashout)

        embed=discord.Embed(title=f"{interaction.user.name}'s Dendy Crash")
        embed.set_thumbnail(url=self.crashing_icon)
        embed.add_field(name="Points", value=f"**{bet:,}**", inline=False)
        embed.add_field(name="Multiplier", value="**1.0x**", inline=False)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="cups", description="Play a game of cups for points!")
    @app_commands.describe(bet="Amount of points you want to bet for Cups")
    async def cups(self, interaction : Interaction, bet : app_commands.Range[int, 10000, 500000]):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)
        
        if bet >= self.points[str(interaction.user.id)]["points"] + 1:
            return await interaction.response.send_message("You cant bet higher than you currently have!", ephemeral=True)

        c = ["Red", "Blue", "Green"]
        r = random.choice(c)

        view = mView(interaction.user)

        redbtn   = Button(label="Red Cup", style=discord.ButtonStyle.red)
        bluebtn  = Button(label="Blue Cup", style=discord.ButtonStyle.blurple)
        greenbtn = Button(label="Green Cup", style=discord.ButtonStyle.green)

        async def redcup(interaction):
            await asyncio.sleep(2)

            if r == "Red":
                self.points[str(interaction.user.id)]["points"] += bet
                await interaction.response.edit_message(content=f"You won! **{bet:,}** points was added from your wallet.", view=None)
            
            if r == "Blue":
                self.points[str(interaction.user.id)]["points"] -= bet
                await interaction.response.edit_message(content=f"You lost! **{bet:,}** points was removed from your wallet.", view=None)

            if r == "Green":
                self.points[str(interaction.user.id)]["points"] -= bet
                await interaction.response.edit_message(content=f"You lost! **{bet:,}** points was removed from your wallet.", view=None)
            
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
            
        async def bluecup(interaction):
            await asyncio.sleep(2)

            if r == "Red":
                self.points[str(interaction.user.id)]["points"] -= bet
                await interaction.response.edit_message(content=f"You lost! **{bet:,}** points was removed from your wallet.", view=None)
            
            if r == "Blue":
                self.points[str(interaction.user.id)]["points"] += bet
                await interaction.response.edit_message(content=f"You won! **{bet:,}** points was added from your wallet.", view=None)

            if r == "Green":
                self.points[str(interaction.user.id)]["points"] -= bet
                await interaction.response.edit_message(content=f"You lost! **{bet:,}** points was removed from your wallet.", view=None)

            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)

        async def greencup(interaction):
            await asyncio.sleep(2)

            if r == "Red":
                self.points[str(interaction.user.id)]["points"] -= bet
                await interaction.response.edit_message(content=f"You lost! **{bet:,}** points was removed from your wallet.", view=None)

            if r == "Blue":
                self.points[str(interaction.user.id)]["points"] -= bet
                await interaction.response.edit_message(content=f"You lost! **{bet:,}** points was removed from your wallet.", view=None)

            if r == "Green":
                self.points[str(interaction.user.id)]["points"] += bet
                await interaction.response.edit_message(content=f"You won! **{bet:,}** points was added from your wallet.", view=None)
        
            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)
        
        redbtn.callback = redcup
        bluebtn.callback = bluecup
        greenbtn.callback = greencup

        view.add_item(redbtn)
        view.add_item(bluebtn)
        view.add_item(greenbtn)
        await interaction.response.send_message("Pick the color of your cup!", view=view)

    @app_commands.command(name="wheel", description="Spin the Multiplier Wheel to gain or lose profit!")
    @app_commands.describe(bet="Amount of points you want to bet for Multiplier Wheel")
    async def wheel(self, interaction : Interaction, bet : app_commands.Range[int, 75000, 500000]):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)

        with open(r"points.json", "r") as f:
            self.points = json.load(f)

        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)
        
        if bet >= self.points[str(interaction.user.id)]["points"] + 1:
            return await interaction.response.send_message("You cant bet higher than you currently have!", ephemeral=True)

        view = mView(interaction.user)
        mult = [0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]

        spin = Button(label="Spin Multiplier Wheel", style=discord.ButtonStyle.green)

        async def spinwheel(interaction):
            embed=discord.Embed(title="Dendy Wheel Multiplier", description="Welcome to **Dendy Wheel Multiplier**! Spin the multiplier wheel to gain points or lose points.")
            embed.set_thumbnail(url=self.multwheel_icon)
            embed.add_field(name="Multiplier", value=f"**x{random.choice(mult)}**", inline=False)
            embed.add_field(name="Info", value="Multipliers above x1 is **GOOD** since you are able to get more points from it. however, Multipliers below x1 is **BAD** since it will remove a small/big amount of points you betted.", inline=True)
            await interaction.response.edit_message(embed=embed, view=None)

            await asyncio.sleep(0.2)

            for x in range(13):
                embed=discord.Embed(title="Dendy Wheel Multiplier", description="Welcome to **Dendy Wheel Multiplier**! Spin the multiplier wheel to gain points or lose points.")
                embed.set_thumbnail(url=self.multwheel_icon)
                embed.add_field(name="Multiplier", value=f"**x{random.choice(mult)}**", inline=False)
                embed.add_field(name="Info", value="Multipliers above x1 is **GOOD** since you are able to get more points from it. however, Multipliers below x1 is **BAD** since it will remove a small/big amount of points you betted.", inline=True)
                await interaction.edit_original_message(embed=embed)

                await asyncio.sleep(0.2)
            
            m = random.choice(mult)

            self.points[str(interaction.user.id)]["points"] += round(bet * m)
            embed=discord.Embed(title="Dendy Wheel Multiplier", description=f"You got a **x{m}** multiplier!\nPoints: **{round(bet * m):,}** (Original: **{bet:,}**)")
            embed.set_thumbnail(url=self.multwheel_icon)
            embed.add_field(name="Multiplier", value=f"**x{m}**", inline=False)
            embed.add_field(name="Info", value="Multipliers above x1 is **GOOD** since you are able to get more points from it. however, Multipliers below x1 is **BAD** since it will remove a small/big amount of points you betted.", inline=True)
            await interaction.edit_original_message(embed=embed)

            with open(r"points.json", "w") as f: 
                json.dump(self.points, f, indent=4)

        embed=discord.Embed(title="Dendy Wheel Multiplier", description="Welcome to **Dendy Wheel Multiplier**! Spin the multiplier wheel to gain points or lose points.")
        embed.set_thumbnail(url=self.multwheel_icon)
        embed.add_field(name="Multiplier", value="**x1**", inline=False)
        embed.add_field(name="Info", value="Multipliers above x1 is **GOOD** since you are able to get more points from it. however, Multipliers below x1 is **BAD** since it will remove a small/big amount of points you betted.", inline=True)
        
        spin.callback = spinwheel
        view.add_item(spin)
        self.points[str(interaction.user.id)]["points"] -= bet
        await interaction.response.send_message(embed=embed, view=view)
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)

    # Cool Kids Commands
    @app_commands.command(name="rain", description="Starts a points rain on the server!")
    @app_commands.describe(amount="Amount of points you want to give per member", max_members="Max amount of members you want to join your points rain")
    async def rain(self, interaction : Interaction, amount : app_commands.Range[int, 500000, 1000000000], max_members : Optional[app_commands.Range[int, 10, 100]] = 100000):
        try:
            str(interaction.guild.id)
        except:
            embed = discord.Embed(description="**You can't run this command on DMs!**")
            return await interaction.response.send_message(embed=embed)
            
        with open(r"points.json", "r") as f:
            self.points = json.load(f)

        if not str(interaction.user.id) in self.points:
            return await interaction.response.send_message("Looks like you are not registered yet. Please use the `/register` command!", ephemeral=True)

        host = interaction
        rain = self.bot.get_channel(984354963851452426)
        
        ids = []
        a = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        code = f"{random.choice(a)}{random.choice(a)}{random.choice(a)}{random.choice(a)}{random.choice(a)}{random.choice(a)}"
            
        if amount >= self.points[str(interaction.user.id)]["points"] + 1:
            await interaction.response.send_message(f"You can't make a **{amount:,}** rain since its higher than you currently have!", ephemeral=True)
            return

        view = View()

        class rain_verification(Modal, title="Rain Verification"):
            codeinput = TextInput(label=f'Verification Code', style=discord.TextStyle.short, required = True, max_length=6)

            async def on_submit(self, interaction: discord.Interaction):
                if str(code) == str(self.codeinput):
                    if max_members != 100000:
                        ids.append(str(interaction.user.id))
                        embed=discord.Embed(title=f"{host.user.name}'s Points Rain - **{amount:,}** Points - {len(ids)} / {max_members}", description=f"Click **Join points Rain** to join the points rain! this will last for 2 minutes.\nMake sure to thank {host.user.mention}!\n\nPoints per user: **{round(amount / len(ids)):,}**\nVerification Code: **{code}**")
                        embed.set_footer(text=f"{len(ids)} members joined the points rain! - Last Joiner: {interaction.user}")
                        await interaction.response.edit_message(embed=embed)
                    
                    else:
                        embed=discord.Embed(title=f"{host.user.name}'s Points Rain - **{amount:,}** Points", description=f"Click **Join points Rain** to join the points rain! this will last for 2 minutes.\nMake sure to thank {host.user.mention}!\n\nPoints per user: **{round(amount / len(ids)):,}**\nVerification Code: **{code}**")
                        embed.set_footer(text=f"{len(ids)} members joined the points rain! - Last Joiner: {interaction.user}")
                        await interaction.response.edit_message(embed=embed)

                if str(code) != str(self.codeinput):
                    await interaction.response.send_message("Incorrect Code!", ephemeral=True)
        
        async def joinrain(interaction):
            try:
                self.points[str(interaction.user.id)]["points"]
            except:
                return await interaction.response.send_message("Looks like your new and havent been registered from the bot. Please talk before you can attend this rain!", ephemeral=True)
                
            if interaction.user.id == host.user.id:
                return await interaction.response.send_message("You can't join your own rain!", ephemeral=True)

            if len(ids) >= max_members + 1:
                return await interaction.response.send_message("This rain has reached max members!", ephemeral=True)
            
            if str(interaction.user.id) in ids:
                return await interaction.response.send_message("You already joined this rain!", ephemeral=True)
            
            await interaction.response.send_modal(rain_verification())

        self.points[str(interaction.user.id)]["points"] -= amount
        with open(r"points.json", "w") as f:
            json.dump(self.points, f, indent=4)
            
        join = Button(label="Join Points Rain", style=discord.ButtonStyle.green)
        join.callback = joinrain
        view.add_item(join)

        if max_members != 100000:
            embed=discord.Embed(title=f"{host.user.name}'s Points Rain - **{amount:,}** Points - {len(ids)} / {max_members}", description=f"Click **Join points Rain** to join the points rain! this will last for 2 minutes.\nMake sure to thank {host.user.mention}!\n\nPoints per user: **{amount:,}**\nVerification Code: **{code}**")
            embed.set_footer(text=f"{len(ids)} members joined the points rain! - Last Joiner: Anon#0000")
            m = await rain.send(content="<@&984363836754780250>", embed=embed, view=view)
        else:
            embed=discord.Embed(title=f"{host.user.name}'s Points Rain - **{amount:,}** Points", description=f"Click **Join points Rain** to join the points rain! this will last for 2 minutes.\nMake sure to thank {host.user.mention}!\n\nPoints per user: **{amount:,}**\nVerification Code: **{code}**")
            embed.set_footer(text=f"{len(ids)} members joined the points rain! - Last Joiner: Anon#0000")
            m = await rain.send(content="<@&984363836754780250>", embed=embed, view=view)

        await interaction.response.send_message("Successfully started Points Rain!", ephemeral=True)
        await asyncio.sleep(120)

        try:
            prize = round(amount / len(ids))
        except:
            embed=discord.Embed(title=f"{interaction.user.name}'s Points Rain - **{amount:,}** Points", description=f"This chat rain has ended!")
            embed.set_footer(text=f"Points Rain owner refunded. No members joined the rain.")
            await m.edit(embed=embed, view=None)
            self.points[str(interaction.user.id)]["points"] += amount
            return

        for x in ids:
            self.points[x]["points"] += prize
        
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)
        
        embed=discord.Embed(title=f"{interaction.user.name}'s Rain - **{amount:,}** Points", description=f"This chat rain has ended! everyone got **{prize:,}** points each!")
        embed.set_footer(text=f"{len(ids)} members attended the points rain!")
        await m.edit(embed=embed, view=None)

    # Owner Commands
    @app_commands.command(name="modifypoints", description="[OWNER COMMAND] Modify a member's points.")
    @app_commands.choices(type=[Choice(name='add', value="add"), Choice(name='remove', value="remove"), Choice(name='set', value="set")])
    async def modifypoints(self, interaction : Interaction, member : discord.Member, type : str, amount : int):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        if type == "add":
            self.points[str(member.id)]["points"] += amount
            await interaction.response.send_message(f"Successfully added **{amount:,}** amount of points to {member.mention}")
        
        if type == "remove":
            self.points[str(member.id)]["points"] -= amount
            await interaction.response.send_message(f"Successfully removed **{amount:,}** amount of points to {member.mention}")
        
        if type == "set":
            self.points[str(member.id)]["points"] = amount
            await interaction.response.send_message(f"Successfully set {member.mention}'s points to **{amount:,}** points")
        
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)
    
    @app_commands.command(name="modifytokens", description="[OWNER COMMAND] Modify a member's tokens.")
    @app_commands.choices(type=[Choice(name='add', value="add"), Choice(name='remove', value="remove"), Choice(name='set', value="set")])
    async def modifytokens(self, interaction : Interaction, member : discord.Member, type : str, amount : int):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        if type == "add":
            self.points[str(member.id)]["tokens"] += amount
            await interaction.response.send_message(f"Successfully added **{amount:,}** amount of tokens to {member.mention}")
        
        if type == "remove":
            self.points[str(member.id)]["tokens"] -= amount
            await interaction.response.send_message(f"Successfully removed **{amount:,}** amount of tokens to {member.mention}")
        
        if type == "set":
            self.points[str(member.id)]["tokens"] = amount
            await interaction.response.send_message(f"Successfully set {member.mention}'s tokens to **{amount:,}** tokens")
        
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)
    
    @app_commands.command(name="toggleexchange", description="[OWNER COMMAND] Toggles exchanging on / off.")
    @app_commands.choices(type=[Choice(name='on', value="on"), Choice(name='off', value="off")])
    async def toggleexchange(self, interaction : Interaction, type : str):
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        if type == "on":
            self.exc = True
            await interaction.response.send_message("Successfully enabled exchanging!", ephemeral=True)
        
        if type == "off":
            await interaction.response.send_message("Successfully disabled exchanging!", ephemeral=True)
            self.exc = False

    @app_commands.command(name="transferpending", description="[OWNER COMMAND] Transfer a user's pending points to their balance.")
    async def transferpending(self, interaction : Interaction, member : discord.Member, amount : int = None):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        if amount == None:
            self.points[str(member.id)]["points"] += self.points[str(member.id)]["pending_points"]
            self.points[str(member.id)]["pending_points"] -= self.points[str(member.id)]["pending_points"]
            await interaction.response.send_message(f"Transfered all of pending points to {member.mention} balance.")
        
        else:
            self.points[str(member.id)]["points"] += amount
            self.points[str(member.id)]["pending_points"] -= amount
            await interaction.response.send_message(f"Transfered **{amount:,}** pending points to {member.mention} balance.")
        
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)

    @app_commands.command(name="removequeue", description="[OWNER COMMAND] Removes a user on queue.")
    @app_commands.describe(member="A member to remove their queue status", messageid="Queue message to delete")
    async def removequeue(self, interaction : Interaction, member : discord.Member, messageid: int):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        self.points[str(member.id)]["onqueue"] = False
        msg = await self.bot.get_message(968298064328658985, messageid)
        await self.bot.delete_message(msg)
        await interaction.response.send_message(f"Successfully removed {member.mention}'s queue status!")

        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)

    @app_commands.command(name="resetcrash", description="[OWNER COMMAND] Reset a user's crashing status.")
    @app_commands.describe(member="A member to reset their crashing status")
    async def resetcrash(self, interaction : Interaction, member : discord.Member):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        self.points[str(member.id)]["crashing"] = False
        await interaction.response.send_message(f"Successfully resetted {member.mention}'s crashing status!")
        
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)
    
    @app_commands.command(name="deletedata", description="[OWNER COMMAND] Deletes a user's data.")
    @app_commands.describe(member="A member to reset data from")
    async def deletedata(self, interaction : Interaction, member : discord.Member):
        with open(r"points.json", "r") as f:
            self.points = json.load(f)
        
        if interaction.user.id != 583200866631155714:
            return await interaction.response.send_message("You are not the owner of this bot!", ephemeral=True)

        del self.points[str(member.id)]
        await interaction.response.send_message(f"Successfully deleted {member.mention}'s data!")
        
        with open(r"points.json", "w") as f: 
            json.dump(self.points, f, indent=4)

async def setup(bot):
    await bot.add_cog(commands(bot))