import asyncio
import os
from pathlib import Path
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env 환경 변수 로드
load_dotenv()


class AePenguinJean(commands.Bot):
    def __init__(self):
        raw_prefixes = os.getenv("BOT_PREFIXES")  # 기본값 설정 권장
        prefixes: List[str] = [p.strip() for p in raw_prefixes.split(",")]

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.voice_states = True

        super().__init__(
            command_prefix=prefixes,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """봇 실행 시 Cog 파일을 자동으로 로드합니다."""
        cogs_path = Path(__file__).parent / "cogs"

        if not cogs_path.exists():
            cogs_path.mkdir()
            print("📂 'cogs' 폴더가 없어 새로 생성했습니다.")

        for filepath in cogs_path.glob("*.py"):
            if filepath.stem.startswith("__"):
                continue

            cog_name = f"cogs.{filepath.stem}"
            try:
                await self.load_extension(cog_name)
                print(f"✅ {cog_name} 로드 성공")
            except Exception as e:
                print(f"❌ {cog_name} 로드 실패 -> {e}")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """명령어 성공 시 유저의 입력 메시지를 자동 삭제합니다."""
        if ctx.guild and ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            try:
                await ctx.message.delete()
            except discord.NotFound:
                pass

    async def on_ready(self):
        print("-" * 30)
        print(f"🟢 {self.user.name} 온라인!")
        print(f"🆔 ID: {self.user.id}")
        print(f"🔢 접두사: {', '.join(self.command_prefix)}")
        print("-" * 30)
        await self.change_presence()


async def main():
    bot = AePenguinJean()
    token = os.getenv("BOT_TOKEN")

    if not token:
        print("❌ 오류: BOT_TOKEN이 .env 파일에 설정되지 않았습니다.")
        return

    async with bot:
        try:
            await bot.start(token)
        except discord.LoginFailure:
            print("❌ 오류: 토큰이 유효하지 않습니다.")
        except Exception as e:
            print(f"❌ 실행 중 오류 발생: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n종료 신호를 감지하여 봇을 종료합니다.")