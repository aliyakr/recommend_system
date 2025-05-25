from recommendations.method_mapper import get_recommendation_by_profile

def evaluate_profile(profile: dict) -> str:
    """
    Принимает словарь с параметрами профиля преподавания
    и возвращает название рекомендованного метода.
    """
    # Пример: profile = {
    #     "discipline_type": "Теоретическая",
    #     "engagement_level": "Высокая",
    #     "attendance": "≥ 75%",
    #     "group_activity": True,
    #     "motivation": 4.3,
    #     "digital_literacy_students": "Высокая",
    #     ...
    # }

    # Здесь могла бы быть логика дерева решений (жёстко зашитая или на основе правил)
    # Для простоты — перенаправим в mapper

    method = get_recommendation_by_profile(profile)
    return method
