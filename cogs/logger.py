import discord
from datetime import datetime
from discord.ext import commands


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel(self, guild, type="general"):
        settings = self.bot.get_cog('Settings')
        if not settings:
            return guild.system_channel

        data = settings.get_server_data(guild)
        if type == "punish":
            chn_id = data.get("punish_log_channel_id") or data.get("server_log_channel_id")
        elif type == "ticket":
            chn_id = data.get("ticket_log_channel_id") or data.get("server_log_channel_id")
        else:
            chn_id = data.get("server_log_channel_id")

        return self.bot.get_channel(chn_id) if chn_id else guild.system_channel

    def escape_code_blocks(self, content: str, limit: int = 1000) -> str:
        if not content:
            return "내용 없음"
        
        if len(content) > limit :
            content = content[:limit] + "..."

        return content.replace("```", "`\u200b`\u200b` ")

    async def send_log(self, guild, embed, type="general"):
        log_channel = self.get_log_channel(guild, type)

        # 권한 확인 및 메시지 전송
        if log_channel and log_channel.permissions_for(guild.me).send_messages:
            if not embed.timestamp:
                embed.timestamp = datetime.now()
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="📥 멤버 입장",
            description=f"{member.mention} **{member}** 님이 입장했습니다.",
            color=0x2ECC71
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text=f"ID: {member.id} | 총 멤버: {member.guild.member_count}명"
        )
        await self.send_log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="📤 멤버 퇴장",
            description=f"**{member}** 님이 서버를 떠났습니다.",
            color=0xE74C3C
        )
        embed.set_footer(
            text=f"ID: {member.id} | 남은 멤버: {member.guild.member_count}명"
        )
        await self.send_log(member.guild, embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if not payload.guild_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        author_name = "알 수 없음"
        author_icon = None
        before_content = "캐시에 없음 (재시작 전 메시지)"

        if payload.cached_message:
            if payload.cached_message.author.bot:
                return
            author = payload.cached_message.author
            author_name = str(author)
            author_icon = author.display_avatar.url
            before_content = self.escape_code_blocks(payload.cached_message.content)
        else:
            try:
                channel = guild.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                if msg.author.bot: return
                author_name = str(msg.author)
                author_icon = msg.author.display_avatar.url
            except:
                pass

        after_content = payload.data.get('content')
        if after_content is None:
            return
        
        if payload.cached_message and payload.cached_message.content == after_content:
            return

        embed = discord.Embed(
            title="📝 메시지 수정됨",
            description=f"[메시지 바로가기](https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})",
            color=0xF1C40F
        )
        embed.set_author(name=author_name, icon_url=author_icon)
        embed.add_field(name="수정 전", value=f"```{before_content}```", inline=False)
        embed.add_field(name="수정 후", value=f"```{self.escape_code_blocks(after_content)}```", inline=False)
        
        await self.send_log(guild, embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return

        embed = discord.Embed(
            title="🗑️ 메시지 삭제됨",
            color=0xE74C3C
        )
        embed.description = (
            f"**작성자:** {message.author.mention}\n"
            f"**채널:** {message.channel.mention}\n"
            f"**내용:** ```{self.escape_code_blocks(message.content)}```"
        )
        await self.send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return

        user_info = f"{member.mention} **({member.id})**"

        if not before.channel:
            desc = f"🔊 {user_info} 님이 **{after.channel.name}** 입장"
            color = 0x2ECC71
        elif not after.channel:
            desc = f"🔇 {user_info} 님이 **{before.channel.name}** 퇴장"
            color = 0x95A5A6
        else:
            desc = f"🔄 {user_info}: **{before.channel.name}** ➡ **{after.channel.name}**"
            color = 0xF1C40F

        embed = discord.Embed(description=desc, color=color)
        await self.send_log(member.guild, embed)


async def setup(bot):
    await bot.add_cog(Logger(bot))