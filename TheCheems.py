import asyncio
import discord
from discord.ext import commands


discord.Intents(guild_messages=True, messages=True, message_content=True)
bot = commands.Bot(command_prefix='¡', intents=discord.Intents.all())
token = "MTA4NDIyMDM0MDc0NzYzMjY0MA.GU_SFH.-blsTf8rVd2c863mFnxCmkSFhD1asBEvmcsk-g"

intents = discord.Intents.default()
intents.messages = True
intents.members = True


# Eliminar el comando help
bot.remove_command('help')

# Comandos

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a member."""
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    """Unban a member."""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.name} has been unbanned.')
            return

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a member."""
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} has been kicked.')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    """Mute a member."""
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if mute_role is None:
        # Create the mute role if it doesn't exist
        mute_role = await ctx.guild.create_role(name='Muted', reason='Mute role for moderation')
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute_role, send_messages=False)
    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.name} has been muted.')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    """Unmute a member."""
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f'{member.name} has been unmuted.')
    else:
        await ctx.send(f'{member.name} is not muted.')


@bot.command()
@commands.has_role(1062140047240986664)
async def clear(ctx, amount: int):
    """Comando para eliminar mensajes en masa"""
    if amount <= 0:
        await ctx.send("Por favor, proporciona un número mayor que cero.")
        return
    elif amount > 100:
        await ctx.send("El límite máximo para eliminar mensajes es 100.")
        return

    channel = ctx.channel
    messages = []
    async for message in channel.history(limit=amount + 1):  # Se suma 1 para incluir el propio comando
        messages.append(message)

    for message in messages:
        await message.delete()

    await ctx.send(f"Se han eliminado {amount} mensajes.", delete_after=5)  # Mensaje de confirmación

@bot.command()
async def tiktok(ctx):
    url = 'https://www.tiktok.com/@gato.bloxfuits' # URL del perfil de TikTok
    await ctx.send(url)


# Comando Help
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Ayuda", color=0xFFA500)
    embed.add_field(name="Moderación", value="Comandos de moderación\n!kick - Expulsa a un usuario del servidor\n!ban - Banea a un usuario del servidor\n!unban - Desbanea a un usuario del servidor\n!mute - Mutea a un usuario del servidor\n!unmute - Desmutea a un usuario del servidor", inline=False)
    embed.add_field(name="Perfil de TikTok", value="!tiktok - Muestra el enlace del perfil de TikTok de Gato", inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await asyncio.sleep(3)
    await bot.change_presence(activity=discord.Game(name="Blox Fruits"))

bot.run(token)

