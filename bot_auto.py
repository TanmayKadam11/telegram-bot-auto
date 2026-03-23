from telethon import TelegramClient
import asyncio
import re
from datetime import datetime

# ===== YOUR API =====
api_id = 23719051
api_hash = "83f2d45bf14e8efac72bbb71f28ffc56"

# ===== BOTS =====
bots = ['OkWinSureShot_bot', 'wingojalwahack_bot']

# ===== CLIENT =====
client = TelegramClient('session_vps', api_id, api_hash)


# ===== WAIT NEXT MINUTE =====
async def wait_next_minute():
    now = datetime.now()
    sec = now.second
    wait = 60 - sec
    print(f"⏳ Waiting {wait} sec for next minute...")
    await asyncio.sleep(wait)


# ===== EXTRACT DATA =====
def extract_data(text):
    period = None
    purchase = None

    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "Period" in line:
            p = re.search(r'\d+', line)
            if p:
                period = p.group()

        if "Purchase" in line:
            if "Big" in line:
                purchase = "Big"
            elif "Small" in line:
                purchase = "Small"

    return period, purchase


# ===== MAIN LOOP =====
async def main():
    await client.start()
    print("🚀 Script Started...\n")

    await wait_next_minute()

    while True:
        for bot in bots:
            try:
                print(f"👉 Processing {bot}")

                # 🔥 Ensure connected
                if not client.is_connected():
                    print("🔄 Reconnecting...")
                    await client.connect()

                # ===== SEND ONLY ONCE =====
                await client.send_message(bot, "Get Prediction")
                print("📩 Sent: Get Prediction")

                await asyncio.sleep(4)

                msgs = await client.get_messages(bot, limit=5)

                found = False

                for msg in msgs:
                    text = msg.text

                    if text and "Period" in text:
                        period, purchase = extract_data(text)

                        if period and purchase:
                            print(f"✅ {bot} → {period} | {purchase}")
                            found = True
                            break

                if not found:
                    print("⚠️ No valid data found")

            except Exception as e:
                print(f"❌ Error in {bot}: {e}")

        print("⏳ Waiting next minute...\n")
        await wait_next_minute()


# ===== RUN =====
with client:
    client.loop.run_until_complete(main())