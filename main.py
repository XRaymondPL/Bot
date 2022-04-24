from dis import disco
from http import client
import imp
from ntpath import join
from pydoc import describe
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import pymongo
from pymongo import MongoClient
from datetime import datetime

client = commands.Bot(command_prefix= "dh!")
client.remove_command("help")

@client.event
async def on_ready():
    print("Online")
    await client.change_presence(activity=discord.Game(name="dh!pomoc"))

@client.command()
async def pomoc(ctx):
    embed=discord.Embed(title="Pomoc", url="https://www.youtube.com/channel/UCvXqOLKhE-U6ufEWyLH7QHA ", description="**Komendy:**", color=0xff0000)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/964548560962060378/967731383139205190/standard.gif")
    embed.add_field(name="dh!pomoc", value="Wyświetla komendy", inline=True)
    embed.add_field(name="dh!ban @użytkownik powód", value="banuje użytkownika", inline=True)
    embed.add_field(name="dh!kick @użytkownik powód", value="wyrzuca użytkownika", inline=True)
    embed.add_field(name="dh!warn @użytkownik powód", value="warnuje użytkownika", inline=True)
    embed.add_field(name="dh!unwarn @użytkownik", value="odwarnowywuje użytkownika", inline=True)
    embed.add_field(name="dh!server_info", value="wyświetla informacje o serwerze", inline=True)
    embed.add_field(name="dh!user_info @użytkownik", value="wyświetla informacje o użytkowniku", inline=True)
    embed.set_footer(text="Drop Hub &copy 2022")
    await ctx.send(embed=embed)

@client.command()
async def graj(ctx, game):
    await client.change_presence(activity=discord.Game(name=game))

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason="Bez Powodu"):
   await member.ban(reason=reason)
   await ctx.channel.send(f'Zbanowano {member.mention} za {reason}')

@client.command()
@has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member, reason="Bez Powodu"):
   await member.kick(reason=reason)
   await ctx.channel.send(f'Wyrzucono {member.mention} za {reason}')

cluster = MongoClient("mongodb+srv://XRaymondPL:Lol1234-@cluster0.ir6vj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = cluster["Cluster0"]
collection = database["Warn-Database"]

@client.command()
@has_permissions(ban_members=True)
async def warn(ctx, member : discord.Member, reason="Bez Powodu"):
    id = member.id

    if collection.count_documents({"memberid":id}) == 0:
        collection.insert_one({"memberid": id, "warns": 0})

    warn_count = collection.find_one({"memberid":id})
    
    count = warn_count["warns"]
    new_count = count + 1

    collection.update_one({"memberid":id},{"$set":{"warns": new_count}})
    await ctx.channel.send(f'Zwarnowano {member.mention} za {reason} | Ma teraz {new_count} warn/y/ów')

@client.command()
@has_permissions(ban_members=True)
async def unwarn(ctx, member : discord.Member):
    id = member.id

    if collection.count_documents({"memberid":id}) == 0:
        collection.delete_one({"memberid": id, "warns": 0})

    warn_count = collection.find_one({"memberid":id})
    
    count = warn_count["warns"]
    new_count = count - 1

    collection.update_one({"memberid":id},{"$set":{"warns": new_count}})
    await ctx.channel.send(f'Odwarnowano {member.mention} | Ma teraz {new_count} warn/y/ów')

@client.command()
async def server_info(ctx):
    embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, title="Server info", url="https://www.youtube.com/channel/UCvXqOLKhE-U6ufEWyLH7QHA", description="Informations about server")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/964548560962060378/967731383139205190/standard.gif")
    embed.set_footer(text=f'Requested by - {ctx.author}')
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="Owner", value='<@904342910651232256>', inline=True)
    embed.add_field(name="Created at", value=ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Members", value=len(ctx.guild.members), inline=True)
    embed.add_field(name="Humans", value=len(list(filter(lambda m: not m.bot, ctx.guild.members))), inline=True)
    embed.add_field(name="Bots", value=len(list(filter(lambda m: m.bot, ctx.guild.members))), inline=True)
    embed.add_field(name="Banned members", value=len(await ctx.guild.bans()), inline=True)
    embed.add_field(name="Text channels", value=len(ctx.guild.text_channels), inline=True)
    embed.add_field(name="Voice channels", value=len(ctx.guild.voice_channels), inline=True)
    await ctx.send(embed=embed)

@client.command()
async def user_info(ctx, user : discord.Member=None):
    if user==None:
        user=ctx.author
    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)
    b = ", ".join(rlist)
    embed = discord.Embed(url="https://www.youtube.com/channel/UCvXqOLKhE-U6ufEWyLH7QHA", colour=0xff0000,timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
    icon_url=ctx.author.avatar_url)
    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)
    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)
    embed.add_field(name='Bot?',value=user.bot,inline=False)
    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)
    await ctx.send(embed=embed)

client.run("OTY3NzIzNTEyOTE3ODE1Mjk2.YmUcwA.--j9VG-fYPCL5wMo3Tkqz6l3OvY")