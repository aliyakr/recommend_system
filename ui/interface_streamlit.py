import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

import streamlit as st
import json
from logic.decision_engine import evaluate_profile
from recommendations.descriptions import get_method_description

st.set_page_config(page_title="Система рекомендаций", page_icon="🎓")

# Загрузка пользователей
def load_users():
    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

USERS = load_users()

# Инициализация состояний
defaults = {
    "step": 0,
    "role": None,
    "group_id": "",
    "user_key": "",
    "profile": {},
    "student_answers": {},
    "go_next": False,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Контейнер для переключения страниц
page = st.empty()

# ===== Шаг 0: выбор роли =====
def show_role_selection():
    with page.container():
        st.title("Система рекомендаций по методам преподавания")
        st.markdown("### Кто вы?")
        role_label = st.radio("Выберите роль", ["Преподаватель", "Студент"], key="role_radio")
        if st.button("Продолжить"):
            st.session_state.role = "teacher" if role_label == "Преподаватель" else "student"
            st.session_state.step = 1
            st.rerun()

# ===== Шаг 1: авторизация =====
def show_login():
    with page.container():
        role_label = "Преподаватель" if st.session_state.role == "teacher" else "Студент"
        st.title("Система рекомендаций по методам преподавания")
        st.markdown(f"### Вход ({role_label})")
        st.info(f"Вы вошли как: **{role_label}**")

        st.text_input("Номер группы", key="group_id")
        st.text_input("Индивидуальный ключ", type="password", key="user_key")

        if st.button("Продолжить"):
            group = st.session_state.group_id.strip().lower()
            key = st.session_state.user_key.strip().lower()
            role = st.session_state.role

            match = next((u for u in USERS if u["group_id"].strip().lower() == group and u["user_key"].strip().lower() == key and u["role"] == role), None)

            if match:
                st.session_state.pop("group_id", None)
                st.session_state.pop("user_key", None)
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Неверный ключ или группа.")

# ===== Шаги для преподавателя =====
def show_teacher_survey():
    steps = [
        ("discipline_type", "Тип дисциплины", ["Теоретическая", "Практико-ориентированная", "Смешанная"]),
        ("format", "Формат обучения", ["Очно", "Онлайн"]),
        ("engagement_level", "Уровень вовлечённости студентов", ["Высокая", "Средняя", "Низкая"]),
        ("attendance", "Посещаемость", ["≥ 75%", "< 75%"]),
        ("group_activity", "Есть групповая активность в LMS?", [True, False]),
        ("motivation", "Уровень мотивации студентов", (1.0, 5.0)),
        ("digital_literacy_students", "Цифровая грамотность студентов", ["Высокая", "Средняя", "Низкая"]),
        ("average_score", "Средний балл студентов", (2.0, 5.0)),
        ("anxiety_level", "Уровень тревожности студентов", (1.0, 5.0)),
        ("teacher_changed_recently", "Преподаватель менялся за последние 2 семестра?", [True, False]),
    ]
    current_step = st.session_state.step - 2

    with page.container():
        if current_step < len(steps):
            field_key, label, options = steps[current_step]
            st.markdown(f"### Вопрос {current_step + 1} из {len(steps)}")

            if not st.session_state.go_next:
                if isinstance(options, list):
                    st.selectbox(label, options, key=field_key)
                elif isinstance(options, tuple):
                    st.slider(label, options[0], options[1], (options[0] + options[1]) / 2, key=field_key)

                if st.button("Далее"):
                    st.session_state.profile[field_key] = st.session_state[field_key]
                    st.session_state.go_next = True
                    st.rerun()
            else:
                st.session_state.step += 1
                st.session_state.go_next = False
                st.rerun()
        else:
            st.markdown("### Все ответы получены:")
            for k, v in st.session_state.profile.items():
                st.write(f"**{k}**: {v}")

            method = evaluate_profile(st.session_state.profile)
            st.success(f"📚 Рекомендуемый метод преподавания: **{method}**")
            desc = get_method_description(method)
            if desc:
                st.markdown(f"📖 **Описание метода:** {desc}")

            if st.button("Сбросить"):
                st.session_state.step = 0
                st.session_state.profile = {}
                st.session_state.go_next = False
                st.session_state.pop("group_id", None)
                st.session_state.pop("user_key", None)
                st.rerun()

# ===== Шаги для студента =====
def show_student_survey():
    steps = [
        ("course_name", "Какой курс или дисциплину вы проходите?", "text"),
        ("clarity", "Насколько понятны вам учебные материалы и объяснения преподавателя?", "slider"),
        ("difficult_topics", "Какие темы в курсе кажутся вам наиболее сложными?", "text"),
        ("attendance", "Как часто вы посещаете занятия по данной дисциплине?", "select", ["Всегда", "Часто", "Редко", "Почти не хожу"]),
        ("lms_activity", "Насколько активно вы участвуете в LMS?", "slider"),
        ("deadline_respect", "Сдаёте ли вы задания в срок?", "select", ["Всегда", "Иногда", "Редко", "Не сдаю"]),
        ("extra_materials", "Используете ли вы дополнительные учебные материалы?", "select", ["Да", "Иногда", "Нет"]),
        ("format_interest", "Насколько вам интересен текущий формат обучения?", "slider"),
        ("preferred_task_type", "Какой тип заданий наиболее удобен?", "select", ["Тесты", "Проекты", "Эссе", "Устные ответы"]),
        ("barriers", "Что мешает вам успешно осваивать материал?", "text_area")
    ]
    current_step = st.session_state.step - 2

    with page.container():
        if current_step < len(steps):
            q_key, label, input_type, *opts = steps[current_step]
            st.markdown(f"### Вопрос {current_step + 1} из {len(steps)}")

            if input_type == "text":
                st.text_input(label, key=q_key)
            elif input_type == "text_area":
                st.text_area(label, key=q_key)
            elif input_type == "slider":
                st.slider(label, 1, 5, 3, key=q_key)
            elif input_type == "select":
                st.selectbox(label, opts[0], key=q_key)

            if st.button("Далее"):
                st.session_state.student_answers[q_key] = st.session_state[q_key]
                st.session_state.step += 1
                st.rerun()
        else:
            st.success("Спасибо за ваш отзыв! Он будет учтён при дальнейшем улучшении курса.")
            st.write("**Ваши ответы:**")
            for k, v in st.session_state.student_answers.items():
                st.write(f"**{k}**: {v}")

            if st.button("Завершить"):
                st.session_state.step = 0
                st.session_state.role = None
                st.session_state.student_answers = {}
                st.session_state.pop("group_id", None)
                st.session_state.pop("user_key", None)
                st.rerun()

# ===== Роутинг =====
if st.session_state.step == 0:
    show_role_selection()
elif st.session_state.step == 1:
    show_login()
else:
    if st.session_state.role == "teacher":
        show_teacher_survey()
    else:
        show_student_survey()