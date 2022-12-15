""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1.1
"""

import datetime
import re
import aiohttp
import disnake
import requests
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from helpers import checks
from pathlib import Path



# Here we name the cog and create a new class for the cog.
class card_realted(commands.Cog, name="card-slash"):
    def __init__(self, bot):
        self.bot = bot
        
    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.slash_command(
        name="cardinfo",
        description="Database update every 30 days. Contact MeiMei#3717 if something huge dropped.",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    # This will only allow owners of the bot to execute the command -> config.json
    #@checks.is_owner()
    async def testcommand(self, interaction: ApplicationCommandInteraction, input_name: str):
        """
        This is a command that does Yu-Gi-oh! stuffs.
        Note: This is a SLASH command
        :param interaction: The application command interaction.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/cards.json") as r:
                
                embed = disnake.Embed(
                        title="Error!",
                        description="Cannot find the card for now. \n Most likely our databases do not have the card.",
                        color=0xE02B2B
                    )
                
                en_name = ""

                if r.status == 200:
                    card_infos = await r.json()
                    for card in card_infos:
                        for card_name in card:                            
                            card_details = card[card_name]
                            en_name = card_name
                            jp_name = card_details["Japanese name"]
                            id = card_details["Card ID"]
                            details = card_details["Details"]
                            
                            if re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_name).lower() \
                            in re.sub('[^a-zA-Z0-9 \n\.]', ' ', en_name).lower():
                                
                                print("Finding similar name")
                                embed = disnake.Embed(
                                title=en_name,
                                description=jp_name,
                                timestamp=datetime.datetime.now(),
                                color=0x9C84EF
                                )

                                # Regular Fields
                                # none for now

                                # Inline Fields
                                for detail in details:
                                    
                                    for set_code in detail:
                                        price = "Out stock!"
                                        if detail[set_code]['price'] != 0:
                                            price = "{} JPY".format(detail[set_code]['price'])
                                        
                                        rarity = detail[set_code]['rarity']
                                        
                                        if rarity == "ｼｰｸﾚｯﾄ":
                                            rarity = "SCR"
                                        elif rarity == "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ":
                                            rarity = "CR"
                                        elif rarity == "ｱﾙﾃｨﾒｯﾄ":
                                            rarity = "Ultimate R"
                                        
                                        condition = detail[set_code]['condition']
                                        
                                        embed.add_field(name="Info", 
                                        value="{}\nPrice: {}\nRarity: {}\nCondition: {}" \
                                        .format(set_code, price, rarity, condition),
                                        inline=True)
                                        
                                id = int(id)
                                path = "pics/{}.jpg".format(id)
                
                                if Path(path).is_file():
                                    print("Requested an already existed image")
                                else:
                                    print("Requested a non-existed image. Downloading it...")
                                    img_url = "https://images.ygoprodeck.com/images/cards/{}.jpg".format(id)
                                    img_data = requests.get(img_url).content
                                    with open(path, 'wb') as handler:
                                        handler.write(img_data)

                                embed.set_image(file=disnake.File(path))

                                embed.set_footer(text="Card ID: {}".format(id),)

                                break
                        

                    for card in card_infos:
                        for card_name in card:                            
                            card_details = card[card_name]
                            en_name = card_name
                            jp_name = card_details["Japanese name"]
                            id = card_details["Card ID"]
                            details = card_details["Details"]
                        
                            if re.sub('[^a-zA-Z0-9 \n\.]', ' ', input_name).lower() \
                            == re.sub('[^a-zA-Z0-9 \n\.]', ' ', en_name).lower():
                                print("Finding exact name")
                                embed = disnake.Embed(
                                title=en_name,
                                description=jp_name,
                                timestamp=datetime.datetime.now(),
                                color=0x9C84EF
                                )

                                # Regular Fields
                                # none for now

                                # Inline Fields
                                for detail in details:
                                    for set_code in detail:
                                        price = "Out stock!"
                                        if detail[set_code]['price'] != 0:
                                            price = "{} JPY".format(detail[set_code]['price'])
                                        
                                        rarity = detail[set_code]['rarity']
                                        if rarity == "ｼｰｸﾚｯﾄ":
                                            rarity = "SCR"
                                        elif rarity == "【TRC1】ﾚｱﾘﾃｨ･ｺﾚｸｼｮﾝ":
                                            rarity = "CR"
                                        elif rarity == "ｱﾙﾃｨﾒｯﾄ":
                                            rarity = "Ultimate R"
                                        
                                        condition = detail[set_code]['condition']

                                        embed.add_field(name="Info", 
                                        value="{}\nPrice: {}\nRarity: {}\nCondition: {}" \
                                        .format(set_code, price, rarity, condition), 
                                        inline=True)

                                id = int(id)

                                path = "pics/{}.jpg".format(id)
                
                                if Path(path).is_file():
                                    print("Requested an already existed image")
                                else:
                                    print("Requested a non-existed image. Downloading it...")
                                    img_url = "https://images.ygoprodeck.com/images/cards/{}.jpg".format(id)
                                    img_data = requests.get(img_url).content
                                    with open(path, 'wb') as handler:
                                        handler.write(img_data)
   
                                embed.set_image(file=disnake.File(path))      
                                
                                embed.set_footer(text="Card ID: {}".format(id),)

                                break
       

                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="There is something wrong with the server, please try again later. Or contact me at MeiMei#3717 on Discord if the error still continue",
                        color=0xE02B2B
                    )
                print("Finish resolving (might be fizzle i don't know)")
                await interaction.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(card_realted(bot))   
