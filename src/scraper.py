"""Telegram scraper with image download."""
import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='logs/scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CHANNELS = ['CheMed', 'lobelia_cosmetics', 'tikvah_pharma']

async def scrape_channel(client, channel_name):
    messages_data = []
    try:
        channel = await client.get_entity(channel_name)
        logging.info(f"Scraping {channel_name}")
        messages = await client.get_messages(channel, limit=100)
        
        for msg in messages:
            if msg.message:
                has_media = msg.media is not None
                data = {
                    'message_id': msg.id,
                    'channel_name': channel_name,
                    'message_date': msg.date.isoformat(),
                    'message_text': msg.message,
                    'views': msg.views if msg.views else 0,
                    'forwards': msg.forwards if msg.forwards else 0,
                    'has_media': has_media
                }
                messages_data.append(data)
                
                # Download image if present
                if has_media and msg.photo:
                    try:
                        img_dir = f'data/raw/images/{channel_name}'
                        os.makedirs(img_dir, exist_ok=True)
                        img_path = f'{img_dir}/{msg.id}.jpg'
                        await client.download_media(msg.media, img_path)
                        logging.info(f"Downloaded image: {img_path}")
                    except Exception as e:
                        logging.error(f"Image download failed: {e}")
        
        today = datetime.now().strftime('%Y-%m-%d')
        os.makedirs(f'data/raw/telegram_messages/{today}', exist_ok=True)
        filepath = f'data/raw/telegram_messages/{today}/{channel_name}.json'
        with open(filepath, 'w') as f:
            json.dump(messages_data, f, indent=2)
        
        logging.info(f"Saved {len(messages_data)} messages from {channel_name}")
        print(f"Scraped {len(messages_data)} messages from {channel_name}")
    except Exception as e:
        logging.error(f"Error scraping {channel_name}: {e}")
        print(f"Error: {channel_name} - {e}")

async def main():
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    if not api_id or api_id == 'your_api_id':
        print("Please set API_ID and API_HASH in .env file")
        return
    client = TelegramClient('session', int(api_id), api_hash)
    await client.start()
    for channel in CHANNELS:
        await scrape_channel(client, channel)
    await client.disconnect()
    print("Done!")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
