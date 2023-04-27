import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

bad_words = ["바보", "멍청이", "똥개"]

@client.event
async def on_message(message):
    for word in bad_words:
        if word in message.content:
            await message.channel.send(f"{message.author.mention}님, 욕설은 삼가해주세요!")
            await message.channel.send(f"{message.author.mention}님을 뮤트 처리 했습니다.")
            await message.author.edit(mute=True)

            await asyncio.sleep(60)

            await message.author.edit(mute=False)

            await message.channel.send(f"{message.author.mention}님의 뮤트 처리를 해제했습니다.")
            return
    await client.process_commands(message)

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


@client.event
async def on_voice_state_update(member, before, after):
    await on_voice_state_update_print(member, before, after)



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


client.run("MTEwMDc4OTg3ODg2NzkwNjU4MA.G3CKZV._7KOk-6-rbEvsLdz1n05mfNSyPjJFKpVjYwNW8")
