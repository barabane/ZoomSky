def today_template(data):
    return f"""
    📍<b>Город:</b> {data['location']['name']}\b
⌚️<b>Дата и время:</b> {data['location']['localtime']}
➖➖➖➖➖➖➖➖➖➖➖➖
⛅️Погода: <b>{data['current']['condition']['text']}</b>
🌡 Температура: {data['current']['temp_c']} °C
🙆‍♂️ Ощущается как: {data['current']['feelslike_c']} °C
🌬 Ветер: {data['current']['wind_mph']}\b м/с
👁 Видимость: {data['current']['vis_km']} км
"""


def forecast_template(data):
    return f"""
    ⌚️<b>Дата: </b> {data['date']}
➖➖➖➖➖➖➖➖➖➖➖➖
⛅️Погода: <b>{data['day']['condition']['text']}</b>
🔥Макс. температура: {data['day']['maxtemp_c']} °C
🧊Мин. температура: {data['day']['mintemp_c']} °C
🌄Рассвет: {data['astro']['sunrise']}
🌅Закат: {data['astro']['sunset']}
"""
