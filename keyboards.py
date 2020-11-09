from messages import Messages
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btn_add = KeyboardButton(Messages.add)
btn_delete = KeyboardButton(Messages.delete)
btn_getsubscribed = KeyboardButton(Messages.get_subscribed_list)
btn_refresh = KeyboardButton(Messages.refresh)
btn_help = KeyboardButton(Messages.commands)
btn_undo_deletion = KeyboardButton(Messages.undo_delete)
btn_undo_addition = KeyboardButton(Messages.undo_accept)

main_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add, btn_delete).add(
    btn_getsubscribed).add(btn_refresh).add(btn_help)

undo_addition_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_undo_addition)
undo_delition_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_undo_deletion)