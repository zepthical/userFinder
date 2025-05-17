import discord
import requests
import asyncio

# === CONFIGURATION ===
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Replace with your bot's token
CHANNEL_ID = 1373295378195284040   # Replace with your Discord channel ID
USER_ID = 3753642683              # The Roblox user ID to monitor
CHECK_INTERVAL = 30               # How often to check (in seconds)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
last_status = None  # Keep track of the last presence status

def get_presence(user_id):
    url = "https://presence.roblox.com/v1/presence/users"
    headers = {"Content-Type": "application/json"}
    body = {"userIds": [user_id]}
    response = requests.post(url, json=body, headers=headers)
    return response.json()["userPresences"][0]

def format_status(presence_type):
    return ["Offline", "Online", "In Game", "In Studio"][presence_type]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    global last_status

    while True:
        try:
            presence = get_presence(USER_ID)
            current_status = presence["userPresenceType"]

            # Only respond if the user's status changed
            if current_status != last_status:
                last_status = current_status

                if current_status == 2:  # In Game
                    game_name = presence.get("lastLocation", "a game")
                    place_id = presence.get("placeId")
                    game_link = f"https://www.roblox.com/games/{place_id}" if place_id else "Game link unavailable"
                    await channel.send(
                        f"🎮 **User is now in-game!**\nGame: `{game_name}`\n🔗 {game_link}"
                    )

                elif current_status == 1:  # Online (not in a game)
                    await channel.send(f"🟢 **Phoenix is now online (not in a game).**")

                elif current_status == 0:  # Offline
                    await channel.send(f"🔴 **Phoenix went offline.**")

                elif current_status == 3:  # In Studio
                    await channel.send(f"🛠️ **Phoenix is working in Roblox Studio.**")

        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(CHECK_INTERVAL)

client.run(TOKEN)
