import discord
from discord.ext import commands
import asyncio
import requests
import matplotlib.pyplot as plt
from matplotlib import font_manager
from io import BytesIO

from django.conf import settings
from django.core.management.base import BaseCommand
import datetime

import logging
import os
import requests
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

##host_url="http://127.0.0.1:8000/"
host_url="http://15.164.32.148:8000/"


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

client.load_extension("speech.spch_rcgn")

# Configuration of speech logger
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("speech.spch_rcgn")
logger.setLevel(logging.WARNING)

bad_words = ["바보", "멍청이", "똥개"]
user=[]
user_count=[]
@client.event
async def on_message(message):
    if 'said' in message.content:
        u = message.content.split('said:')[0].strip()
        t = message.content.split('said:')[1].strip()
        url_storesentence = host_url+"storesentence/"
        userid = u
        spoken_sentence = t
        serverid = "aaa" #random
        sentence_json = {"server": serverid, "user": userid, "sentence": spoken_sentence}
        request = requests.post(url_storesentence, json=sentence_json)
        count = request.json()["count"]
        if count > 0:
            await message.channel.send(f"{u}님, 욕설은 삼가해주세요!")
            await asyncio.sleep(0.5)
            await message.channel.send(f"{u}님을 뮤트 처리 했습니다.")
            chk = False
            for member in message.guild.members:
                if str(member.id) == u[2:-1]:
                    chk = True
                    await member.edit(mute=True)
                    await asyncio.sleep(30)
                    await member.edit(mute=False)
                if chk: break


        await message.channel.send(f"{u}님의 뮤트 처리를 해제했습니다.")
        return
    # for word in bad_words:
    #     if word in message.content:
    #         for i in range(5):
    #             await message.author.send(f"{message.author.mention}님, 욕설은 삼가해주세요!")
    #             await asyncio.sleep(0.5)
    #         await message.channel.send(f"{message.author.mention}님을 뮤트 처리 했습니다.")
    #         await message.author.edit(mute=True)
    #         await message.channel.send(message.author)
    #         await asyncio.sleep(30)
    #
    #         await message.author.edit(mute=False)
    #
    #         await message.channel.send(f"{message.author.mention}님의 뮤트 처리를 해제했습니다.")
    #         return
    await client.process_commands(message)

@client.command(name='userid')
async def commandlist(ctx):
    userid=str(ctx.message.author.id)
    await ctx.send("당신은 "+userid+"입니다.")

@client.command(name='명령어')
async def commandlist(ctx):
    help_embed=discord.Embed(title="명령어 도움말", description="이 봇이 제공하는 명령어들입니다.", color=0x00ff00)
    help_embed.add_field(name='!인사', value='봇이 인사해줍니다.', inline=False)
    help_embed.add_field(name='!멤버', value='현재 음성 채널에 있는 멤버를 출력해줍니다.', inline=False)
    help_embed.add_field(name='!하루통계', value='하루에 욕설한 사람과 욕설 횟수를 표와 그래프로 보여줍니다.', inline=False)
    help_embed.add_field(name='!1주통계', value='한 주동안 욕설한 사람과 욕설 횟수를 표와 그래프로 보여줍니다.', inline=False)
    help_embed.add_field(name='!5주통계', value='5주동안 욕설한 사람과 욕설 횟수를 표와 그래프로 보여줍니다.', inline=False)
    help_embed.add_field(name='!금지어추가 (단어)', value='해당 채팅방에 금지어로 사용할 단어를 추가합니다.', inline=False)
    help_embed.add_field(name='!금지어확인', value='금지어로 설정된 단어를 보여줍니다.', inline=False)
    await ctx.send(embed=help_embed)

@client.command(name='인사')
async def hello(ctx):
    user_name=ctx.author.name
    await ctx.send(f"{user_name}님, 안녕하세요 좋은 하루되세요~")


@client.command(name='멤버')
async def present_member(ctx):
    voice_state=ctx.author.voice
    members=voice_state.channel.members
    memberlist=[member.name for member in members]
    present_members="\n".join(memberlist)
    await ctx.send(f"현재 {voice_state.channel.name}에 있는 멤버: \n{present_members}")
    
##################################통계 관련 기능 추가##########################################

@client.command(name='하루통계')
async def print_server_count_date(ctx):
    slang_count={}
    embed=discord.Embed(title="오늘 통계", description="오늘 하루 욕설 횟수", color=discord.Color.dark_orange())
    serverid=str(ctx.message.guild.id)
    year=str(datetime.date.today().year)
    month=str(datetime.date.today().month)
    day=str(datetime.date.today().day)
    url=host_url+serverid+"/count_date/"+year+"/"+month+"/"+day
    response=requests.get(url)
    print("status_code:{}".format(response.status_code))
    if len(response.json())==0:
        print("list is empty")
    else:
        for i in range(0,len(response.json())):
            serverid=response.json()[i]["server"]
            userid=response.json()[i]["user"]
            count_date=response.json()[i]["count"]
            date=response.json()[i]["date"]
            user=await client.fetch_user(int(userid))
            embed.add_field(name=user.name, value=count_date, inline=True)
            slang_count[user.name]=count_date
        users=list(slang_count.keys())
        slang=list(slang_count.values())
        plt.bar(users, slang)
        plt.xlabel('욕설 사용자')
        plt.ylabel('욕설 횟수')
        plt.title('욕설 사용 통계')
        
        buffer=BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        file=discord.File(buffer, filename='slangcount1.png')
        await ctx.send(embed=embed)
        await ctx.send(file=file)
       

@client.command(name='1주통계')
async def print_server_count_week(ctx):
    slang_count={}
    embed=discord.Embed(title="이번주 통계", description="이번주 욕설 횟수", color=discord.Color.dark_orange())
    serverid=str(ctx.message.guild.id)
    year=str(datetime.date.today().year)
    week=str(datetime.date.today().isocalendar()[1])
    url=host_url+serverid+"/count_week/"+year+"/"+week
    response=requests.get(url)
    print("status_code:{}".format(response.status_code))
    if len(response.json())==0:
        print("list is empty")
    else:
        for i in range(0,len(response.json())):
            serverid=response.json()[i]["server"]
            userid=response.json()[i]["user"]
            count_week=response.json()[i]["count"]
            year=response.json()[i]["year"]
            week=response.json()[i]["week"]
            user=await client.fetch_user(int(userid))
            embed.add_field(name=user.name, value=count_week, inline=True)
            slang_count[user.name]=count_week
        users = list(slang_count.keys())
        slang = list(slang_count.values())
        plt.bar(users, slang)
        plt.xlabel('욕설 사용자')
        plt.ylabel('욕설 횟수')
        plt.title('욕설 사용 통계')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        file = discord.File(buffer, filename='slangcount2.png')
        await ctx.send(embed=embed)
        await ctx.send(file=file)

@client.command(name='5주통계')
async def print_server_count_week(ctx):
    embed = discord.Embed(title="통계", description="주차별 욕설 횟수", color=discord.Color.dark_orange())
    serverid = str(ctx.message.guild.id)
    year = str(datetime.date.today().year)
    week = datetime.date.today().isocalendar()[1]
    users = []
    slang = []
    week_lst=[]
    colors = ['red', 'blue', 'green', 'yellow', 'purple']
    fig, ax = plt.subplots()
    for i in range(4, -1, -1):
        week = str(datetime.date.today().isocalendar()[1] - i)
        week_lst.append(week)
        url = host_url + serverid + "/count_week/" + year + "/" + week
        response = requests.get(url)
        print("status_code:{}".format(response.status_code))

        if len(response.json()) == 0:
            print("list is empty")
        else:
            for i in range(0, len(response.json())):
                serverid = str(response.json()[i]["server"])
                userid = response.json()[i]["user"]
                count_week = response.json()[i]["count"]
                year = str(response.json()[i]["year"])
                week_pasing = response.json()[i]["week"]
                user = await client.fetch_user(int(userid))
                embed.add_field(name=user.name, value=count_week, inline=True)
                users.append(user.name)
                slang.append(count_week)
            embed.add_field(name="주차", value=week_pasing, inline=True)
    user_len=int(len(users)/5)
    for i in range(user_len):
        indices=[idx for idx in range(len(users)) if idx % user_len==i]
        y_data=[slang[idx] for idx in indices]
        ax.plot(week_lst, y_data, color=colors[i], marker='o', label='user'+str(i+1))
    ax.set_xlabel('주차')
    ax.set_ylabel('욕설 사용 횟수')
    ax.set_title('주차별 욕설 횟수')
    ax.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    file = discord.File(buffer, filename='slangcount3.png')
    await ctx.send(embed=embed)
    await ctx.send(file=file)
    plt.close(fig)



############################################################################


################################금지어 관련 기능 추가############################################

@client.command(name='금지어추가')
async def 금지어추가(ctx,*,text):
    server=str(ctx.message.guild.id)
    url_storeban=host_url+"storeban/"
    ban_word=text
    ban_json={"server":server,"banned":ban_word}
    response=requests.post(url_storeban, json=ban_json)
    if response.status_code==201:
        await ctx.send("금지어 '"+text+"' 가 추가되었습니다.")
    elif response.status_code==400:
        await ctx.send("금지어 '"+text+"' 는 이미 추가되어 있습니다.")



@client.command(name='금지어확인')
async def print_ban_word(ctx):
    serverid=str(ctx.message.guild.id)
    url=host_url+serverid+"/banned_check/"
    response=requests.get(url)
    print("status_code:{}".format(response.status_code))
    
    for i in range(0,len(response.json())):
        server=response.json()[i]["server"]
        ban_word=response.json()[i]["banned"]
        out=ban_word
        await ctx.send(out)
############################################################################

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel=client.get_channel(1065631703504273511)
    await channel.send('"!명령어" 입력시 명령어에 대해 설명해줍니다.')

@client.event
async def on_voice_state_update(member, before, after):
    await on_voice_state_update_print(member, before, after)
    await mute_voice(member, before, after)



@client.event
async def mute_voice(member, before, after):
    if after.channel:
        if len(user)!=0:
            for m in user:
                if m==member.id:
                    await member.edit(mute=True, reason="욕설 사용")
                    await asyncio.sleep(2)
                    await member.edit(mute=False)
                    user.remove(member.name)
                    break

@client.event
async def on_voice_state_update_print(member, before, after):
    if before.channel != after.channel:
        if after.channel:
            await member.guild.text_channels[0].send(f"{member.name}님이 음성 채널 {after.channel.name}에 입장했습니다.")
        elif before.channel:
            await member.guild.text_channels[0].send(f"{member.name}님이 음성 채널 {before.channel.name}에서 퇴장했습니다.")
    elif before.self_mute != after.self_mute and after.self_mute:
        await member.guild.text_channels[0].send(f"{member.name}님이 자신의 마이크를 음소거했습니다.")
    elif before.self_deaf != after.self_deaf and after.self_deaf:
        await member.guild.text_channels[0].send(f"{member.name}님이 자신의 스피커를 음소거했습니다.")


client.run(os.getenv("TOKEN"))
