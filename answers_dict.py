dates = {["февраль", "февраля"]:["1"],
         ["январь", "января"]:["2"],
         ["март", "марта"]:["3"],
         ["апрель", "апреля"]:["4"],
         ["май", "мая"]:["5"],
         ["июнь", "июня"]:["6"],
         ["июль", "июля"]:["7"],
         ["август", "августа"]:["8"],
         ["сентябрь", "сентября"]:["9"],
         ["октябрь", "октября"]:["10"],
         ["ноябрь", "ноября"]:["11"],
         ["декабрь", "декабря"]:["12"]}



answers = {["/start"]:["Привет, я ЭлжурБот. Чтобы узнать мои команды, напиши: 'Что ты умеешь?' или 'Команды' или воспользуйя кнопками."],
           ["что", "умеешь", "команды",]:["Вот что я могу:\n"
                                          "Регистация -- советую начать с этой команды для дальнейшей работы со мной.\n"
                                          "Мой аккаунт/Мой акк -- расскажу, что знаю о тебе. Можешь изменить информацию о себе.\n"
                                          "Расписание -- я скину расписание на текущую неделю.\n"
                                          "Расписание на *дата* -- я скину расписание на указанную дату. Так же можешь написать: 'Расписание на неделю *дата*' и произойдет немыслимое!\n"
                                          "Отмена или Замена -- сообщить, что какой-то урок отменили/заменили.\n"
                                          "Комментарий/Коммент -- расскать, что думаешь о прошедшем уроке.\n"
                                          "Поддержка -- задать вопрос или сообщить об ошибке моим СОЗДАТЕЛЯМ.\n"
                                          "Пока что все. Я обзятельно тебе скажу, как только научусь чему-то новому!)"],
           ["регистрация", "зарегистрироваться"]:["Ура! Новый пользователь! Как мне тебя называть?",
                                                  #"Придумай пароль:",
                                                  #"Повтори пароль еще раз:"
                                                  "В каком классе учишься?",
                                                  "Хорошо, с необходимым закончили. Захочешь изменить или добавить данные -- напиши Мой аккаунт."],
           ["мой аккаунт", "мой акк"]:["Вот что я знаю о тебе:", "Данные о тебе:", "Твои данные:"],
           ["расписание"]:["Лови", "Скинул", "Вот"],
           ["расписание", "на"]:["Лови", "Скинул", "Вот"],
           ["отмена"]:["Какой урок отменен?", "Какого урока не будет?", "Что отменили?"],
           ["замена"]:["Какой урок заменен?", "Что заменили?"],
           ["комментарий", "коментарий", "коммент", "комент"]:["Какой урок хочешь прокомментировать?"],
           ["поддержка"]:["Оу, надеюсь, что все в порядке) Твое сообщение поддержке:"]}