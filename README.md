# Discord AFK Voice Bot

[![GitHub](https://img.shields.io/badge/GitHub-Source-181717?logo=github)](https://github.com/v1p0r/discord_afk_bot)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-v1p0r%2Fdiscord--afk--bot-2496ED?logo=docker)](https://hub.docker.com/r/v1p0r/discord-afk-bot)

A lightweight, Dockerized Discord self-bot that joins a voice channel, self-mutes, and stays connected indefinitely. Control it via text commands from any channel.

> **Warning:** This is a self-bot that runs on a user account token. Self-bots violate [Discord's Terms of Service](https://discord.com/terms). Use at your own risk.

---

## Quick Start

```bash
docker run -d \
  --name afk-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN=your_token_here \
  -e DEFAULT_VC_ID=your_default_vc_id_here \
  v1p0r/discord-afk-bot:latest
```

---

## How to Use

### Option 1: `docker run`

Run the bot with a single command. Pass configuration as environment variables:

```bash
docker run -d \
  --name afk-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN=your_token_here \
  -e DEFAULT_VC_ID=your_default_vc_id_here \
  -e COMMAND_PREFIX=! \
  -e AUTO_JOIN=true \
  -e SELF_MUTE=true \
  -e SELF_DEAF=true \
  v1p0r/discord-afk-bot:latest
```

**Manage the container:**

```bash
# View logs
docker logs -f afk-bot

# Stop the bot
docker stop afk-bot

# Start it again
docker start afk-bot

# Remove the container
docker stop afk-bot && docker rm afk-bot
```

### Option 2: Docker Compose (recommended)

**1. Create a `docker-compose.yml` file:**

```yaml
services:
  afk-bot:
    image: v1p0r/discord-afk-bot:latest
    environment:
      - DISCORD_TOKEN=your_token_here
      - DEFAULT_VC_ID=123456789012345678
      - COMMAND_PREFIX=!
      - AUTO_JOIN=true
      - SELF_MUTE=true
      - SELF_DEAF=true
    restart: unless-stopped
```

**2. Start the bot:**

```bash
docker compose up -d
```

**3. Manage the bot:**

```bash
# View logs (live)
docker compose logs -f

# Stop the bot
docker compose down

# Pull latest version and restart
docker compose pull && docker compose up -d
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DISCORD_TOKEN` | **Yes** | — | Your Discord user account token |
| `DEFAULT_VC_ID` | **Yes** | — | Voice channel ID to join |
| `COMMAND_PREFIX` | No | `!` | Prefix for text commands |
| `AUTO_JOIN` | No | `false` | Auto-join voice channel on startup |
| `SELF_MUTE` | No | `true` | Self-mute when joining voice |
| `SELF_DEAF` | No | `false` | Self-deafen when joining voice |

### `DISCORD_TOKEN` (required)

Your Discord **user account** token. This is how the bot logs in as you.

**How to get it:**

1. Open Discord **in your browser** (not the desktop app)
2. Press `F12` to open Developer Tools
3. Go to the **Console** tab
4. Paste this snippet and press Enter:
   ```js
   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
   ```
5. Copy the output (the string between the quotes)

> **Security:** Treat this token like a password. Anyone with it has full access to your Discord account. Never share it publicly or commit it to git.

### `DEFAULT_VC_ID` (required)

The numeric ID of the voice channel the bot should join.

**How to get it:**

1. Open Discord and go to **User Settings** (gear icon)
2. Scroll to **Advanced** > toggle on **Developer Mode**
3. Close settings
4. Right-click the voice channel you want > **Copy Channel ID**

The ID will look something like: `1148442235457769543`

### `COMMAND_PREFIX` (optional)

The character(s) that trigger bot commands in text channels. Defaults to `!`.

Examples:
- `!` — commands are `!join`, `!leave`, `!status`
- `.` — commands are `.join`, `.leave`, `.status`
- `afk!` — commands are `afk!join`, `afk!leave`, `afk!status`

### `AUTO_JOIN` (optional)

Whether the bot automatically joins the voice channel when it starts. Defaults to `true`.

- `true` — bot connects to `DEFAULT_VC_ID` immediately on startup
- `false` — bot starts idle; you must type `!join` in a text channel to connect

### `SELF_MUTE` (optional)

Whether the bot self-mutes when joining voice. Defaults to `true`.

- `true` — you appear muted in the voice channel (microphone icon crossed out)
- `false` — you appear unmuted (your mic will be live)

### `SELF_DEAF` (optional)

Whether the bot self-deafens when joining voice. Defaults to `true`.

- `true` — you appear deafened (headphone icon crossed out). Deafened users are always muted too
- `false` — you can hear others in the channel (but you're likely AFK, so this doesn't matter much)

---

## Commands

Type these in any text channel while the bot is running:

| Command | Description |
|---|---|
| `!join` | Join the default voice channel |
| `!join <channel_id>` | Join a specific voice channel |
| `!leave` | Disconnect from voice |
| `!status` | Show connection status and uptime |

> Commands are only processed from **your own account** (self-bot behavior). Other users cannot control the bot.

---

## Building from Source

If you prefer to build the image yourself:

```bash
git clone https://github.com/v1p0r/discord_afk_bot.git
cd discord_afk_bot
docker build -t discord-afk-bot .
```

Then run with your local image:

```bash
docker run -d \
  --name afk-bot \
  --restart unless-stopped \
  -e DISCORD_TOKEN=your_token_here \
  -e DEFAULT_VC_ID=your_default_vc_id_here \
  -e COMMAND_PREFIX=! \
  -e AUTO_JOIN=false \
  -e SELF_MUTE=true \
  -e SELF_DEAF=false \
  v1p0r/discord-afk-bot:latest
```

---

## Image Details

| | |
|---|---|
| **Base image** | `python:3.11-slim` |
| **Architecture** | `amd64` |
| **Image size** | ~150 MB |
| **Source** | [GitHub](https://github.com/v1p0r/discord_afk_bot) |
| **Docker Hub** | [v1p0r/discord-afk-bot](https://hub.docker.com/r/v1p0r/discord-afk-bot) |

---

## License

MIT
