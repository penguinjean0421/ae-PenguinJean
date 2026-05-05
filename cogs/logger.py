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
    async def on_message_edit(self, payload):
        if not payload.guild_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return

        channel = guild.get_channel(payload.channel_id)
        if not channel:
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
                msg = await channel.fetch_message(payload.message_id)
                if msg.author.bot: return
                author_name = str(msg.author)
                author_icon = msg.author.display_avatar.url
            except:
                pass

        after_content = payload.data.get('content')
        if after_content is None:
            return

        location = channel.mention
        if isinstance(channel, discord.Thread):
            if isinstance(channel.parent, discord.ForumChannel):
                location = f"📌 포럼: {channel.parent.mention} > 게시글: {channel.mention}"
            else:
                location = f"🧵 스레드: {channel.parent.mention} > {channel.mention}"

        embed = discord.Embed(
            title="📝 메시지 수정됨",
            description=f"**위치:** {location}\n[메시지 바로가기](https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})",
            color=0xF1C40F
        )
        embed.set_author(name=author_name, icon_url=author_icon)
        embed.add_field(name="수정 전", value=f"```{before_content}```", inline=False)
        embed.add_field(name="수정 후", value=f"```{self.escape_code_blocks(after_content)}```", inline=False)
        
        await self.send_log(guild, embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        if isinstance(message.channel, discord.Thread):
            is_forum = isinstance(message.channel.parent, discord.ForumChannel)
            title = "💬 포럼 댓글 작성" if is_forum else "💬 스레드 메시지 작성"
            
            embed = discord.Embed(
                title=title,
                description=f"**위치:** {message.channel.parent.mention} > {message.channel.mention}\n"
                            f"**작성자:** {message.author.mention}\n"
                            f"**내용:** ```{self.escape_code_blocks(message.content)}```",
                color=0x3498DB
            )
            embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
            embed.set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id}")
            
            await self.send_log(message.guild, embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if not payload.guild_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        
        # 메시지 정보 구성
        author_info = "알 수 없음 (캐시 없음)"
        content = "삭제된 메시지의 내용을 불러올 수 없습니다."
        
        if payload.cached_message:
            if payload.cached_message.author.bot: return
            author_info = f"{payload.cached_message.author.mention}"
            content = self.escape_code_blocks(payload.cached_message.content)

        # 채널 타입 판별 (스레드/포럼 여부)
        channel_type = "메시지"
        location = channel.mention
        if isinstance(channel, discord.Thread):
            if isinstance(channel.parent, discord.ForumChannel):
                channel_type = "포럼 댓글"
                location = f"{channel.parent.mention} > {channel.mention}"
            else:
                channel_type = "스레드 메시지"
                location = f"{channel.parent.mention} > {channel.mention}"

        embed = discord.Embed(
            title=f"🗑️ {channel_type} 삭제됨",
            description=f"**위치:** {location}\n**작성자:** {author_info}\n**내용:** ```{content}```",
            color=0xE74C3C
        )
        await self.send_log(guild, embed)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        is_forum = isinstance(thread.parent, discord.ForumChannel)
        title = "📌 새 포럼 게시글" if is_forum else "🧵 새 스레드 생성"
        color = 0x2ECC71

        embed = discord.Embed(
            title=title,
            description=f"**이름:** {thread.name}\n**상위 채널:** {thread.parent.mention}\n**생성자:** {thread.owner.mention if thread.owner else '알 수 없음'}",
            color=color
        )
        embed.set_footer(text=f"Thread ID: {thread.id}")
        await self.send_log(thread.guild, embed)

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        is_forum = isinstance(thread.parent, discord.ForumChannel)
        title = "🗑️ 포럼 게시글 삭제됨" if is_forum else "🗑️ 스레드 삭제됨"
        color = 0xE74C3C

        embed = discord.Embed(
            title=title,
            description=f"**이름:** {thread.name}\n**상위 채널:** {thread.parent.mention if thread.parent else '삭제된 채널'}",
            color=color
        )
        embed.set_footer(text=f"Thread ID: {thread.id}")
        await self.send_log(thread.guild, embed)

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        if before.name == after.name and before.archived == after.archived and before.locked == after.locked:
            return

        embed = discord.Embed(
            title="⚙️ 스레드/포럼 설정 변경",
            description=f"**대상:** {after.mention}",
            color=0xF1C40F
        )

        if before.name != after.name:
            embed.add_field(name="이름 변경", value=f"{before.name} ➡ {after.name}", inline=False)
        
        if before.archived != after.archived:
            status = "보관됨" if after.archived else "보관 해제됨"
            embed.add_field(name="보관 상태", value=status, inline=True)

        if before.locked != after.locked:
            status = "잠금됨" if after.locked else "잠금 해제됨"
            embed.add_field(name="잠금 상태", value=status, inline=True)

        if before.applied_tags != after.applied_tags:
            before_tags = ", ".join([t.name for t in before.applied_tags]) or "없음"
            after_tags = ", ".join([t.name for t in after.applied_tags]) or "없음"
            embed.add_field(name="태그 변경", value=f"{before_tags} ➡ {after_tags}", inline=False)

        await self.send_log(after.guild, embed)

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