import nextcord
from nextcord.ext import commands
import requests

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_roblox_user_id(username):
    url = f"https://api.roblox.com/users/get-by-username?username={username}"
    res = requests.get(url).json()
    return res.get("Id", None)

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
    """User param can be Roblox username or user ID"""
    await interaction.response.defer()  # Acknowledge command immediately

    # Determine if input is user ID (digits) or username (letters)
    if user.isdigit():
        user_id = int(user)
    else:
        user_id = get_roblox_user_id(user)
        if user_id is None:
            await interaction.followup.send(f"❌ User `{user}` not found on Roblox.")
            return

    presence = get_presence(user_id)
    if presence is None:
        await interaction.followup.send(f"❌ Could not get presence info for user ID {user_id}.")
        return

    status_types = ["Offline", "Online", "In Game", "In Studio"]
    status = presence.get("userPresenceType", 0)
    last_location = presence.get("lastLocation", "N/A")
    place_id = presence.get("placeId", None)
    game_link = f"https://www.roblox.com/games/{place_id}" if place_id else "N/A"

    msg = f"**Roblox User ID:** {user_id}\n**Status:** {status_types[status]}\n"
    if status == 2:  # In Game
        msg += f"**Playing:** {last_location}\n**Game Link:** {game_link}"

    await interaction.followup.send(msg)

token = os.getenv('DISCORD_BOT_TOKEN')

bot.run(token)
