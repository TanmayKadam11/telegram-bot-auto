from telethon import TelegramClient
import asyncio
import re
from datetime import datetime
last_period = {}

# ===== API =====
api_id = 23719051
api_hash = "83f2d45bf14e8efac72bbb71f28ffc56"

# ===== BOTS =====
bots = ['OkWinSureShot_bot', 'wingojalwahack_bot']

# ===== CLIENT =====
client = TelegramClient('session_new', api_id, api_hash)


# ===== WAIT NEXT MINUTE =====
async def wait_next_minute():
    now = datetime.now()
    wait = 60 - now.second
    print(f"⏳ Waiting {wait} sec...")
    await asyncio.sleep(wait)


# ===== EXTRACT DATA =====
def extract_data(text):
    period = None
    purchase = None

    lines = text.split("\n")

    for line in lines:
        if "Period" in line:
            match = re.search(r'\d+', line)
            if match:
                period = match.group()

        if "Purchase" in line:
            if "Big" in line:
                purchase = "Big"
            elif "Small" in line:
                purchase = "Small"

    return period, purchase


# ===== MAIN =====
async def main():
    await client.start()
    print("🚀 Bot Started")

    await wait_next_minute()

    while True:
        for bot in bots:
            try:
                print(f"👉 {bot}")

                # reconnect fix
                if not client.is_connected():
                    await client.connect()

                # send only once
                await client.send_message(bot, "🔮 Get Prediction")
                print("📩 Sent")

                await asyncio.sleep(3)

                msgs = await client.get_messages(bot, limit=5)

                for msg in msgs:
                    if msg.text and "Period" in msg.text:
                        period, purchase = extract_data(msg.text)

                        if period and purchase:

                            # 🔥 skip old data
                            if bot in last_period and last_period[bot] == period:
                                continue

                            last_period[bot] = period

                            print(f"✅ {bot} → {period} | {purchase}")
                            break

            except Exception as e:
                print("❌ Error:", e)

        print("⏳ Next round...\n")
        await wait_next_minute()


# ===== RUN =====
with client:
    client.loop.run_until_complete(main())