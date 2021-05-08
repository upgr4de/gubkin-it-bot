from aiogram.utils.callback_data import CallbackData


# pl - poll, nm - name, gr - group -- for economy of bytes (limit 64b)
poll_callback = CallbackData('pl', 'nm', 'gr')
