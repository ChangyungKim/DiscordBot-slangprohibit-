import discord
import logging
import os
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

client.load_extension("speech.spch_rcgn")

# Configuration of speech logger
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("speech.spch_rcgn")
logger.setLevel(logging.WARNING)

bad_words = ["바보", "멍청이", "똥개"]
user=["찬경"]
user_count=[]
@client.event
async def on_message(message):
    for word in bad_words:
        if word in message.content:
            for i in range(5):
                await message.author.send(f"{message.author.mention}님, 욕설은 삼가해주세요!")
                await asyncio.sleep(0.5)
            await message.channel.send(f"{message.author.mention}님을 뮤트 처리 했습니다.")
            await message.author.edit(mute=True)

            await asyncio.sleep(30)

            await message.author.edit(mute=False)

            await message.channel.send(f"{message.author.mention}님의 뮤트 처리를 해제했습니다.")
            return
    await client.process_commands(message)

@client.command(name='명령어')
async def commandlist(ctx):
    help_embed=discord.Embed(title="명령어 도움말", description="이 봇이 제공하는 명령어들입니다.", color=0x00ff00)
    help_embed.add_field(name='!인사', value='봇이 인사해줍니다.', inline=False)
    help_embed.add_field(name='!멤버', value='현재 음성 채널에 있는 멤버를 출력해줍니다.', inline=False)

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
