from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


#######################################################################################
#                              КНОПКИ "ГЛАВНОГО МЕНЮ"	                              #
#######################################################################################


btn_get_product_info = KeyboardButton("Получить информацию по товару✳️")
btn_get_db_info = KeyboardButton("Получить информацию из БД⏺")
kb_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btn_get_product_info).add(btn_get_db_info)


#######################################################################################
#                              ИНЛАЙН  КНОПКИ                                         #
#######################################################################################


inl_btn_subscribe_to_notifications = InlineKeyboardButton(text = "Подписаться на уведомления✅", callback_data = "subscribe_to_notifications")
inl_menu_subscribe_to_notifications = InlineKeyboardMarkup(row_width=1).insert(inl_btn_subscribe_to_notifications)
