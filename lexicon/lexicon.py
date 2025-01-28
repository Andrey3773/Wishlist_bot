######################################################################################################################
########################################## ФАЙЛ ДЛЯ ХРАНЕНИЯ ЛЕКСИКОНА БОТА ##########################################
######################################################################################################################


##### ТЕКСТ НА КНОПКАХ КЛАВИАТУР #####
KEYBOARD_LEXICON: dict[str: dict[str: str|list]] = {
    'main_menu_button': {
        'ru': 'В главное меню',
        'eng': '',
        'callback': 'main_menu_button'
    },
    'main_menu': {
        'ru': ['Мой вишлист', 'Мои группы', 'Создать группу', 'Вступить в группу', 'Оставить отзыв'],
        'eng': [],
        'callback': ['my_list', 'my_groups', 'new_group', 'in_group', 'feedback']
    },
    'new_gift': {
        'ru': 'Новая идея',
        'eng': '',
        'callback': 'new_gift'
    },
    'delete_gift': {
        'ru': 'Удалить идею',
        'eng': '',
        'callback': 'kill_gift'
    }
}


##### РЕПЛИКИ БОТА ПРИ ВЫЗОВЕ КОМАНД #####
LEXICON_COMMAND: dict[str: dict[str: str|list]] = {
    '/start': {
        'ru': ['Привет, ',
              '!\nДля регистрации введите имя, по которому ваши друзья смогут вас узнать.\n'
              'Пожалуйста, используйте только буквы👉👈\n\n'
              '<span class="tg-spoiler">Ну лаааааадно, можно ещё эмодзи)</span>'],
        'eng': ''
    },
    '/start_again': {
        'ru': 'Вы уже зарегистрированы.\n'
              'Чтобы посмотреть информацию о боте, вызовите команду /help.\n\n'
              '<i>можно просто тыкнуть на нее в сообщении</i>',
        'eng': ''
    }
}


##### ОСНОВНОЙ ЛЕКСИКОН БОТА #####
LEXICON: dict[str: dict[str: str|list]] = {
    'correct_registration': {
        'ru': ['Поздравляю, ',
              '!\nВы успешно зарегистрированы✅'],
        'eng': ['', '']
    },
    'correct_feedback': {
        'ru': 'Спасибо за ваш отзыв!🫶',
        'eng': ['', '']
    },
    'correct_new_gift_idea': {
        'ru': 'Отлично!\n'
              'Теперь остается лишь ждать)',
        'eng': ['', '']
    },
    'main_menu': {
        'ru': 'Итак, что вы хотите сделать?',
        'eng': ['', '']
    },
    'help': {
        'ru': 'Пока что просто заглушка для команды /help',
        'eng': ''
    },
    'my_own_group': {
        'ru': 'Общедоступные',
        'eng': ''
    },
    'no_gifts': {
        'ru': 'У вас пока нет подарков.',
        'eng': ''
    },
    'fill_feedback': {
        'ru': 'Здесь вы можете передать обратную связь.\n'
              'Напишите о своих впечатлениях или обнаруженной проблеме в текстовом сообщении, '
              'а я передам всю информацию разработчикам.🙏\n\n'
              'Если это сообщение исчезнет -- не переживайте, отзыв все равно будет принят.',
        'eng': ''
    },
    'fill_new_gift': {
        'ru': 'Отправьте идею для подарка вам текстовым сообщением, я передам его вашим друзьям.\n'
              '*Эта идея будет доступна во всех ваших группах.',
        'eng': ''
    },
    'fill_deleted_gift': {
        'ru': 'Пожалуйста, напишите название идеи, которую вы хотите удалить.\n'
              'Очень важно написать ее именно так, как это указано в списке. Лучше скопировать из сообщения выше.\n\n'
              '<span class="tg-spoiler">Это обязательно пофиксят позднее, но пока что я умею только так((</span>',
        'eng': ''
    },
    'correct_deleted_gift': {
        'ru': 'Окей👌\n'
              'Удалил.',
        'eng': ''
    }
}


##### ЛЕКСИКОН БОТА ПРИ ОБЩЕНИИ С АДМИНАМИ #####
LEXICON_ADMIN: dict[str: dict[str: str|list]] = {
    '/start': {
        'ru': 'Приветствую, администратор!\n'
              'Регистрация все равно нужна...',
        'eng': ''
    },
    '/start_again': {
        'ru': 'Ну админу-то зачем пытаться ещё раз зарегистрироваться😭😭',
        'eng': ''
    },
    '/help': {
        'ru': 'Это help для администраторов',
        'eng': ''
    },
    'clothed_trouble': {
        'ru': '✅',
        'eng': '✅'
    },
    'trouble': {
        'ru': '❌',
        'eng': '❌'
    }
}


##### РЕАКЦИИ БОТА НА ПЛОХОЕ ПОВЕДЕНИЕ #####
WRONG_LEXICON: dict[str: dict[str: str|list]] = {
    'incorrect_registration': {
            'ru': 'Боюсь, вы ввели некорректное имя пользователя.\n'
                  'Напоминаю, необходимо использовать только буквы и эмодзи.',
            'eng': ''
    },
    'incorrect_feedback': {
        'ru': 'К сожалению, я могу передавать разработчикам только текстовые сообщения👉👈',
        'eng': ''
    },
    'other': {
        'ru': 'Ну я не понимаю, что ты хочешь...\n'
              'ХВАТИТЬ😭😭😭',
        'eng': ['', '']
    }
}
