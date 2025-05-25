def get_recommendation_by_profile(profile: dict) -> str:
    """
    Примитивный маппер, возвращающий метод преподавания на основе профиля.
    В реальной версии — можно заменить на дерево решений или правила.
    """
    discipline = profile.get("discipline_type")
    engagement = profile.get("engagement_level")
    attendance = profile.get("attendance")
    motivation = profile.get("motivation", 0)
    digital_literacy = profile.get("digital_literacy_students")

    if discipline == "Теоретическая":
        if engagement == "Высокая":
            if attendance == "≥ 75%":
                if profile.get("group_activity"):
                    return "Лекции + семинары с элементами дебатов"
                elif motivation >= 4.0:
                    return "Флип-класс + ролевые дискуссии"
                else:
                    return "Мини-лекции + блиц-опросы"
            else:
                if digital_literacy == "Высокая":
                    return "Онлайн-курсы + практикумы на платформе"
                else:
                    return "Классические лекции + бумажные тесты"
        else:
            if profile.get("average_score", 0) <= 4.0:
                if profile.get("anxiety_level", 0) >= 3.5:
                    return "Индивидуальные занятия + менторство"
                elif profile.get("teacher_changed_recently"):
                    return "Диагностическое тестирование + настройка темпа"
                else:
                    return "Проясняющее преподавание + регулярная обратная связь"
            else:
                return "Кейс-стади + самооценка знаний"

    elif discipline == "Практико-ориентированная":
        format_ = profile.get("format")
        if format_ == "Очно":
            if profile.get("equipment_available"):
                if profile.get("course_experience"):
                    return "Проектная работа + peer-review"
                elif profile.get("assistant_present"):
                    return "Наставническая модель + парная работа"
                else:
                    return "Поддерживаемая мастерская (scaffolded lab)"
            else:
                if profile.get("group_interaction") == "Высокий":
                    return "Деловая игра / имитация"
                else:
                    return "Индивидуальные задания + обсуждение"
        elif format_ == "Онлайн":
            if profile.get("lms_activity", 0) >= 60:
                if motivation >= 4.0:
                    return "Проектное обучение с наставником + форум"
                else:
                    return "Самообучение + периодические консультации"
            else:
                if profile.get("digital_literacy_teacher") == "Высокая":
                    return "Модульное обучение + визуальные инструкции"
                else:
                    return "PDF-материалы + Zoom-консультации"

    elif discipline == "Смешанная":
        avg = profile.get("average_score", 0)
        if avg > 4.5:
            return "Флип-класс + мозговые штурмы"
        else:
            if profile.get("tasks_completed_percent", 0) >= 70:
                if profile.get("project_used"):
                    return "Спиральная модель обучения"
                elif profile.get("group_working") is True:
                    return "Групповой исследовательский проект"
                else:
                    return "Индивидуальные маршруты + аналитические задания"
            else:
                if motivation < 3.5:
                    return "Игровая механика (бейджи, уровни)"
                else:
                    return "Адаптивные онлайн-курсы с выбором траектории"

    return "Метод не определён — недостаточно данных"
