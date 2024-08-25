import bittensor
from telegram._bot import Bot
import asyncio
from telegram.request import HTTPXRequest
import json

def read_json_from_file(file_path):
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id='-4245052265', text=message, pool_timeout=100)
    except Exception as e:
        print(f"Error sending message: {e}")
        pass

config = read_json_from_file('config.json')
trequest = HTTPXRequest(connection_pool_size=20)
bot = Bot(token='7281318901:AAGOQr8SRDCd94LrOtdjObGqjU0YSQVBwQM', request=trequest)
subtensor = bittensor.subtensor(network="local")

hotkey_states = [False] * len(config["hotkeys"])

while True:
    for i in range(0,len(config["hotkeys"])):
        print(f'{config["coldkey"]} - {config["hotkeys"][i]} registering...')
        wallet = bittensor.wallet(name=config["coldkey"],hotkey=config["hotkeys"][i])
        try:
            if subtensor.burned_register( wallet = wallet, netuid = config["netuid"],wait_for_finalization=False ):
                if hotkey_states[i]:
                    continue
                hotkey_states[i] = True
                message = f'{config["coldkey"]} - {config["hotkeys"][i]} registered successfully on subnet {config["netuid"]}'
                print(message)
                asyncio.run(send_telegram_message(message=message))
            else:
                print(f'{config["coldkey"]} - {config["hotkeys"][i]} registration failed')
        except Exception as e:
            print(f'{config["coldkey"]} - {config["hotkeys"][i]} registration failed: {e}')