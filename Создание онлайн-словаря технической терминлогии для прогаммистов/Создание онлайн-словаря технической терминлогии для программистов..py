import tkinter as tk
from tkinter import messagebox
import random
import json
from pathlib import Path

TERMS = [
    ("Algorithm", "Последовательность шагов, которая решает конкретную задачу."),
    ("Program", "Набор инструкций, которые выполняет компьютер."),
    ("Code", "Текст программы, написанный на языке программирования."),
    ("Compilation", "Перевод исходного кода в машинный или промежуточный код."),
    ("Interpretation", "Выполнение кода построчно без предварительной полной компиляции."),
    ("Variable", "Именованное место для хранения значения в программе."),
    ("Constant", "Значение, которое не должно изменяться во время работы программы."),
    ("Data Type", "Категория данных: число, строка, список, логическое значение и т.д."),
    ("Function", "Блок кода, который выполняет определённую задачу."),
    ("Method", "Функция, которая принадлежит объекту или классу."),
    ("Condition", "Конструкция, которая позволяет выполнить код только при выполнении условия."),
    ("Loop", "Конструкция для повторения одного и того же действия несколько раз."),
    ("Array", "Коллекция элементов, обычно одного типа, расположенных по индексам."),
    ("List", "Упорядоченная коллекция элементов, которую можно изменять."),
    ("Dictionary", "Структура данных, где значения хранятся в формате ключ — значение."),
    ("Class", "Шаблон для создания объектов с общими свойствами и поведением."),
    ("Object", "Экземпляр класса, который имеет данные и методы."),
    ("Inheritance", "Механизм, позволяющий одному классу получать свойства другого класса."),
    ("Encapsulation", "Сокрытие внутренней логики объекта и защита данных от прямого доступа."),
    ("Polymorphism", "Возможность использовать один интерфейс для разных типов объектов."),
    ("Bug", "Ошибка в программе, из-за которой она работает неправильно."),
    ("Debugging", "Процесс поиска и исправления ошибок в коде."),
    ("Fix", "Исправление ошибки или проблемы в программе."),
    ("Refactoring", "Улучшение структуры кода без изменения его внешнего поведения."),
    ("Repository", "Хранилище проекта и истории его изменений."),
    ("Git", "Система контроля версий для отслеживания изменений в коде."),
    ("Commit", "Сохранённое состояние изменений в репозитории."),
    ("Branch", "Отдельная линия разработки в системе контроля версий."),
    ("Merge", "Объединение изменений из разных веток."),
    ("Pull Request", "Запрос на проверку и добавление изменений в проект."),
    ("Frontend", "Часть приложения, с которой взаимодействует пользователь."),
    ("Backend", "Серверная часть приложения, где работает основная логика."),
    ("API", "Интерфейс, через который программы взаимодействуют друг с другом."),
    ("HTTP", "Протокол передачи данных между клиентом и сервером."),
    ("HTTPS", "Защищённая версия HTTP с шифрованием данных."),
    ("URL", "Адрес веб-страницы или ресурса в интернете."),
    ("HTML", "Язык разметки для создания структуры веб-страниц."),
    ("CSS", "Язык стилей для оформления веб-страниц."),
    ("JavaScript", "Язык программирования, часто используемый в веб-разработке."),
    ("JSON", "Текстовый формат хранения и передачи данных."),
    ("Database", "Организованное хранилище информации."),
    ("SQL", "Язык для работы с реляционными базами данных."),
    ("Table", "Структура базы данных, состоящая из строк и столбцов."),
    ("Record", "Одна строка данных в таблице базы данных."),
    ("Index", "Структура, которая ускоряет поиск данных в базе."),
    ("CRUD", "Основные операции с данными: создать, прочитать, обновить, удалить."),
    ("Server", "Компьютер или программа, которая обрабатывает запросы клиентов."),
    ("Client", "Программа или устройство, которое отправляет запрос серверу."),
    ("Deployment", "Размещение приложения на сервере для использования."),
    ("CI/CD", "Автоматизация проверки, сборки и доставки приложения."),
    ("Framework", "Готовая основа для разработки приложений."),
    ("Library", "Набор готовых функций или инструментов для разработки."),
    ("Module", "Отдельная часть программы, которую можно подключать и использовать."),
    ("Package", "Набор модулей, объединённых для удобного использования."),
    ("Docker", "Инструмент для запуска приложений в изолированных контейнерах."),
    ("IDE", "Среда разработки с редактором кода, запуском и отладкой."),
    ("CLI", "Интерфейс командной строки."),
    ("GUI", "Графический интерфейс пользователя с окнами, кнопками и меню."),
    ("Log", "Запись событий, ошибок и действий программы."),
    ("Cache", "Временное хранилище данных для ускорения работы."),
    ("Thread", "Отдельная линия выполнения внутри программы."),
    ("Asynchronous", "Способ выполнения задач без ожидания завершения каждой из них."),
    ("Stack", "Структура данных, где последний добавленный элемент выходит первым."),
    ("Queue", "Структура данных, где первый добавленный элемент выходит первым."),
]

SAVE_FILE = Path(__file__).with_name("dictionary_progress.json")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Словарь программиста")
        self.root.geometry("1200x720")
        self.root.minsize(950, 600)
        self.root.configure(bg="#0f131d")

        self.term_dict = dict(TERMS)
        self.current_term = None
        self.current_answer = None

        self.progress = {
            "seen": [],
            "known": [],
            "unknown": [],
            "opened": [],
            "random_clicks": 0
        }

        self.load_progress()
        self.build_ui()
        self.refresh_list()
        self.update_stats()
        self.show_random_term()

    def load_progress(self):
        if SAVE_FILE.exists():
            try:
                data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    self.progress.update(data)
            except Exception:
                pass

        valid = set(self.term_dict.keys())
        for key in ["seen", "known", "unknown", "opened"]:
            self.progress[key] = [x for x in self.progress.get(key, []) if x in valid]

    def save_progress(self):
        try:
            SAVE_FILE.write_text(json.dumps(self.progress, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def build_ui(self):
        # === ROOT GRID ===
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        app = tk.Frame(self.root, bg="#0f131d")
        app.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

        app.grid_rowconfigure(1, weight=1)
        app.grid_columnconfigure(0, weight=1)
        app.grid_columnconfigure(1, weight=0)

        # === TOP BAR ===
        top = tk.Frame(app, bg="#0f131d")
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        top.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            top,
            text="📘 Словарь программиста",
            font=("Segoe UI", 22, "bold"),
            bg="#0f131d",
            fg="#f4f6ff"
        )
        title.grid(row=0, column=0, sticky="w")

        self.stats_label = tk.Label(
            top,
            text="",
            font=("Segoe UI", 11),
            bg="#0f131d",
            fg="#a9b2c7"
        )
        self.stats_label.grid(row=1, column=0, sticky="w", pady=(6, 0))

        # === CENTER CARD ===
        center = tk.Frame(app, bg="#151a26", highlightthickness=1, highlightbackground="#2a3246")
        center.grid(row=1, column=0, sticky="nsew", padx=(0, 14))
        center.grid_rowconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=0)
        center.grid_columnconfigure(0, weight=1)

        card = tk.Frame(center, bg="#1c2333", highlightthickness=1, highlightbackground="#343e56")
        card.grid(row=0, column=0, sticky="nsew", padx=22, pady=22)
        card.grid_rowconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=0)
        card.grid_rowconfigure(2, weight=1)
        card.grid_columnconfigure(0, weight=1)

        self.term_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 44, "bold"),
            bg="#1c2333",
            fg="#ffd166",
            wraplength=720,
            justify="center"
        )
        self.term_label.grid(row=0, column=0, sticky="s", padx=30, pady=(30, 10))

        self.answer_label = tk.Label(
            card,
            text="Объяснение скрыто",
            font=("Segoe UI", 17),
            bg="#1c2333",
            fg="#d6dcee",
            wraplength=780,
            justify="center"
        )
        self.answer_label.grid(row=1, column=0, sticky="n", padx=40, pady=(8, 18))

        self.tip_label = tk.Label(
            card,
            text="Enter — ответ   •   Space — случайный термин   •   1 — знаю   •   2 — повторить",
            font=("Segoe UI", 11),
            bg="#1c2333",
            fg="#8d98b2"
        )
        self.tip_label.grid(row=2, column=0, sticky="s", pady=(0, 24))

        # === BUTTON PANEL ===
        controls = tk.Frame(center, bg="#151a26")
        controls.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 22))
        for i in range(5):
            controls.grid_columnconfigure(i, weight=1)

        self.button(controls, "🎲 Случайный", self.show_random_term, "#ff9f1c", "#101010").grid(row=0, column=0, sticky="ew", padx=6)
        self.button(controls, "👁 Ответ", self.show_answer, "#2ec4b6", "#071b1a").grid(row=0, column=1, sticky="ew", padx=6)
        self.button(controls, "✅ Знаю", self.mark_known, "#7bd88f", "#102015").grid(row=0, column=2, sticky="ew", padx=6)
        self.button(controls, "❌ Повторить", self.mark_unknown, "#ff6b6b", "#1f1111").grid(row=0, column=3, sticky="ew", padx=6)
        self.button(controls, "🔄 Сброс", self.reset_progress, "#2c354c", "#f4f6ff").grid(row=0, column=4, sticky="ew", padx=6)

        # === RIGHT PANEL ===
        right = tk.Frame(app, bg="#1c2333", width=310, highlightthickness=1, highlightbackground="#343e56")
        right.grid(row=1, column=1, sticky="ns")
        right.grid_propagate(False)
        right.grid_rowconfigure(2, weight=1)
        right.grid_columnconfigure(0, weight=1)

        tk.Label(
            right,
            text="📋 Список терминов",
            font=("Segoe UI", 15, "bold"),
            bg="#1c2333",
            fg="#ffffff"
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_list())

        self.search_entry = tk.Entry(
            right,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            bg="#111722",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat"
        )
        self.search_entry.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12), ipady=8)

        list_frame = tk.Frame(right, bg="#1c2333")
        list_frame.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 10))
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            bg="#111722",
            fg="#ffffff",
            selectbackground="#ff9f1c",
            selectforeground="#101010",
            activestyle="none",
            yscrollcommand=scrollbar.set,
            relief="flat",
            borderwidth=0
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.listbox.yview)

        legend = tk.Label(
            right,
            text="✅ изучено   ❌ повторить   👁 ответ открыт",
            font=("Segoe UI", 9),
            bg="#1c2333",
            fg="#a9b2c7"
        )
        legend.grid(row=3, column=0, padx=14, pady=(0, 14), sticky="w")

        self.listbox.bind("<<ListboxSelect>>", self.select_from_list)
        self.root.bind("<Return>", lambda e: self.show_answer())
        self.root.bind("<space>", lambda e: self.show_random_term())
        self.root.bind("1", lambda e: self.mark_known())
        self.root.bind("2", lambda e: self.mark_unknown())

    def button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief="flat",
            padx=12,
            pady=12,
            cursor="hand2"
        )

    def display_term(self, term):
        self.current_term = term
        self.current_answer = self.term_dict[term]

        if term not in self.progress["seen"]:
            self.progress["seen"].append(term)

        self.term_label.config(text=term)
        self.answer_label.config(text="Объяснение скрыто")
        self.save_progress()
        self.update_stats()
        self.refresh_list(keep_selection=term)

    def show_random_term(self):
        self.progress["random_clicks"] += 1
        not_known = [term for term, _ in TERMS if term not in self.progress["known"]]
        pool = not_known if not_known else [term for term, _ in TERMS]
        self.display_term(random.choice(pool))

    def show_answer(self):
        if not self.current_term:
            messagebox.showwarning("Нет термина", "Сначала выбери термин.")
            return

        self.answer_label.config(text=self.current_answer)

        if self.current_term not in self.progress["opened"]:
            self.progress["opened"].append(self.current_term)

        self.save_progress()
        self.update_stats()
        self.refresh_list(keep_selection=self.current_term)

    def mark_known(self):
        if not self.current_term:
            return

        if self.current_term not in self.progress["known"]:
            self.progress["known"].append(self.current_term)

        if self.current_term in self.progress["unknown"]:
            self.progress["unknown"].remove(self.current_term)

        self.save_progress()
        self.update_stats()
        self.refresh_list(keep_selection=self.current_term)

    def mark_unknown(self):
        if not self.current_term:
            return

        if self.current_term not in self.progress["unknown"]:
            self.progress["unknown"].append(self.current_term)

        if self.current_term in self.progress["known"]:
            self.progress["known"].remove(self.current_term)

        self.save_progress()
        self.update_stats()
        self.refresh_list(keep_selection=self.current_term)

    def reset_progress(self):
        if not messagebox.askyesno("Сброс прогресса", "Сбросить статистику и подсветку?"):
            return

        self.progress = {
            "seen": [],
            "known": [],
            "unknown": [],
            "opened": [],
            "random_clicks": 0
        }
        self.save_progress()
        self.refresh_list()
        self.update_stats()
        self.show_random_term()

    def select_from_list(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return

        text = self.listbox.get(selection[0])
        term = text.replace("✅ ", "").replace("❌ ", "").replace("👁 ", "").strip()

        if term in self.term_dict:
            self.display_term(term)

    def refresh_list(self, keep_selection=None):
        if not hasattr(self, "listbox"):
            return

        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        self.listbox.delete(0, tk.END)
        self.visible_terms = []

        for term, _ in TERMS:
            if query and query not in term.lower():
                continue

            if term in self.progress["known"]:
                prefix = "✅ "
                color = "#7bd88f"
            elif term in self.progress["unknown"]:
                prefix = "❌ "
                color = "#ff8b8b"
            elif term in self.progress["opened"]:
                prefix = "👁 "
                color = "#ffd166"
            else:
                prefix = ""
                color = "#ffffff"

            self.visible_terms.append(term)
            self.listbox.insert(tk.END, prefix + term)
            self.listbox.itemconfig(tk.END, fg=color)

        if keep_selection and keep_selection in self.visible_terms:
            idx = self.visible_terms.index(keep_selection)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.listbox.see(idx)

    def update_stats(self):
        total = len(TERMS)
        seen = len(self.progress["seen"])
        known = len(self.progress["known"])
        unknown = len(self.progress["unknown"])
        opened = len(self.progress["opened"])
        percent = round((known / total) * 100)

        self.stats_label.config(
            text=f"Всего: {total}   •   Просмотрено: {seen}   •   Изучено: {known} ({percent}%)   •   Повторить: {unknown}   •   Ответ открыт: {opened}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
