




def is_end(driver):
    """Проверяет, находится ли на последней странице курса"""

    try:


        return True
    except Exception as e:
        print("Ошибка:", e)
        return False