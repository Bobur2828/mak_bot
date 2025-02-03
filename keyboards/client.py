from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
class CustomKeyboard:
    def __init__(self, buttons):
        self.buttons = buttons


menu_buttons_uzb = [
    [KeyboardButton(text="🎬 Kinolar")],
    # [KeyboardButton(text="📥 Video yuklash")],

    [ KeyboardButton(text="🤝 Hamkorlik")],
]
menu = ReplyKeyboardMarkup(keyboard=menu_buttons_uzb, resize_keyboard=True,is_persistent=True)


kino_buttons1 = [
    [KeyboardButton(text="🔍 KOD bilan izlash"), KeyboardButton(text="🎲 Tasodifiy kino")],
    [KeyboardButton(text="📊 TOP Kinolar 🎬"),KeyboardButton(text="🏠 Bosh menu")],
    
]

kino_btn = ReplyKeyboardMarkup(keyboard=kino_buttons1, resize_keyboard=True, is_persistent=True)

channel_buttons11 = [
    [KeyboardButton(text="Menyular ochilishi uchun obunani tasdiqlang")],
    
]

chan_btn = ReplyKeyboardMarkup(keyboard=channel_buttons11, resize_keyboard=True, is_persistent=True)


back_btn = [
    [KeyboardButton(text="↩️ Ortga")],  # Ortga tugmasiga ↩️ emoji qo'shildi
]

# ReplyKeyboardMarkup obyektini yaratish
back = ReplyKeyboardMarkup(keyboard=back_btn, resize_keyboard=True, is_persistent=True)
# KeyboardButton(text="ℹ️ Biz haqimizda"),