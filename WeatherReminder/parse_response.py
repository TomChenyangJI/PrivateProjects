
def get_weather_info(data):
    weather = data.get('weather')
    description = weather[0].get("description")
    main = weather[0].get('main')

    temperate = data.get('main')
    cur_temp = temperate.get('temp')
    feels_like = temperate.get('feels_like')
    temp_min = temperate.get('temp_min')
    temp_max = temperate.get('temp_max')

    details = f"Description:\n\t{description.capitalize()}\n\nMain:\n\t{main}\n\n" \
              f"Temperature:\n\tFeels like:{feels_like}\n\tCur:{cur_temp}\tMin:{temp_min}\tMax:{temp_max}"

    return details
