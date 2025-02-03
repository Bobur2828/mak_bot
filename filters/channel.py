from typing import Any
from aiogram.types import Message
from aiogram.filters import Filter
from aiogram import Bot
from config import CHANNEL_ID

ROLES = ['member', 'administrator', 'creator']
class CheckSubChannel(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        for channel in CHANNEL_ID:
            user_status = await bot.get_chat_member(channel, message.from_user.id)
        if user_status.status  in ROLES:
            return False        
        else:
            return True

