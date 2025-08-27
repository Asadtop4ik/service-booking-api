USER_ERRORS = {
    2000: {
        "uz": "Noto'g'ri foydalanuvchi malumotlari",
        "ru": "Некорректные учетные данные пользователя",
        "status_code": 401,
    },
    2001: {
        "uz": "Foydalanuvchi o'zini o'zi o'chira olmaydi",
        "ru": "Пользователь не может удалить сам себя",
        "status_code": 400,
    },
    2002: {
        "uz": "Kiritilgan parolni tasdiqlang",
        "ru": "Подтвердите введенный пароль",
        "status_code": 400,
    },
    2003: {
        "uz": "Bu loginli foydalanuvchi bazada mavjud",
        "ru": "Пользователь с таким логином уже существует в базе данных",
        "status_code": 400,
    },
    2004: {
        "uz": "Autentifikatsiya maʼlumotlari taqdim etilmagan",
        "ru": "Информация для аутентификации не предоставлена",
        "status_code": 401,
    },
    2005: {
        "uz": "Login eki parol not'o'gri kiritildi.",
        "ru": "Логин и пароль были введены неверно.",
        "status_code": 401,
    },
    2006: {
        "en": "The Username must be set",
        "ru": "Имя пользователя должно быть установлено",
        "uz": "Foydalanuvchi nomi o'rnatilishi kerak",
        "status_code": 400,
    },
    2007: {
        "en": "Superuser must have is_staff=True.",
        "ru": "Суперпользователь должен иметь is_staff=True.",
        "uz": "Superuser is_staff=True bo'lishi kerak",
        "status_code": 400,
    },
    2008: {
        "en": "Superuser must have is_superuser=True.",
        "ru": "Суперпользователь должен иметь is_superuser=True.",
        "uz": "Superuser is_superuser=True bo'lishi kerak",
        "status_code": 400,
    },
}
