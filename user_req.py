import logger
from lessons_db_manip import LessonDbReq
import answers_dict as ad
from users_db_parser import UserDbReq
from datetime import datetime, timedelta
import eljur_api as ea
import config


lesson_db = LessonDbReq()
user_db = UserDbReq()

preset = {"devkey": config.secret['eljurapi']['devkey'], "vendor": "1543",
              "password": config.secret['eljurapi']['password'],
              "login": config.secret['eljurapi']['login']}
student = ea.Student(**preset)


def update_schedule():
    lesson_db.add_schedules()
    return


def cur_date(add=0):
    return (datetime.today() + timedelta(days=add)).strftime('%Y%m%d')


def get_schedule(scr, user_id, text):
    logger.log("user_req", f"getting schedule in {text}")

    class_name = get_class_name_from_text(text.upper())
    if not lesson_db.get_schedule(class_name, cur_date(1)):
        lesson_db.add_schedule(class_name, cur_date(1))

    schedule = {"Сегодня": lesson_db.get_schedule(class_name, cur_date()),
                "Завтра": lesson_db.get_schedule(class_name, cur_date(1))}

    logger.log("user_req", f"current_user_schedule {schedule}")

    answer_string = ""
    for day_date, day_schedule in schedule.items():
        answer_string += f"{day_date.title()}:\n"
        for lesson_num, lesson in day_schedule.items():

            for it in range(len(lesson)):
                if lesson[it]['comment'] is not None:
                    lesson[it] = f"{lesson[it]['name']} ({lesson[it]['comment']})"
                else:
                    lesson[it] = f"{lesson[it]['name']}"

            answer_string += f"{lesson_num}. {'/'.join(lesson)}.\n"
    return answer_string


def register_new_user(scr, user_id, text):    # регистрация login name surname parallel
    text = text.split()
    if len(text) >= 5:
        login = text[1]
        name = text[2]
        surname = text[3]
        parallel = text[4]
        return user_db.add_user(name, surname, user_id)

    else:
        return "Чтобы зарегистрироваться вводите (без кавычек):\n регистрация \"твой логин\" " \
               "\"твое имя\" \"твоя фамилия\" \"твой класс\""


def get_class_name_from_text(text):
    class_name = text.split()[1]
    return class_name


def get_day_and_lesson_and_class_name_from_text(text):
    day = text.split()[3].capitalize()
    lesson = text.split()[1].capitalize()
    class_name = text.split()[5]
    return day, lesson, class_name


def make_date(n):
    s = datetime.isoformat(n)
    s = s.split(sep='T')
    s = s[0]
    s = s.split(sep='-')
    s = s[0] + s[1] + s[2]
    return s


def get_day_and_class_name_from_text(text):
    t = text.split()
    for i in range(len(t)):
        if t[i] in ['дз', 'домашнее', 'задание', 'домашка']:
            continue
        else:
            ind = i
            break
    else:
        return ['', '']
    now = datetime.now()
    today = make_date(now)
    tomorrow = make_date(datetime.fromordinal(datetime.toordinal(now) + 1))
    yesterday = make_date(datetime.fromordinal(datetime.toordinal(now) - 1))
    w = now.weekday()
    mon = datetime.fromordinal(datetime.toordinal(now) - w)
    sun = datetime.fromordinal(datetime.toordinal(now) - w + 5)
    monday = make_date(mon)
    sunday = make_date(sun)
    week = monday + '-' + sunday
    try:
        class_name = t[ind]
        day = t[ind + 1]
    except Exception:
        return [today, t[ind]]
    class_name = class_name.upper()
    if day == 'сегодня':
        day = today
    elif day == 'завтра':
        day = tomorrow
    elif day == 'вчера':
        day = yesterday
    elif day == 'неделя':
        day = week
    return [day, class_name]


def generate_return(text):
    return {"text": text, "buttons": None}


def send_acc_information(src, user_id, text):
    logger.log("user_req", "request for acc data")
    ans_mes = user_db.get_user_info(user_id)
    if ans_mes is None:
        logger.log("user_req", "user " + str(user_id) + " is not in the database")
        answer_message = "К сожалению вас пока нет в нашей базе данных"
    else:
        answer_message = f"Логин: {ans_mes['login']}\nИмя: {ans_mes['first_name']}\nФамилия: {ans_mes['last_name']}\n" \
            f"Класс: {ans_mes['class']}\n vk_id: {ans_mes['vk_id']}"
    return answer_message


def cancel_lesson(src, user_id, text):
    logger.log("user_req", "cancelling a lesson")
    day, lesson, class_name = get_day_and_lesson_and_class_name_from_text(text)
    lesson_db.make_cancel(class_name, day, lesson)
    return "Урок отменен"


def comment_lesson(src, user_id, text):      # комментарий lesson в day у class_name comment
    logger.log("user_req", "commenting a lesson")
    day, lesson, class_name = get_day_and_lesson_and_class_name_from_text(text)
    comment = " ".join(text.split()[6:])
    return lesson_db.get_comment(class_name, day, lesson, comment)


def replace_lesson(src, user_id, text):      # замена lesson в day у class_name another_lesson
    logger.log("user_req", "replacing a lesson")
    day, lesson, class_name = get_day_and_lesson_and_class_name_from_text(text)
    another_lesson = text.split()[6]
    return lesson_db.get_replacement(class_name, day, lesson, another_lesson)


def get_hometask(scr, user_id, text):
    logger.log("user_req", "getting hometask")
    day, class_name = get_day_and_class_name_from_text(text)
    r = student.get_hometask(class_name, day)
    logger.log("user_req", "response get: " + str(r))
    if not r:
        return "Вы неправильно ввели класс или дату, или на этот(и) день(и) расписания в eljur нет."
    d = r['days']
    ans = ""
    for info in d.values():
        ans += '\n'
        ans += ("--<" + info['title'] + '>--' + '\n')
        for lesson in info['items']:
            ans += lesson['name']
            if 'grp' in lesson.keys():
                ans += (" группа " + lesson['grp'] + '\n')
            else:
                ans += '\n'
            ans += (lesson['homework']['1']['value'] + '\n')
            try:
                ans += (lesson['files']['file'][0]['link'] + '\n')
            except Exception:
                pass
            ans += "-" * 20 + "\n"
    return ans


def user_reg0(src, user_id, text):
    if src == "vk":
        user_db.update_user({"status": "reg1"}, vk_id=user_id)
    if src == "tg":
        user_db.update_user({"status": "reg1"}, tg_id=user_id)

    return {"text": "Выберите класс.\nЕсли хотите продолжить без введения класса, нажмите \"Отмена\"",
            "buttons": [[5, 6, 7, 8], [9, 10, 11], ["Отмена"]]}


def user_reg1(src, user_id, text):
    if text == "отмена":
        user_db.update_user({"class": "null", "status": "reg0"}, user_id)
        return user_reg0(src, user_id, text)
    if text in ["5", "6", "7", "8", "9", "10", "11"]:
        user_db.update_user({"class": text, "status": "reg2"}, user_id)
        return {"text": "Выберите букву класса.\nЕсли хотите продолжить без введения класса, нажмите \"Отмена\"",
                "buttons": [["А", "Б", "В", "Г"], ["Отмена"]]}
    return {"text": "Выберите класс.\nЕсли хотите продолжить без введения класса, нажмите \"Отмена\"",
            "buttons": [[5, 6, 7, 8], [9, 10, 11], ["Отмена"]]}


def user_reg2(src, user_id, text):
    if text == "отмена":
        user_db.update_user({"class": "null", "status": "reg0"}, user_id)
        return user_reg0(src, user_id, text)
    if text in ["а", "б", "в", "г"]:
        info = user_db.get_user_info(user_id)
        user_db.update_user({"class": info['class'] + text, "status": "waiting"}, user_id)
        return {"text": "Теперь вы можете узнавать расписание или дз, нажимая лишь на одну кнопку. \n"
                        "Вы можете сбросить класс, нажав \"разлогиниться\".",
                "buttons": waiting_buttons}
    return {"text": "Выберите букву класса.\nЕсли хотите продолжить без введения класса, нажмите \"Отмена\"",
            "buttons": [["А", "Б", "В", "Г"], ["Отмена"]]}


def user_sch0(src, user_id, text):
    info = user_db.get_user_info(user_id)
    user_db.update_user({"class": info['class'], "status": "rasp1"}, user_id)
    return {"text": "Выберите время",
            "buttons": [["Сегодня"], ["Завтра"], ["Неделя"], ["Отмена"]]}


def send_commands(src, user_id, text):
    logger.log("user_req", "commands request")
    ans = "Из доступных команд у меня пока есть: расписание <класс вида: число буква>, мой аккаунт"
    return ans


def fast_schedule(src, user_id, text):
    info = user_db.get_user_info(user_id)
    if info['class'] == 'null':
        user_db.update_user({"class": "null", "status": "reg0"}, user_id)
        return user_reg0(src, user_id, text)
    if text == "отмена":
        user_db.update_user({"class": info['class'], "status": "waiting"}, user_id)
        return {"text": "Вы в главном меню:",
                "buttons": waiting_buttons}
    user_db.update_user({"class": info['class'], "status": "waiting"}, user_id)
    return {"text": get_schedule(src, user_id, "null " + info["class"]),
            "buttons": waiting_buttons}


def fast_hometask(src, user_id, text):
    info = user_db.get_user_info(user_id)
    return {"text": get_hometask(src, user_id, info["class"] + " неделя"),
            "buttons": waiting_buttons}


def cancel_waiting(src, user_id, text):
    user_db.update_user({"class": "null", "status": "reg0"}, user_id)
    return user_reg0(src, user_id, text)


def parse_message_from_user(scr, user_id, text, name):
    logger.log("user_req", "process request")
    text = text.strip().lower()

    if user_db.get_user_info(user_id) is None:
        user_db.add_user(name['first_name'], name['last_name'], user_id)

    logger.log("user_req", "requesting info")
    info = user_db.get_user_info(user_id)
    if info['status'] is None:
        user_db.update_user({"status": "reg0"}, user_id)

    if info['status'] != 'waiting':
        function = status_to_function[info['status']]
        return function(scr, user_id, text)

    info = user_db.get_user_info(user_id)
    if info['status'] == 'waiting' and info['class'].lower() is not "null" and text in fast_msg_to_function.keys():
        function = fast_msg_to_function[text]
        return function(scr, user_id, text)

    try:
        for key, value in ad.quest.items():
            if key in text:
                needed_function = key_words_to_function[value]
                answer_from_function = needed_function(scr, user_id, text)

                return generate_return(answer_from_function)
        logger.log("user_req", f"Запрос не найден. Запрос: {text}")
        return {"text": "Запроса не найдено :( ", "buttons": None}

    except Exception as err:
        logger.log("user_req", f"Processing error: {err}\n Запрос: {text}")
        return {"text": "Видно не судьба :( ", "buttons": None}


key_words_to_function = {"schedule": get_schedule,
                         "registration": register_new_user,
                         "account": send_acc_information,
                         "cancel": cancel_lesson,
                         "replacement": replace_lesson,
                         "comment": comment_lesson,
                         # "support": support_message,
                         "commands": send_commands,
                         "hometask": get_hometask
                         }


status_to_function = {
    "reg0": user_reg0,
    "reg1": user_reg1,
    "reg2": user_reg2,
}


fast_msg_to_function = {
    "расписание": fast_schedule,
    "дз": fast_hometask,
    "разлогиниться": cancel_waiting
}


waiting_buttons = [["расписание"], ["дз"], ["разлогиниться"]]


if __name__ == '__main__':
    pass
