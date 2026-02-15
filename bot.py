"""
Discord AFK Voice Bot (Self-Bot)

Joins a voice channel, self-mutes, and stays connected indefinitely.
Reads text commands from any text channel for control.

Commands:
    !join [channel_id]  - Join a voice channel (default if no ID given)
    !leave              - Disconnect from voice
    !status             - Show connection status and uptime
"""

import logging
import os
import time

import discord
from discord.ext import commands
# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_VC_ID = int(os.getenv("DEFAULT_VC_ID"))
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
AUTO_JOIN = os.getenv("AUTO_JOIN", "false").lower() == "true"
SELF_MUTE = os.getenv("SELF_MUTE", "true").lower() == "true"
SELF_DEAF = os.getenv("SELF_DEAF", "false").lower() == "true"

if not TOKEN:
    raise SystemExit("ERROR: DISCORD_TOKEN not set in .env file.")
if not DEFAULT_VC_ID:
    raise SystemExit("ERROR: DEFAULT_VC_ID not set in .env file.")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("afk-bot")

# ---------------------------------------------------------------------------
# Bot setup
# ---------------------------------------------------------------------------

bot = commands.Bot(command_prefix=COMMAND_PREFIX, self_bot=True)

# Track state for status command — stored on the bot object
bot.state = {
    "connected_since": None,       # timestamp when voice was joined
    "target_channel_id": None,     # channel we *want* to be in
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def join_voice(channel: discord.VoiceChannel) -> bool:
    """Join a voice channel and self-mute. Returns True on success."""
    try:
        # Disconnect from any existing voice connection in this guild first
        existing_vc = channel.guild.voice_client
        if existing_vc:
            await existing_vc.disconnect(force=True)

        log.info("Connecting to #%s (ID: %s) ...", channel.name, channel.id)
        await channel.connect()

        # Self-mute and self-deafen via the gateway websocket
        await bot.ws.voice_state(
            channel.guild.id, channel.id, self_mute=SELF_MUTE, self_deaf=SELF_DEAF
        )

        bot.state["connected_since"] = time.time()
        bot.state["target_channel_id"] = channel.id

        log.info("Joined #%s (muted).", channel.name)
        return True

    except Exception as exc:
        log.error("Failed to join #%s: %s", channel.name, exc)
        return False


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


@bot.event
async def on_ready():
    log.info("Logged in as %s (ID: %s)", bot.user.name, bot.user.id)

    if AUTO_JOIN and DEFAULT_VC_ID:
        channel = bot.get_channel(DEFAULT_VC_ID)
        if channel:
            await join_voice(channel)
        else:
            log.error("Default voice channel ID %s not found.", DEFAULT_VC_ID)
    else:
        log.info("Auto-join disabled. Use %sjoin to connect to the DEFAULT_VC_ID.", COMMAND_PREFIX)



# ---------------------------------------------------------------------------
# Text Commands
# ---------------------------------------------------------------------------


@bot.command(name="join")
async def cmd_join(ctx, channel_id: int = None):
    """Join a voice channel. Uses default if no ID is given."""
    target_id = channel_id or DEFAULT_VC_ID
    if not target_id:
        log.warning("No channel ID provided and no default set.")
        return

    channel = bot.get_channel(target_id)
    if channel is None:
        log.warning("Channel ID %s not found.", target_id)
        return
    if not isinstance(channel, discord.VoiceChannel):
        log.warning("Channel %s is not a voice channel.", target_id)
        return

    await join_voice(channel)


@bot.command(name="leave")
async def cmd_leave(ctx):
    """Disconnect from the current voice channel."""
    bot.state["target_channel_id"] = None
    bot.state["connected_since"] = None

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        log.info("Disconnected from voice by command.")
    else:
        log.info("Not currently in a voice channel.")



@bot.command(name="status")
async def cmd_status(ctx):
    """Print the current bot status to the log and reply in chat."""
    if bot.state["connected_since"]:
        uptime_seconds = int(time.time() - bot.state["connected_since"])
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        channel = bot.get_channel(bot.state["target_channel_id"])
        channel_name = channel.name if channel else "unknown"

        msg = f"Connected to #{channel_name} for {hours:02d}:{minutes:02d}:{seconds:02d}"
        log.info("Status: %s", msg)
        await ctx.send(msg)
    else:
        msg = "Not connected to any voice channel."
        log.info("Status: %s", msg)
        await ctx.send(msg)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    log.info("Starting AFK Voice Bot ...")
    bot.run(TOKEN)
