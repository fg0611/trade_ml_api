import asyncio
from telegram import Bot

# Step 2: Send Chart via Telegram
async def send_chart_via_telegram(chart_path, bot_token, chat_id):
    # Create a Bot instance
    bot = Bot(token=bot_token)   
    # Send the image
    with open(chart_path, 'rb') as chart_file:
        await bot.send_photo(chat_id=chat_id, photo=chart_file)