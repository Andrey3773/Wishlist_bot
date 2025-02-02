######################################################################################################################
########################################## ФАЙЛ ДЛЯ ХРАНЕНИЯ ЛЕКСИКОНА БОТА ##########################################
######################################################################################################################


##### ТЕКСТ НА КНОПКАХ КЛАВИАТУР #####
KEYBOARD_LEXICON: dict[str: dict[str: dict[str: str]]] = {
    'main_menu': {
        'my_list': {
            'ru': 'Мой вишлист',
            'eng': '',
            'callback': 'my_list',
        },
        'my_groups': {
            'ru': 'Мои группы',
            'eng': '',
            'callback': 'my_groups',
        },
        'new_group': {
            'ru': 'Создать группу',
            'eng': '',
            'callback': 'new_group',
        },
        'in_group': {
            'ru': 'Вступить в группу',
            'eng': '',
            'callback': 'in_group',
        },
        'feedback': {
            'ru': 'Оставить отзыв',
            'eng': '',
            'callback': 'feedback',
        },
        'main_menu_button': {
            'ru': 'В главное меню',
            'eng': '',
            'callback': 'main_menu_button',
        },
    },
    'in_my_list': {
        'new_gift': {
            'ru': 'Новая идея',
            'eng': '',
            'callback': 'new_gift'
        },
        'delete_gift': {
            'ru': 'Удалить идею',
            'eng': '',
            'callback': 'kill_gift'
        },
    },
    'admin': {
        'kill_feedback': {
            'ru': 'Удалить отзыв😈',
            'eng': '',
            'callback': 'kill_feedback'
        },
        'make_issue': {
            'ru': 'Сделать багом☠️',
            'eng': '',
            'callback': 'make_issue'
        },
        'see_issues': {
            'ru': 'Посмотреть проблемы',
            'eng': '',
            'callback': 'see_issues'
        },
    },
    'admin_lower': {
        'back': {
            'ru': 'Назад',
            'eng': '',
            'callback': 'back'
        }
    },
    'admin_in_issues': {
        'solve_issue': {
            'ru': 'Закрыть',
            'eng': '',
            'callback': 'solve_issue'
        },
        'not_solve_issue': {
            'ru': 'Открыть',
            'eng': '',
            'callback': 'not_solve_issue'
        },
        'kill_issue': {
            'ru': 'Удалить',
            'eng': '',
            'callback': 'kill_issue'
        },
    },
    'group_password': {
        'get_password': {
            'ru': 'Пароль',
            'eng': '',
            'callback': 'get_password'
        },
    },
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
    'user_already_has_gift': {
        'ru': 'У вас уже есть подарок с таким названием, попробуйте придумать что-то еще👉👈',
        'eng': ''
    },
    'correct_deleted_gift': {
        'ru': 'Окей👌\n'
              'Удалил.',
        'eng': ''
    },
    'correct_new_group': {
        'ru': 'Принято, пароль можно посмотреть в списке групп.',
        'eng': ''
    },
    'user_already_has_group': {
        'ru': 'Вы уже состоите в группе с таким названием, придумайте какое-нибудь другое👉👈',
        'eng': ''
    },
    'user_already_has_same_group': {
        'ru': 'К сожалению, у вы уже состоите в группе с таким же названием, как та, в которую хотите вступить(\n'
              'Переименуйте свою или попросите владельца группы переименовать ее.'
    },
    'correct_password': {
        'ru': 'Поздравляю, теперь вы в группе!',
        'eng': ''
    },
    'user_already_in_group': {
        'ru': 'У вас уже есть доступ к этой группе)',
        'eng': ''
    },
    'main_menu': {
        'ru': 'Итак, что вы хотите сделать?',
        'eng': ['', '']
    },
    'my_own_group': {
        'ru': 'Общедоступные',
        'eng': ''
    },
    'no_gifts': {
        'ru': 'У вас пока нет идей для подарка.',
        'eng': ''
    },
    'choose_group': {
        'ru': '\nВыберите группу.',
        'eng': ''
    },
    'choose_user': {
        'ru': '\nВыберите пользователя.',
        'eng': ''
    },
    'choose_gift': {
        'ru': '\nВыберите подарок.',
        'eng': ''
    },
    'fill_feedback': {
        'ru': 'Здесь вы можете передать обратную связь.\n'
              'Напишите о своих впечатлениях или обнаруженной проблеме в текстовом сообщении, '
              'а я передам всю информацию разработчикам🙏',
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
    'fill_group_name': {
        'ru': 'Отправьте мне название новой группы текстовым сообщением, а я взамен пришлю пароль для неё)',
        'eng': ''
    },
    'fill_password': {
        'ru': 'Попросите у владельца группы пароль для доступа к ней и пришлите мне его текстовым сообщением.',
        'eng': ''
    },
    'you_giver': {
        'ru': '✅',
        'eng': '✅'
    },
    'not_free_gift': {
        'ru': '❌',
        'eng': '❌'
    },
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
    },
    '/help': {
        'ru': 'Пока что просто заглушка для команды /help',
        'eng': ''
    },
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
    'no_issue': {
        'ru': 'Пока живем без проблем🤞',
        'eng': ''
    },
    'no_feedback': {
        'ru': 'Никто так и не соизволил оставить хоть какой-то отзыв😭😭😭',
        'eng': ''
    },
    'clothed_issue': {
        'ru': '✅',
        'eng': '✅'
    },
    'issue': {
        'ru': '❌',
        'eng': '❌'
    },
    'fill_kill_feedback': {
        'ru': '\nВведи цифру отзыва, который надо удалить',
        'eng': ''
    },
    'fill_make_issue': {
        'ru': '\nВведи цифру отзыва, который надо удалить',
        'eng': ''
    },
    'fill_see_issue': {
        'ru': '\nВведи цифру отзыва, который хочешь сделать своей проблемой😒',
        'eng': ''
    },
    'kill_feedback': {
        'ru': '\nКайфарики, отзыв удален💪',
        'eng': ''
    },
    'make_issue': {
        'ru': 'Теперь в твоей жизни на одну проблему больше🫠',
        'eng': ''
    },
    'solve_issue': {
        'ru': 'Теперь в твоей жизни на одну проблему меньше\n😎🎉🎉',
        'eng': ''
    },
    'choose_issue': {
        'ru': '\n\nНу выбирай...',
        'eng': ''
    },
    'kill_issue': {
        'ru': '\n\nПравильно, туда её!🖕',
        'eng': ''
    },
    'issues': {
        'ru': 'Вот твои проблемы:\n\n',
        'eng': ''
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
