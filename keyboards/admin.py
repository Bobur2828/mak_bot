from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
class CustomKeyboard:
    def __init__(self, buttons):
        self.buttons = buttons


menu_buttons_uzb = [
    [ KeyboardButton(text="Kinolar"), KeyboardButton(text="Foydalanuvchilar soni")],
    [ KeyboardButton(text="Kanallar"), KeyboardButton(text="Adminlar")],
    [ KeyboardButton(text="Reklama"), KeyboardButton(text="Kanal ID sini aniqlash")],

]
menu = ReplyKeyboardMarkup(keyboard=menu_buttons_uzb, resize_keyboard=True,is_persistent=True)


admin_buttons = [
    [ KeyboardButton(text="Admin qo'shish"), KeyboardButton(text="Admin o'chirish")],
    [ KeyboardButton(text="Adminlar ro'yhati"), KeyboardButton(text="Ortga")],


]
admin_btn = ReplyKeyboardMarkup(keyboard=admin_buttons, resize_keyboard=True,is_persistent=True)


menu_buttons = [
    [ KeyboardButton(text="Bosh menu")],


]
menu_btn = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True,is_persistent=True)

chan_btn = [
    [ KeyboardButton(text="Kanal qo'shish"), KeyboardButton(text="Kanal o'chirish")],
    [ KeyboardButton(text="Kanallar ro'yhati"), KeyboardButton(text="Ortga")],


]
channel_btn = ReplyKeyboardMarkup(keyboard=chan_btn, resize_keyboard=True,is_persistent=True)



confirm_buttons = [
    [ KeyboardButton(text="✅ Tasdiqlash")],


]
confirm = ReplyKeyboardMarkup(keyboard=confirm_buttons, resize_keyboard=True,is_persistent=True)


kin_btn = [
    [ KeyboardButton(text="Kino Yuklash"), KeyboardButton(text="Kino o'chirish")],
    [ KeyboardButton(text="Kinolar ro'yhati"), KeyboardButton(text="Ortga")],


]
kino_btn = ReplyKeyboardMarkup(keyboard=kin_btn, resize_keyboard=True,is_persistent=True)