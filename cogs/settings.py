import json
import os

import discord
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_path, "..", "config.json")
        self.server_configs = {}
        self.load_config()

    def load_config(self):
        """설정 파일(JSON)을 로드합니다."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.server_configs = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.server_configs = {}
        else:
            self.server_configs = {}

    def save_config(self):
        """현재 설정을 파일에 저장합니다."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.server_configs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")

    def get_server_data(self, guild):
        """서버별 데이터 구조를 반환하며, 없을 경우 초기화합니다."""
        gid = str(guild.id)

        if gid not in self.server_configs:
            self.server_configs[gid] = {
                "server_name": guild.name,
                "owner_id": guild.owner_id,
                "owner_name": str(guild.owner),
                "server_log_channel_id": None,
                "punish_log_channel_id": None,
                "command_channel_id": None
                }

        else:
            # 필수 키 누락 대비 기본값 채워넣기
            self.server_configs[gid]["server_name"] = guild.name

        self.save_config()
        return self.server_configs[gid]

# 설정 명령어
    @commands.command(name="set")
    @commands.has_permissions(administrator=True)
    async def set_command(self, ctx, target: str = None, channel: discord.TextChannel = None):
        """서버의 각종 로그 및 티켓 채널을 설정합니다."""
        key_map = {
            "server": "server_log_channel_id",
            "bot": "command_channel_id",
            "punish": "punish_log_channel_id"
            }
        

        if not target or target.lower() not in key_map:
            embed = discord.Embed(
                description=f"❓ 사용법: `{ctx.prefix}set [server/punish/bot/emoji/panel/ticket/all] [#채널]`",
                color=0x95A5A6
            )
            return await ctx.send(embed=embed)

        target = target.lower()
        target_channel = channel or ctx.channel
        gid = str(ctx.guild.id)
        self.get_server_data(ctx.guild)

        self.server_configs[gid][key_map[target]] = target_channel.id
        embed = discord.Embed(
            description=f"✅ **{target.upper()}** 채널이 {target_channel.mention}로 설정되었습니다.",
            color=0x2ECC71
        )

        self.save_config()
        await ctx.send(embed=embed)

    @commands.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def reset_command(self, ctx, target: str = None):
        """서버 설정을 초기화하거나 특정 채널 설정을 제거합니다."""
        gid = str(ctx.guild.id)
        key_map = {
            "server": "server_log_channel_id",
            "bot": "command_channel_id",
            "punish": "punish_log_channel_id"
            }

        if target == "all":
            self.server_configs.pop(gid, None)
            embed = discord.Embed(description="✅ 모든 설정이 초기화되었습니다.", color=0xE74C3C)
        elif target and target.lower() in key_map:
            target = target.lower()

            if gid in self.server_configs:
                self.server_configs[gid][key_map[target]] = None

                embed = discord.Embed(
                    description=f"✅ **{target.upper()}** 설정 및 패널이 제거되었습니다.",
                    color=0x95A5A6
                )
            else:
                embed = discord.Embed(description="❌ 설정된 데이터가 없습니다.", color=0xE74C3C)
        else:
            embed = discord.Embed(
                description=f"❓ 사용법: `{ctx.prefix}reset [server/punish/bot/emoji/panel/ticket/all]`",
                color=0x95A5A6
            )

        self.save_config()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Settings(bot))