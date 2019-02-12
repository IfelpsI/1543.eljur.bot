import logger
import lessons_db_manip as ldm
import schedule_parser as sp
import answers_dict as ad


def update_schedule():
    schedule = sp.get_current_schedule()
    ldm.add_schedules(schedule)
    return


def get_schedule(text):
    schedule = ldm.get_schedule(get_class_name_from_text(text.upper()))
    answer_string = ""
    for day_name, day_schedule in schedule.items():
        answer_string += str(day_name.title()) + ':\n'
        for lesson_num in day_schedule.keys():
            answer_string += str(lesson_num) + '. ' + str(day_schedule[lesson_num][1]) + '\n'
    return answer_string


def get_class_name_from_text(text):
    class_name = text.split()[1]
    return class_name


def generate_return(text):
    return {"text": text, "buttons": None}


def parse_message_from_user(scr, user_id, text):
    logger.log("user_req", "process request")
    text = text.strip().lower()
    try:
        for key, value in ad.quest.items():
            if key in text:
                needed_function = key_words_to_function[value]
                answer_from_function = needed_function(text)
                return generate_return(answer_from_function)
                # generate_return(ldm.get_schedule())
        logger.log("user_req", f"Запрос не найден. Запрос: {text}")
        return {"text": "Запроса не найдено :( ", "buttons": None}

    except Exception as err:
        logger.log("user_req", f"Processing error: {err}\n Запрос: {text}")
        return {"text": "Видно, не судьба :( ", "buttons": None}


key_words_to_function = {"schedule": get_schedule}
# update_schedule()
parse_message_from_user("tg", "1", "УМРИ")

# ya LOH_KABAKOV
