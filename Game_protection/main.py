import json
import os
import tkinter as tk
from tkinter import font as tkfont


class CyberSafeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Safe Phone")
        self.root.geometry("430x820")
        self.root.minsize(390, 700)
        self.root.configure(bg="#111315")

        self.player_name = ""
        self.score = 0
        self.current_index = 0
        self.is_waiting_next = False
        self.scenarios = []
        self.handbook = []

        self.colors = {
            "bg": "#111315",
            "phone": "#171a1d",
            "header": "#1e2328",
            "panel": "#20262c",
            "panel_2": "#262d34",
            "text": "#f2f4f5",
            "muted": "#a9b1b8",
            "accent": "#4da3ff",
            "good": "#37c871",
            "bad": "#ff5c75",
            "warn": "#ffb84d",
            "bubble_left": "#222930",
            "bubble_right": "#2a4f7c",
            "option_bg": "#2a3138",
            "option_hover": "#36404a",
        }

        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.h1_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.h2_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.body_font = tkfont.Font(family="Segoe UI", size=11)
        self.small_font = tkfont.Font(family="Segoe UI", size=9)

        self.load_data()
        self.build_shell()
        self.show_start_screen()

    def load_data(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "data.json")

        if not os.path.exists(path):
            raise FileNotFoundError("Файл data.json не найден рядом с main.py")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.scenarios = data.get("scenarios", [])
        self.handbook = data.get("handbook", [])

    def build_shell(self):
        self.outer = tk.Frame(self.root, bg=self.colors["bg"])
        self.outer.pack(fill="both", expand=True, padx=16, pady=14)

        self.phone = tk.Frame(
            self.outer,
            bg=self.colors["phone"],
            highlightthickness=1,
            highlightbackground="#2d343b",
        )
        self.phone.pack(fill="both", expand=True)

        self.topbar = tk.Frame(self.phone, bg="#0d0f11", height=30)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.status_left = tk.Label(
            self.topbar,
            text="9:58",
            bg="#0d0f11",
            fg="#e8edf2",
            font=("Segoe UI", 9, "bold"),
        )
        self.status_left.pack(side="left", padx=12, pady=6)

        self.status_right = tk.Label(
            self.topbar,
            text="📶  Wi-Fi  🔋",
            bg="#0d0f11",
            fg="#e8edf2",
            font=("Segoe UI Symbol", 9),
        )
        self.status_right.pack(side="right", padx=12, pady=6)

        self.header = tk.Frame(self.phone, bg=self.colors["header"], height=62)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.header_left = tk.Frame(self.header, bg=self.colors["header"])
        self.header_left.pack(side="left", fill="y", padx=12)

        self.header_title = tk.Label(
            self.header_left,
            text="SecureChat",
            bg=self.colors["header"],
            fg=self.colors["text"],
            font=self.title_font,
        )
        self.header_title.pack(anchor="w", pady=(8, 0))

        self.header_subtitle = tk.Label(
            self.header_left,
            text="Обучение цифровой безопасности",
            bg=self.colors["header"],
            fg=self.colors["muted"],
            font=self.small_font,
        )
        self.header_subtitle.pack(anchor="w")

        self.header_right = tk.Frame(self.header, bg=self.colors["header"])
        self.header_right.pack(side="right", padx=10)

        self.score_label = tk.Label(
            self.header_right,
            text="Очки: 0",
            bg=self.colors["header"],
            fg=self.colors["text"],
            font=self.h2_font,
        )
        self.score_label.pack(anchor="e", pady=(10, 2))

        self.progress_label = tk.Label(
            self.header_right,
            text="0/0",
            bg=self.colors["header"],
            fg=self.colors["muted"],
            font=self.small_font,
        )
        self.progress_label.pack(anchor="e")

        self.body = tk.Frame(self.phone, bg=self.colors["phone"])
        self.body.pack(fill="both", expand=True)

        self.bottom_nav = tk.Frame(self.phone, bg="#0d0f11", height=42)
        self.bottom_nav.pack(fill="x", side="bottom")
        self.bottom_nav.pack_propagate(False)

        self.nav_info = tk.Label(
            self.bottom_nav,
            text="●",
            bg="#0d0f11",
            fg="#dbe4ec",
            font=("Segoe UI Symbol", 12),
        )
        self.nav_info.pack(pady=8)

    def clear_body(self):
        for widget in self.body.winfo_children():
            widget.destroy()

    def update_header_stats(self):
        total = len(self.scenarios)
        shown = min(self.current_index + 1, total) if total else 0
        if self.current_index >= total:
            shown = total

        self.score_label.config(text=f"Очки: {self.score}")
        self.progress_label.config(text=f"{shown}/{total}")

    def show_start_screen(self):
        self.clear_body()
        self.header_title.config(text="SecureChat")
        self.header_subtitle.config(text="Мини-симулятор мошенничества")
        self.update_header_stats()

        wrapper = tk.Frame(self.body, bg=self.colors["phone"])
        wrapper.pack(fill="both", expand=True, padx=22, pady=24)

        card = tk.Frame(
            wrapper,
            bg=self.colors["panel"],
            highlightthickness=1,
            highlightbackground="#313841",
            padx=18,
            pady=18,
        )
        card.pack(fill="x", pady=(40, 14))

        tk.Label(
            card,
            text="Добро пожаловать",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=self.title_font,
        ).pack(anchor="w")

        tk.Label(
            card,
            text=(
                "Ты находишься в мессенджере. Тебе будут приходить "
                "подозрительные сообщения, уведомления и просьбы.\n\n"
                "Твоя задача — распознать мошенничество и выбрать безопасное действие."
            ),
            justify="left",
            wraplength=320,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.body_font,
        ).pack(anchor="w", pady=(10, 14))

        tk.Label(
            card,
            text="Имя пользователя",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=self.h2_font,
        ).pack(anchor="w", pady=(0, 6))

        self.name_entry = tk.Entry(
            card,
            font=("Segoe UI", 12),
            relief="flat",
            bd=0,
            bg="#101418",
            fg="white",
            insertbackground="white",
        )
        self.name_entry.pack(fill="x", ipady=10)
        self.name_entry.focus_set()

        btn_row = tk.Frame(wrapper, bg=self.colors["phone"])
        btn_row.pack(fill="x", pady=8)

        self.make_button(
            btn_row,
            text="Начать",
            command=self.start_game,
            bg=self.colors["accent"],
            fg="white",
        ).pack(fill="x", pady=(6, 10))

        self.make_button(
            btn_row,
            text="Открыть справочник",
            command=self.show_handbook,
            bg=self.colors["option_bg"],
            fg=self.colors["text"],
        ).pack(fill="x")

    def make_button(self, parent, text, command, bg, fg):
        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=self.h2_font,
            padx=14,
            pady=12,
            cursor="hand2",
        )
        btn.bind("<Button-1>", lambda e: command())

        normal_bg = bg
        hover_bg = self.colors["option_hover"] if bg == self.colors["option_bg"] else bg

        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))
        return btn

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            return

        self.player_name = name
        self.score = 0
        self.current_index = 0
        self.is_waiting_next = False
        self.show_chat_screen()

    def show_handbook(self):
        self.clear_body()
        self.header_title.config(text="Справочник")
        self.header_subtitle.config(text="Коротко о защите данных")

        wrapper = tk.Frame(self.body, bg=self.colors["phone"])
        wrapper.pack(fill="both", expand=True, padx=14, pady=12)

        top = tk.Frame(wrapper, bg=self.colors["phone"])
        top.pack(fill="x", pady=(0, 10))

        self.make_button(
            top,
            text="← Назад",
            command=self.show_start_screen if not self.player_name else self.show_chat_screen,
            bg=self.colors["option_bg"],
            fg=self.colors["text"],
        ).pack(anchor="w")

        canvas = tk.Canvas(
            wrapper,
            bg=self.colors["phone"],
            highlightthickness=0,
            bd=0,
        )
        scrollbar = tk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors["phone"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in self.handbook:
            card = tk.Frame(
                scroll_frame,
                bg=self.colors["panel"],
                highlightthickness=1,
                highlightbackground="#313841",
                padx=14,
                pady=12,
            )
            card.pack(fill="x", pady=6)

            tk.Label(
                card,
                text=item["title"],
                bg=self.colors["panel"],
                fg=self.colors["text"],
                font=self.h1_font,
            ).pack(anchor="w")

            tk.Label(
                card,
                text=item["text"],
                bg=self.colors["panel"],
                fg=self.colors["muted"],
                font=self.body_font,
                wraplength=330,
                justify="left",
            ).pack(anchor="w", pady=(8, 0))

    def show_chat_screen(self):
        self.clear_body()
        self.header_title.config(text="Чат: Администратор безопасности")
        self.header_subtitle.config(text=f"Пользователь: {self.player_name}")
        self.update_header_stats()

        if self.current_index >= len(self.scenarios):
            self.show_final_screen()
            return

        scenario = self.scenarios[self.current_index]

        main = tk.Frame(self.body, bg=self.colors["phone"])
        main.pack(fill="both", expand=True)

        top_actions = tk.Frame(main, bg=self.colors["phone"])
        top_actions.pack(fill="x", padx=12, pady=(10, 6))

        self.make_button(
            top_actions,
            text="Справочник",
            command=self.show_handbook,
            bg=self.colors["option_bg"],
            fg=self.colors["text"],
        ).pack(side="left")

        chat_area = tk.Frame(main, bg=self.colors["phone"])
        chat_area.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        canvas = tk.Canvas(chat_area, bg=self.colors["phone"], highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(chat_area, orient="vertical", command=canvas.yview)
        self.chat_frame = tk.Frame(canvas, bg=self.colors["phone"])

        self.chat_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.add_system_notice("Система", "Открыт защищённый обучающий чат.")
        self.add_left_bubble("Администратор", scenario["intro"])
        self.add_left_bubble(scenario["sender"], scenario["message"])

        self.feedback_holder = tk.Frame(self.chat_frame, bg=self.colors["phone"])
        self.feedback_holder.pack(fill="x", pady=(4, 8))

        bottom = tk.Frame(main, bg=self.colors["panel"])
        bottom.pack(fill="x", side="bottom", padx=10, pady=(0, 10))

        tk.Label(
            bottom,
            text="Выбери действие",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.small_font,
        ).pack(anchor="w", padx=10, pady=(10, 6))

        self.options_frame = tk.Frame(bottom, bg=self.colors["panel"])
        self.options_frame.pack(fill="x", padx=8, pady=(0, 8))

        for idx, option in enumerate(scenario["options"]):
            self.create_option_button(option, idx).pack(fill="x", pady=4)

        self.next_btn = self.make_button(
            bottom,
            text="Следующее сообщение",
            command=self.next_scenario,
            bg=self.colors["accent"],
            fg="white",
        )
        self.next_btn.pack(fill="x", padx=8, pady=(2, 10))
        self.next_btn.pack_forget()

        canvas.update_idletasks()
        canvas.yview_moveto(1.0)

    def add_system_notice(self, title, text):
        wrap = tk.Frame(self.chat_frame, bg=self.colors["phone"])
        wrap.pack(fill="x", pady=(8, 6))

        label = tk.Label(
            wrap,
            text=f"{title}: {text}",
            bg=self.colors["phone"],
            fg=self.colors["muted"],
            font=self.small_font,
        )
        label.pack()

    def add_left_bubble(self, sender, text):
        row = tk.Frame(self.chat_frame, bg=self.colors["phone"])
        row.pack(fill="x", pady=5, anchor="w")

        bubble = tk.Frame(row, bg=self.colors["bubble_left"], padx=10, pady=8)
        bubble.pack(anchor="w")

        tk.Label(
            bubble,
            text=sender,
            bg=self.colors["bubble_left"],
            fg=self.colors["accent"],
            font=self.small_font,
        ).pack(anchor="w")

        tk.Label(
            bubble,
            text=text,
            bg=self.colors["bubble_left"],
            fg=self.colors["text"],
            font=self.body_font,
            wraplength=260,
            justify="left",
        ).pack(anchor="w", pady=(2, 0))

    def add_right_bubble(self, text):
        row = tk.Frame(self.chat_frame, bg=self.colors["phone"])
        row.pack(fill="x", pady=5)

        bubble = tk.Frame(row, bg=self.colors["bubble_right"], padx=10, pady=8)
        bubble.pack(anchor="e")

        tk.Label(
            bubble,
            text=self.player_name,
            bg=self.colors["bubble_right"],
            fg="#d7ebff",
            font=self.small_font,
        ).pack(anchor="e")

        tk.Label(
            bubble,
            text=text,
            bg=self.colors["bubble_right"],
            fg="white",
            font=self.body_font,
            wraplength=260,
            justify="left",
        ).pack(anchor="e", pady=(2, 0))

    def create_feedback_card(self, title, text, tone):
        tone_color = {
            "good": self.colors["good"],
            "bad": self.colors["bad"],
            "warn": self.colors["warn"],
        }.get(tone, self.colors["accent"])

        card = tk.Frame(
            self.feedback_holder,
            bg=self.colors["panel_2"],
            highlightthickness=1,
            highlightbackground=tone_color,
            padx=12,
            pady=10,
        )
        card.pack(fill="x", pady=8)

        tk.Label(
            card,
            text=title,
            bg=self.colors["panel_2"],
            fg=tone_color,
            font=self.h2_font,
        ).pack(anchor="w")

        tk.Label(
            card,
            text=text,
            bg=self.colors["panel_2"],
            fg=self.colors["text"],
            font=self.body_font,
            wraplength=310,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def create_option_button(self, text, idx):
        label = tk.Label(
            self.options_frame,
            text=text,
            bg=self.colors["option_bg"],
            fg=self.colors["text"],
            font=self.body_font,
            padx=12,
            pady=10,
            cursor="hand2",
            wraplength=320,
            justify="left",
        )

        label.bind("<Button-1>", lambda e: self.select_option(idx))
        label.bind("<Enter>", lambda e: label.config(bg=self.colors["option_hover"]))
        label.bind("<Leave>", lambda e: label.config(bg=self.colors["option_bg"]))
        return label

    def disable_options(self):
        for child in self.options_frame.winfo_children():
            child.unbind("<Button-1>")
            child.config(bg="#23272d", fg="#808892", cursor="arrow")

    def select_option(self, idx):
        if self.is_waiting_next:
            return

        scenario = self.scenarios[self.current_index]
        self.is_waiting_next = True

        chosen_text = scenario["options"][idx]
        self.add_right_bubble(chosen_text)
        self.disable_options()

        if idx == scenario["correct"]:
            self.score += scenario.get("score", 1)
            tone = "good"
            title = "Верное решение"
            feedback = scenario["success_feedback"]
        else:
            tone = "bad"
            title = "Опасное решение"
            feedback = scenario["fail_feedback"]

        self.create_feedback_card(title, feedback, tone)
        self.add_left_bubble("Администратор", scenario["explanation"])

        extra = scenario.get("praise") if idx == scenario["correct"] else scenario.get("warning")
        if extra:
            self.create_feedback_card(
                "Комментарий администратора",
                extra,
                "warn" if idx != scenario["correct"] else "good",
            )

        self.update_header_stats()
        self.next_btn.pack(fill="x", padx=8, pady=(2, 10))

    def next_scenario(self):
        self.current_index += 1
        self.is_waiting_next = False

        if self.current_index >= len(self.scenarios):
            self.show_final_screen()
        else:
            self.show_chat_screen()

    def show_final_screen(self):
        self.clear_body()
        self.header_title.config(text="Результат")
        self.header_subtitle.config(text=f"Пользователь: {self.player_name}")
        self.update_header_stats()

        wrapper = tk.Frame(self.body, bg=self.colors["phone"])
        wrapper.pack(fill="both", expand=True, padx=18, pady=18)

        if self.score <= 3:
            rank = "Новичок"
            summary = "Ты уже видишь часть угроз, но пока легко попасться на давление и срочность."
            rank_color = self.colors["bad"]
        elif self.score <= 7:
            rank = "Осторожный пользователь"
            summary = "Хороший результат. Ты замечаешь явные признаки обмана, но ещё есть куда расти."
            rank_color = self.colors["warn"]
        else:
            rank = "Кибер-защитник"
            summary = "Отлично. Ты уверенно распознаёшь подозрительные действия и не раскрываешь данные."
            rank_color = self.colors["good"]

        card = tk.Frame(
            wrapper,
            bg=self.colors["panel"],
            highlightthickness=1,
            highlightbackground="#313841",
            padx=18,
            pady=18,
        )
        card.pack(fill="x", pady=(50, 14))

        tk.Label(
            card,
            text=f"{self.player_name}, симуляция завершена",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=self.h1_font,
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"Очки безопасности: {self.score} / {sum(s.get('score', 1) for s in self.scenarios)}",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=self.body_font,
        ).pack(anchor="w", pady=(12, 6))

        tk.Label(
            card,
            text=f"Ранг: {rank}",
            bg=self.colors["panel"],
            fg=rank_color,
            font=self.title_font,
        ).pack(anchor="w", pady=(4, 8))

        tk.Label(
            card,
            text=summary,
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=self.body_font,
            wraplength=320,
            justify="left",
        ).pack(anchor="w")

        buttons = tk.Frame(wrapper, bg=self.colors["phone"])
        buttons.pack(fill="x", pady=10)

        self.make_button(
            buttons,
            text="Сыграть снова",
            command=self.restart_game,
            bg=self.colors["accent"],
            fg="white",
        ).pack(fill="x", pady=(0, 8))

        self.make_button(
            buttons,
            text="Открыть справочник",
            command=self.show_handbook,
            bg=self.colors["option_bg"],
            fg=self.colors["text"],
        ).pack(fill="x")

    def restart_game(self):
        self.score = 0
        self.current_index = 0
        self.is_waiting_next = False
        self.show_chat_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberSafeGame(root)
    root.mainloop()