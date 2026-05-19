import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DATA_FILE = "bookings.json"

SPACES = [
    {"id": 1, "name": "Desk A1", "type": "Рабочее место", "capacity": 1, "price": 1200, "zone": "Open Space"},
    {"id": 2, "name": "Desk A2", "type": "Рабочее место", "capacity": 1, "price": 1200, "zone": "Open Space"},
    {"id": 3, "name": "Desk B1 Premium", "type": "Рабочее место", "capacity": 1, "price": 1800, "zone": "Quiet Zone"},
    {"id": 4, "name": "Meeting Room Alpha", "type": "Переговорная", "capacity": 6, "price": 4500, "zone": "Business"},
    {"id": 5, "name": "Meeting Room Omega", "type": "Переговорная", "capacity": 10, "price": 7000, "zone": "Business"},
    {"id": 6, "name": "Private Office", "type": "Кабинет", "capacity": 3, "price": 5000, "zone": "Private"},
]


class PremiumCoworkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coworking Pro — Dark Premium UI")
        self.root.geometry("1180x720")
        self.root.minsize(1060, 650)
        self.root.configure(bg="#0f172a")

        self.bookings = self.load_bookings()

        self.colors = {
            "bg": "#0f172a",
            "sidebar": "#020617",
            "panel": "#111827",
            "panel2": "#1e293b",
            "panel3": "#0b1220",
            "muted": "#94a3b8",
            "text": "#e2e8f0",
            "text2": "#cbd5e1",
            "blue": "#3b82f6",
            "blue_dark": "#2563eb",
            "orange": "#f97316",
            "orange_dark": "#ea580c",
            "green": "#22c55e",
            "red": "#ef4444",
            "border": "#263244",
            "soft_blue": "#172554",
            "soft_orange": "#431407",
            "soft_green": "#052e16",
            "soft_purple": "#2e1065",
        }

        self.setup_style()
        self.build_ui()
        self.refresh_space_cards()
        self.refresh_table()
        self.refresh_stats()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.colors["panel"],
            fieldbackground=self.colors["panel"],
            foreground=self.colors["text"],
            rowheight=38,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=self.colors["panel2"],
            foreground=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
            padding=10,
        )
        style.map(
            "Treeview",
            background=[("selected", self.colors["blue_dark"])],
            foreground=[("selected", "#ffffff")],
        )

        style.configure(
            "TCombobox",
            padding=8,
            fieldbackground=self.colors["panel3"],
            background=self.colors["panel2"],
            foreground=self.colors["text"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["border"],
            lightcolor=self.colors["border"],
            darkcolor=self.colors["border"],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.colors["panel3"])],
            foreground=[("readonly", self.colors["text"])],
            selectbackground=[("readonly", self.colors["panel3"])],
            selectforeground=[("readonly", self.colors["text"])],
        )

    def build_ui(self):
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self.root, bg=self.colors["bg"])
        self.content.pack(side="right", fill="both", expand=True)

        self.build_sidebar()
        self.build_header()
        self.build_main()

    def build_sidebar(self):
        tk.Label(
            self.sidebar,
            text="CO•WORK",
            bg=self.colors["sidebar"],
            fg="#ffffff",
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w", padx=24, pady=(28, 4))

        tk.Label(
            self.sidebar,
            text="Premium Dark Booking System",
            bg=self.colors["sidebar"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=24, pady=(0, 28))

        items = [
            ("🏠", "Панель управления"),
            ("📅", "Бронирования"),
            ("🪑", "Рабочие места"),
            ("👥", "Клиенты"),
            ("⚙️", "Настройки"),
        ]

        for icon, text in items:
            active = text == "Панель управления"
            item_bg = "#1e293b" if active else self.colors["sidebar"]
            item = tk.Frame(self.sidebar, bg=item_bg)
            item.pack(fill="x", padx=14, pady=4)

            tk.Frame(item, bg=(self.colors["orange"] if active else item_bg), width=4).pack(side="left", fill="y")

            tk.Label(
                item,
                text=f"{icon}  {text}",
                bg=item_bg,
                fg=("#ffffff" if active else self.colors["text2"]),
                font=("Segoe UI", 11, "bold" if active else "normal"),
                padx=14,
                pady=12,
            ).pack(side="left", anchor="w")

        tk.Frame(self.sidebar, bg=self.colors["border"], height=1).pack(fill="x", padx=24, pady=24)

        tk.Label(
            self.sidebar,
            text="Сегодня",
            bg=self.colors["sidebar"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=24)

        tk.Label(
            self.sidebar,
            text=datetime.now().strftime("%d.%m.%Y"),
            bg=self.colors["sidebar"],
            fg="#ffffff",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", padx=24, pady=(4, 0))

        tk.Label(
            self.sidebar,
            text="Данные сохраняются в bookings.json рядом с программой.",
            bg=self.colors["sidebar"],
            fg=self.colors["muted"],
            wraplength=190,
            justify="left",
            font=("Segoe UI", 9),
        ).pack(side="bottom", anchor="w", padx=24, pady=24)

    def build_header(self):
        header = tk.Frame(self.content, bg=self.colors["bg"], height=105)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=self.colors["bg"])
        left.pack(side="left", padx=28, pady=24)

        tk.Label(
            left,
            text="Бронирование коворкинга",
            bg=self.colors["bg"],
            fg="#ffffff",
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Управление местами, клиентами и активными бронями",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(header, bg=self.colors["bg"])
        right.pack(side="right", padx=28, pady=24)

        self.button(
            right,
            "+ Новая бронь",
            self.colors["orange"],
            self.colors["orange_dark"],
            lambda: self.name_entry.focus_set(),
            padx=18,
            pady=10,
        ).pack()

    def build_main(self):
        main = tk.Frame(self.content, bg=self.colors["bg"])
        main.pack(fill="both", expand=True, padx=28, pady=(0, 28))

        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(1, weight=1)

        self.stats_frame = tk.Frame(main, bg=self.colors["bg"])
        self.stats_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        self.stats_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_total = self.create_stat_card(self.stats_frame, 0, "Всего броней", "0", self.colors["soft_blue"], self.colors["blue"])
        self.stat_today = self.create_stat_card(self.stats_frame, 1, "Сегодня", "0", self.colors["soft_orange"], self.colors["orange"])
        self.stat_income = self.create_stat_card(self.stats_frame, 2, "Доход/час", "0 ₸", self.colors["soft_green"], self.colors["green"])
        self.stat_spaces = self.create_stat_card(self.stats_frame, 3, "Мест", str(len(SPACES)), self.colors["soft_purple"], "#a78bfa")

        left_panel = self.card(main)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_panel.rowconfigure(2, weight=1)
        left_panel.columnconfigure(0, weight=1)

        right_panel = self.card(main)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        self.build_booking_table(left_panel)
        self.build_booking_form(right_panel)

    def button(self, parent, text, bg, active_bg, command, padx=14, pady=8):
        return tk.Button(
            parent,
            text=text,
            bg=bg,
            fg="#ffffff",
            activebackground=active_bg,
            activeforeground="#ffffff",
            bd=0,
            padx=padx,
            pady=pady,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            command=command,
        )

    def create_stat_card(self, parent, col, title, value, icon_bg, accent):
        card = tk.Frame(parent, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1)
        card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 8, 0 if col == 3 else 8))
        card.columnconfigure(1, weight=1)

        icon = tk.Label(card, text="●", bg=icon_bg, fg=accent, font=("Segoe UI", 18), width=3)
        icon.grid(row=0, column=0, rowspan=2, padx=16, pady=16, sticky="w")

        tk.Label(card, text=title, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 10)).grid(row=0, column=1, sticky="e", padx=14, pady=(16, 0))
        value_label = tk.Label(card, text=value, bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 20, "bold"))
        value_label.grid(row=1, column=1, sticky="e", padx=14, pady=(0, 16))
        return value_label

    def card(self, parent):
        return tk.Frame(parent, bg=self.colors["panel"], highlightbackground=self.colors["border"], highlightthickness=1)

    def build_booking_table(self, parent):
        top = tk.Frame(parent, bg=self.colors["panel"])
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 10))
        top.columnconfigure(0, weight=1)

        tk.Label(top, text="Активные бронирования", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(top, text="Список всех созданных броней", bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.button(
            top,
            "Обновить",
            self.colors["blue"],
            self.colors["blue_dark"],
            lambda: [self.refresh_table(), self.refresh_stats()],
        ).grid(row=0, column=1, rowspan=2, sticky="e")

        filter_frame = tk.Frame(parent, bg=self.colors["panel"])
        filter_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        filter_frame.columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        search = tk.Entry(
            filter_frame,
            textvariable=self.search_var,
            bg=self.colors["panel3"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            font=("Segoe UI", 10),
        )
        search.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 10))
        search.bind("<KeyRelease>", lambda e: self.refresh_table())

        self.type_filter_var = tk.StringVar(value="Все")
        filter_box = ttk.Combobox(
            filter_frame,
            textvariable=self.type_filter_var,
            values=["Все", "Рабочее место", "Переговорная", "Кабинет"],
            state="readonly",
            width=18,
        )
        filter_box.grid(row=0, column=1, sticky="e")
        filter_box.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        columns = ("client", "space", "type", "date", "time", "price")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 12))

        headings = {
            "client": "Клиент",
            "space": "Место",
            "type": "Тип",
            "date": "Дата",
            "time": "Время",
            "price": "₸/час",
        }
        widths = {"client": 140, "space": 150, "type": 120, "date": 105, "time": 120, "price": 80}
        for col, title in headings.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, width=widths[col], anchor="center" if col == "price" else "w")

        bottom = tk.Frame(parent, bg=self.colors["panel"])
        bottom.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 18))
        bottom.columnconfigure(0, weight=1)

        self.button(
            bottom,
            "Удалить выбранную бронь",
            self.colors["red"],
            "#dc2626",
            self.delete_booking,
            padx=16,
            pady=9,
        ).grid(row=0, column=1, sticky="e")

    def build_booking_form(self, parent):
        parent.columnconfigure(0, weight=1)

        tk.Label(parent, text="Создать бронь", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w", padx=22, pady=(20, 4))
        tk.Label(parent, text="Заполни данные клиента и выбери место", bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 16))

        form = tk.Frame(parent, bg=self.colors["panel"])
        form.grid(row=2, column=0, sticky="ew", padx=22)
        form.columnconfigure(0, weight=1)

        self.name_entry = self.field(form, "Имя клиента", 0)
        self.contact_entry = self.field(form, "Телефон / email", 2)

        self.type_var = tk.StringVar(value="Все")
        self.combo_field(form, "Тип места", self.type_var, ["Все", "Рабочее место", "Переговорная", "Кабинет"], 4, self.refresh_space_cards)

        self.space_var = tk.StringVar()
        self.space_combo = self.combo_field(form, "Место", self.space_var, [], 6, None)

        date_time = tk.Frame(form, bg=self.colors["panel"])
        date_time.grid(row=8, column=0, sticky="ew", pady=(12, 0))
        date_time.columnconfigure((0, 1), weight=1)

        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.small_field(date_time, "Дата", self.date_var, 0, 0)

        self.start_var = tk.StringVar(value="10:00")
        self.small_combo(date_time, "Начало", self.start_var, [f"{h:02d}:00" for h in range(8, 23)], 0, 1)

        end_frame = tk.Frame(form, bg=self.colors["panel"])
        end_frame.grid(row=9, column=0, sticky="ew", pady=(12, 0))
        end_frame.columnconfigure(0, weight=1)

        self.end_var = tk.StringVar(value="11:00")
        self.small_combo(end_frame, "Окончание", self.end_var, [f"{h:02d}:00" for h in range(9, 24)], 0, 0)

        self.button(
            form,
            "Создать бронирование",
            self.colors["orange"],
            self.colors["orange_dark"],
            self.create_booking,
            padx=18,
            pady=12,
        ).grid(row=10, column=0, sticky="ew", pady=(20, 0))

        self.space_cards = tk.Frame(parent, bg=self.colors["panel"])
        self.space_cards.grid(row=3, column=0, sticky="ew", padx=22, pady=(22, 0))

    def label(self, parent, text):
        tk.Label(parent, text=text, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).grid(sticky="w")

    def field(self, parent, label, row):
        tk.Label(parent, text=label, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(
            parent,
            bg=self.colors["panel3"],
            fg=self.colors["text"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            insertbackground=self.colors["text"],
            font=("Segoe UI", 10),
        )
        entry.grid(row=row + 1, column=0, sticky="ew", ipady=10, pady=(5, 10))
        return entry

    def combo_field(self, parent, label, var, values, row, callback):
        tk.Label(parent, text=label, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w")
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        combo.grid(row=row + 1, column=0, sticky="ew", pady=(5, 10))
        if callback:
            combo.bind("<<ComboboxSelected>>", lambda e: callback())
        return combo

    def small_field(self, parent, label, var, row, col):
        box = tk.Frame(parent, bg=self.colors["panel"])
        box.grid(row=row, column=col, sticky="ew", padx=(0, 6) if col == 0 else (6, 0))
        box.columnconfigure(0, weight=1)
        tk.Label(box, text=label, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        entry = tk.Entry(
            box,
            textvariable=var,
            bg=self.colors["panel3"],
            fg=self.colors["text"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            insertbackground=self.colors["text"],
            font=("Segoe UI", 10),
        )
        entry.grid(row=1, column=0, sticky="ew", ipady=10, pady=(5, 0))
        return entry

    def small_combo(self, parent, label, var, values, row, col):
        box = tk.Frame(parent, bg=self.colors["panel"])
        box.grid(row=row, column=col, sticky="ew", padx=(0, 6) if col == 0 else (6, 0))
        box.columnconfigure(0, weight=1)
        tk.Label(box, text=label, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w")
        combo = ttk.Combobox(box, textvariable=var, values=values, state="readonly")
        combo.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        return combo

    def refresh_space_cards(self):
        selected_type = self.type_var.get()
        available = [s for s in SPACES if selected_type == "Все" or s["type"] == selected_type]
        values = [f'{s["id"]}. {s["name"]} — {s["type"]} ({s["price"]} ₸/час)' for s in available]
        self.space_combo["values"] = values
        self.space_var.set(values[0] if values else "")

        for w in self.space_cards.winfo_children():
            w.destroy()

        tk.Label(self.space_cards, text="Доступные места", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 10))

        for s in available[:4]:
            card = tk.Frame(self.space_cards, bg=self.colors["panel2"], highlightbackground=self.colors["border"], highlightthickness=1)
            card.pack(fill="x", pady=5)
            left = tk.Frame(card, bg=self.colors["panel2"])
            left.pack(side="left", fill="x", expand=True, padx=12, pady=10)

            tk.Label(left, text=s["name"], bg=self.colors["panel2"], fg=self.colors["text"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(left, text=f'{s["type"]} • {s["zone"]} • до {s["capacity"]} чел.', bg=self.colors["panel2"], fg=self.colors["muted"], font=("Segoe UI", 9)).pack(anchor="w")

            tk.Label(card, text=f'{s["price"]} ₸', bg=self.colors["panel2"], fg=self.colors["orange"], font=("Segoe UI", 11, "bold")).pack(side="right", padx=12)

    def create_booking(self):
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        space_text = self.space_var.get().strip()
        date = self.date_var.get().strip()
        start = self.start_var.get().strip()
        end = self.end_var.get().strip()

        if not name or not contact or not space_text or not date or not start or not end:
            messagebox.showwarning("Ошибка", "Заполни все поля.")
            return

        try:
            space_id = int(space_text.split(".")[0])
            start_dt = datetime.strptime(f"{date} {start}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{date} {end}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверь дату и время. Формат даты: ГГГГ-ММ-ДД.")
            return

        if end_dt <= start_dt:
            messagebox.showerror("Ошибка", "Окончание должно быть позже начала.")
            return

        if self.has_conflict(space_id, start_dt, end_dt):
            messagebox.showerror("Место занято", "Это место уже забронировано на выбранное время.")
            return

        space = next(s for s in SPACES if s["id"] == space_id)
        booking = {
            "id": self.next_id(),
            "client": name,
            "contact": contact,
            "space_id": space_id,
            "space": space["name"],
            "type": space["type"],
            "date": date,
            "start": start,
            "end": end,
            "price": space["price"],
        }
        self.bookings.append(booking)
        self.save_bookings()
        self.refresh_table()
        self.refresh_stats()
        messagebox.showinfo("Готово", "Бронирование создано.")

    def has_conflict(self, space_id, start_dt, end_dt):
        for b in self.bookings:
            if b["space_id"] != space_id:
                continue
            b_start = datetime.strptime(f'{b["date"]} {b["start"]}', "%Y-%m-%d %H:%M")
            b_end = datetime.strptime(f'{b["date"]} {b["end"]}', "%Y-%m-%d %H:%M")
            if start_dt < b_end and end_dt > b_start:
                return True
        return False

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().lower().strip() if hasattr(self, "search_var") else ""
        type_filter = self.type_filter_var.get() if hasattr(self, "type_filter_var") else "Все"

        filtered = []
        for b in self.bookings:
            if query and query not in b["client"].lower() and query not in b["space"].lower():
                continue
            if type_filter != "Все" and b["type"] != type_filter:
                continue
            filtered.append(b)

        for b in sorted(filtered, key=lambda x: (x["date"], x["start"])):
            self.tree.insert("", "end", iid=str(b["id"]), values=(b["client"], b["space"], b["type"], b["date"], f'{b["start"]} - {b["end"]}', f'{b["price"]} ₸'))

    def refresh_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total = len(self.bookings)
        today_count = sum(1 for b in self.bookings if b["date"] == today)
        income = sum(b["price"] for b in self.bookings)

        self.stat_total.config(text=str(total))
        self.stat_today.config(text=str(today_count))
        self.stat_income.config(text=f"{income} ₸")
        self.stat_spaces.config(text=str(len(SPACES)))

    def delete_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Нет выбора", "Выбери бронь в таблице.")
            return
        booking_id = int(selected[0])
        if not messagebox.askyesno("Удалить", "Удалить выбранное бронирование?"):
            return
        self.bookings = [b for b in self.bookings if b["id"] != booking_id]
        self.save_bookings()
        self.refresh_table()
        self.refresh_stats()

    def next_id(self):
        return 1 if not self.bookings else max(b["id"] for b in self.bookings) + 1

    def load_bookings(self):
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_bookings(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.bookings, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumCoworkingApp(root)
    root.mainloop()
