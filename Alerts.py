from users_db_parser import UserDbReq
import Vk_bot
import Tg_bot
import logger


user_db = UserDbReq()


def send_alerts(a, mess):
    vk = []
    tg = []
    for id in a:
        info = user_db.get_user_info_by_global_id(id)
        vk_id = info['vk_id']
        tg_id = info['tg_id']
        if vk_id:
            vk.append(vk_id)
        if tg_id:
            tg.append(tg_id)
    logger.log("alerts", "alerts formed: vk_users: " + str(len(vk)) + " tg_users: " + str(len(tg)))
    logger.log("alerts", "alerts formed: vk_ids: " + str(vk) + " tg_ids: " + str(tg))
    Vk_bot.alerts(vk, mess)
    Tg_bot.alerts(tg, mess)
