import Tg_bot
import Vk_bot
import config
import logger
from users_db_parser import UserDbReq

flag_on_PC = config.params['flag_on_PC']

if flag_on_PC:
    user_db = UserDbReq()
else:
    user_db = UserDbReq("1543.eljur.bot/1543.eljur.bot.db")


def send_alerts(a, mess):
    vk = []
    tg = []
    for u_id in a:
        info = user_db.get_user_info_by_global_id(u_id)
        vk_id = info['vk_id']
        tg_id = info['tg_id']
        if vk_id:
            vk.append(vk_id)
        if tg_id:
            tg.append(tg_id)
    logger.log("alerts_save", "alerts formed: vk_users: " + str(len(vk)) + " tg_users: " + str(len(tg)))
    logger.log("alerts_save", "alerts formed: vk_ids: " + str(vk) + " tg_ids: " + str(tg))
    Vk_bot.alerts(vk, mess)
    Tg_bot.alerts(tg, mess)
