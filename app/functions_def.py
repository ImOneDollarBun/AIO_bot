# Получаем список кнопок из базы данных
def get_buttons_from_db():
    cursor.execute("SELECT name FROM buttons")
    buttons = [row[0] for row in cursor.fetchall()]
    return buttons


def convert_data(data, file_name):
    with open(file_name, 'wb') as file:
        file.write(data)
