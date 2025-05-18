import nextcord
import os
from nextcord.ext import commands
import requests

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_roblox_user_id(username):
    url = f"https://users.roblox.com/v1/users/search?keyword={username}"
    res = requests.get(url).json()
    if "data" in res and len(res["data"]) > 0:
        return res["data"][0]["id"]
    return None

def get_presence(user_id):
    url = "https://presence.roblox.com/v1/presence/users"
    response = requests.post(url, json={"userIds": [user_id]})
    if response.status_code != 200:
        return None
    data = response.json()
    if not data["userPresences"]:
        return None
    return data["userPresences"][0]

@bot.slash_command(name="check", description="Check Roblox user's online status")
async def check(interaction: nextcord.Interaction, user: str):
    await interaction.response.defer()
    if user.isdigit():
        user_id = int(user)
    else:
        user_id = get_roblox_user_id(user)
        if user_id is None:
            await interaction.followup.send(f"❌ Roblox user `{user}` not found.")
            return

    presence = get_presence(user_id)
    if not presence:
        await interaction.followup.send("❌ Unable to fetch presence data.")
        return

    status_map = ["Offline", "Online", "In Game", "In Studio"]
    status = presence["userPresenceType"]
    place_id = presence.get("placeId")
    last_location = presence.get("lastLocation", "N/A")

    msg = f"👤 **Roblox User ID:** {user_id}\n"
    msg += f"📶 **Status:** {status_map[status]}\n"

    if status == 2 and place_id:
        msg += f"🎮 **Game:** {last_location}\n"
        msg += f"🔗 [Join Game](https://www.roblox.com/games/{place_id})"

    await interaction.followup.send(msg)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.sync_application_commands()
        print("✅ Slash commands synced")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

bot.run(TOKEN)
