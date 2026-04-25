import discord
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_data = {
            "name": "æ-PENGUINJEAN",
            "color": 0x0F4C81,
            "welcome": {
                "greeting": "서버에 초대해 주셔서 감사합니다!\n",
                "summary": "원활한 서버 관리를 위한 주요 명령어들을 안내해 드립니다.\n",
            },
            "credit": {
                "developer": "penguinjean0421",
                "support": "", 
                "repository": "ae-PenguinJean"
            },
        }

    # --- 도움말 관련 메서드 ---
    async def send_welcome_help(self, channel: discord.abc.Messageable, prefix: str = None):
        name = self.bot_data["name"]
        color = self.bot_data["color"]
        data = self.bot_data["welcome"]

        if prefix is None:
            prefix = self.bot.command_prefix
            if isinstance(prefix, list):
                prefix = prefix[0]

        embed = discord.Embed(
            title=f"👋 {name} 입니다.",
            description=f"{data['greeting']}{data['summary']}",
            color=color
        )
        
        embed.add_field(name="🆔 접두사(Prefix)", value=f"`{prefix}`", inline=False)
        embed.add_field(name="📖 도움말 명령어", value=f"`{prefix}help`", inline=True)
        
        embed.add_field(
            name="⚙️ 시스템 설정",
            value=(
                f"`{prefix}set [server/punish/bot/panel/ticket] [#채널]` : 채널 설정\n"
                f"`{prefix}reset [server/punish/bot/panel/ticket]` : 설정 해제\n"
                f"`{prefix}reset all` : 모든 설정 초기화"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔇 음성 제재",
            value=(
                f"`{prefix}mute [유저] (시간)` : 마이크 차단\n"
                f"`{prefix}unmute [유저]` : 마이크 해제\n"
                f"`{prefix}vckick [유저] (사유)` : 음성 채널 강제 퇴장"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔨 서버 제재",
            value=(
                f"`{prefix}timeout [유저] [시간] (사유)` : 타임아웃\n"
                f"`{prefix}kick [유저] (사유)` : 서버 추방\n"
                f"`{prefix}ban [유저] (사유)` : 서버 차단\n"
                f"`{prefix}unban [ID/닉네임]` : 차단 해제"
            ),
            inline=False
        )

        embed.add_field(
            name="🎫 티켓 시스템",
            value=(
                f"`{prefix}open` : 티켓 열기\n"
                f"`{prefix}close` : 티켓 닫기 버튼 전송\n"
                f"`{prefix}answer [#채널] 내용` : 답변을 임베드로 전송"
                ), 
                inline=False,
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text="시간 단위: s(초), m(분), h(시간), d(일) | 예: 10m, 1d",
            icon_url=self.bot.user.display_avatar.url
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        logger_cog = self.bot.get_cog("Logger")
        channel = None
        
        if logger_cog:
            channel = logger_cog.get_log_channel(guild)
            
        if not channel:
            channel = guild.system_channel
            
        if channel and channel.permissions_for(guild.me).send_messages:
            await self.send_welcome_help(channel)

    @commands.command(name="help", aliases=["도움말", "guide"])
    async def help_command(self, ctx: commands.Context):
        await self.send_welcome_help(ctx.channel, ctx.prefix)

    # --- 크레딧 관련 메서드 ---
    async def send_credit(self, ctx: commands.Context):
        name = self.bot_data["name"]
        color = self.bot_data["color"]
        data = self.bot_data["credit"]

        embed = discord.Embed(
            title=f"Thanks for using {name}",
            description=f"{name}을 만들고, 관리하는 사람 입니다.",
            color=color
        )
        
        embed.add_field(
            name=f"👤 Developer : {data['developer']}",
            value=(
                f"📧 E-Mail : `{data['developer']}@gmail.com`\n"
                f"✉️ Discord : [@🐧](https://discord.com/users/{data['developer']})\n"
                f"💻 GitHub: [@{data['developer']}](https://github.com/{data['developer']})"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Support Server",
            value=f"[Join a Server](https://discord.gg/{data['support']})",
            inline=False
        )
        
        embed.add_field(
            name="🔗 Source Code",
            value=(
                f"[GitHub Repository]"
                f"(https://github.com/{data['developer']}/{data['repository']})"
            ),
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"© 2026 {data['developer']} All rights reserved.")
        await ctx.send(embed=embed)

    @commands.command(name="credit", aliases=["크레딧"])
    async def credit_command(self, ctx: commands.Context):
        await self.send_credit(ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))