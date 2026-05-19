# -*- coding: utf-8 -*-
"""
Дневник-книжка + календарь + будильники

Функции:
- интерфейс в стиле открытой книжки
- запись дня
- задания на сегодня
- календарь на текущий год
- заметка на любой выбранный день
- будильник/напоминание на любой день текущего года
- локальное сохранение в diary_data.json

Важно:
Будильник сработает, если программа в этот момент открыта.

Запуск:
python diary_book_calendar_app.py
"""

import json
import calendar
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime, date


APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "diary_data.json"


class DiaryBookCalendarApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Дневник — книжка")
        self.root.geometry("1180x760")
        self.root.minsize(980, 660)

        self.today = date.today()
        self.today_key = self.today.isoformat()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_date = self.today

        self.data = self.load_data()
        self.already_alerted = set()

        self.colors = {
            "desk": "#7b4b2a",
            "cover": "#5b2f22",
            "cover_light": "#7b4432",
            "page": "#fff3d6",
            "page_shadow": "#e6cf9e",
            "paper_line": "#e4cfa2",
            "ink": "#2c241b",
            "muted": "#7a6045",
            "accent": "#9c5a2e",
            "accent_dark": "#6f3d22",
            "danger": "#a83232",
            "done": "#9d8a73",
            "selected": "#d79b5b",
            "today": "#ffd37a",
        }

        self.root.configure(bg=self.colors["desk"])
        self.build_ui()
        self.load_today()
        self.draw_calendar()
        self.load_selected_day()
        self.update_clock()
        self.check_alarms()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_data(self):
        if not DATA_FILE.exists():
            return {}
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            messagebox.showwarning("Ошибка", "Не получилось прочитать diary_data.json. Будет создан новый файл.")
            return {}

    def day_data(self, key):
        return self.data.setdefault(key, {
            "note": "",
            "tasks": [],
            "day_note": "",
            "alarms": []
        })

    def save_data(self):
        today = self.day_data(self.today_key)
        today["note"] = self.note_text.get("1.0", "end-1c")
        today["tasks"] = self.get_tasks()
        today["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        selected_key = self.selected_date.isoformat()
        selected = self.day_data(selected_key)
        selected["day_note"] = self.day_note_text.get("1.0", "end-1c")

        DATA_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def build_ui(self):
        outer = tk.Frame(self.root, bg=self.colors["desk"])
        outer.pack(fill="both", expand=True, padx=24, pady=18)

        top = tk.Frame(outer, bg=self.colors["desk"])
        top.pack(fill="x", pady=(0, 12))

        tk.Label(
            top,
            text="Мой дневник",
            bg=self.colors["desk"],
            fg="#fff4df",
            font=("Georgia", 28, "bold")
        ).pack(side="left")

        self.clock_label = tk.Label(
            top,
            bg=self.colors["desk"],
            fg="#f4d9ad",
            font=("Georgia", 14)
        )
        self.clock_label.pack(side="right", pady=12)

        cover = tk.Frame(
            outer,
            bg=self.colors["cover"],
            highlightthickness=3,
            highlightbackground=self.colors["cover_light"]
        )
        cover.pack(fill="both", expand=True)

        book = tk.Frame(cover, bg=self.colors["cover"])
        book.pack(fill="both", expand=True, padx=18, pady=18)

        left_shadow = tk.Frame(book, bg=self.colors["page_shadow"])
        left_shadow.pack(side="left", fill="both", expand=True, padx=(0, 6), pady=(2, 10))

        self.left_page = tk.Frame(left_shadow, bg=self.colors["page"], highlightthickness=1, highlightbackground="#d9b977")
        self.left_page.pack(fill="both", expand=True, padx=(0, 5), pady=(0, 5))

        spine = tk.Frame(book, bg=self.colors["accent_dark"], width=18)
        spine.pack(side="left", fill="y")
        tk.Frame(spine, bg="#3f2418", width=4).pack(side="left", fill="y", padx=(6, 0))

        right_shadow = tk.Frame(book, bg=self.colors["page_shadow"])
        right_shadow.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=(2, 10))

        self.right_page = tk.Frame(right_shadow, bg=self.colors["page"], highlightthickness=1, highlightbackground="#d9b977")
        self.right_page.pack(fill="both", expand=True, padx=(5, 0), pady=(0, 5))

        self.build_left_page()
        self.build_right_page()

        self.status_label = tk.Label(
            outer,
            text="",
            bg=self.colors["desk"],
            fg="#f4d9ad",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

    def book_button(self, parent, text, command, width=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=self.colors["accent"],
            fg="#fff4df",
            activebackground=self.colors["accent_dark"],
            activeforeground="#fff4df",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=6
        )

    def draw_line(self, parent):
        canvas = tk.Canvas(parent, bg=self.colors["page"], highlightthickness=0, height=12)
        canvas.pack(fill="x", padx=22)
        canvas.create_line(0, 8, 1200, 8, fill=self.colors["paper_line"])

    def build_left_page(self):
        page = self.left_page

        tk.Label(page, text="Запись дня", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 21, "bold")).pack(anchor="w", padx=24, pady=(20, 0))
        tk.Label(page, text=f"Сегодня: {datetime.now().strftime('%d.%m.%Y')}", bg=self.colors["page"], fg=self.colors["muted"], font=("Georgia", 11, "italic")).pack(anchor="w", padx=26, pady=(0, 7))
        self.draw_line(page)

        self.note_text = tk.Text(
            page,
            wrap="word",
            bg=self.colors["page"],
            fg=self.colors["ink"],
            insertbackground=self.colors["ink"],
            relief="flat",
            font=("Georgia", 12),
            padx=10,
            pady=8,
            undo=True,
            height=8
        )
        self.note_text.pack(fill="both", expand=True, padx=24, pady=(10, 8))

        btns = tk.Frame(page, bg=self.colors["page"])
        btns.pack(fill="x", padx=24, pady=(0, 12))
        self.book_button(btns, "Сохранить", self.manual_save).pack(side="left")
        self.book_button(btns, "Очистить", self.clear_note).pack(side="left", padx=8)

        tk.Label(page, text="Задания сегодня", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 17, "bold")).pack(anchor="w", padx=24, pady=(0, 2))

        add = tk.Frame(page, bg=self.colors["page"])
        add.pack(fill="x", padx=24, pady=(6, 6))

        self.task_entry = tk.Entry(
            add,
            bg="#fff8e6",
            fg=self.colors["ink"],
            insertbackground=self.colors["ink"],
            relief="flat",
            font=("Georgia", 11),
            highlightthickness=1,
            highlightbackground="#d4b16f",
            highlightcolor=self.colors["accent"]
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=7)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.book_button(add, "+", self.add_task, width=4).pack(side="left", padx=(8, 0))

        list_wrap = tk.Frame(page, bg=self.colors["page"])
        list_wrap.pack(fill="both", expand=True, padx=24, pady=(0, 10))

        self.tasks_canvas = tk.Canvas(list_wrap, bg=self.colors["page"], highlightthickness=0)
        self.tasks_canvas.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(list_wrap, command=self.tasks_canvas.yview)
        scroll.pack(side="right", fill="y")

        self.tasks_frame = tk.Frame(self.tasks_canvas, bg=self.colors["page"])
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scroll.set)

        self.tasks_frame.bind("<Configure>", lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))

        task_btns = tk.Frame(page, bg=self.colors["page"])
        task_btns.pack(fill="x", padx=24, pady=(0, 18))
        self.book_button(task_btns, "Удалить выполненные", self.delete_done).pack(side="left")
        self.book_button(task_btns, "Очистить всё", self.clear_tasks).pack(side="left", padx=8)

    def build_right_page(self):
        page = self.right_page

        header = tk.Frame(page, bg=self.colors["page"])
        header.pack(fill="x", padx=22, pady=(20, 0))

        self.month_title = tk.Label(header, text="", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 20, "bold"))
        self.month_title.pack(side="left")

        nav = tk.Frame(header, bg=self.colors["page"])
        nav.pack(side="right")
        self.book_button(nav, "←", self.prev_month, width=3).pack(side="left")
        self.book_button(nav, "Сегодня", self.go_today).pack(side="left", padx=6)
        self.book_button(nav, "→", self.next_month, width=3).pack(side="left")

        tk.Label(page, text="Календарь, заметка и будильник", bg=self.colors["page"], fg=self.colors["muted"], font=("Georgia", 11, "italic")).pack(anchor="w", padx=24, pady=(0, 7))
        self.draw_line(page)

        self.calendar_frame = tk.Frame(page, bg=self.colors["page"])
        self.calendar_frame.pack(fill="x", padx=22, pady=(8, 8))

        self.selected_label = tk.Label(page, text="", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 14, "bold"))
        self.selected_label.pack(anchor="w", padx=24, pady=(4, 3))

        self.day_note_text = tk.Text(
            page,
            wrap="word",
            bg="#fff8e6",
            fg=self.colors["ink"],
            insertbackground=self.colors["ink"],
            relief="flat",
            font=("Georgia", 11),
            height=4,
            padx=8,
            pady=7,
            highlightthickness=1,
            highlightbackground="#d4b16f",
            highlightcolor=self.colors["accent"]
        )
        self.day_note_text.pack(fill="x", padx=24, pady=(0, 8))

        alarm_box = tk.Frame(page, bg=self.colors["page"])
        alarm_box.pack(fill="x", padx=24, pady=(0, 8))

        tk.Label(alarm_box, text="Будильник:", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 11, "bold")).pack(side="left")

        self.alarm_hour = tk.Spinbox(alarm_box, from_=0, to=23, width=3, format="%02.0f", font=("Georgia", 10))
        self.alarm_hour.pack(side="left", padx=(8, 2))

        tk.Label(alarm_box, text=":", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 11, "bold")).pack(side="left")

        self.alarm_minute = tk.Spinbox(alarm_box, from_=0, to=59, width=3, format="%02.0f", font=("Georgia", 10))
        self.alarm_minute.pack(side="left", padx=(2, 8))

        self.alarm_text = tk.Entry(
            alarm_box,
            bg="#fff8e6",
            fg=self.colors["ink"],
            insertbackground=self.colors["ink"],
            relief="flat",
            font=("Georgia", 10),
            highlightthickness=1,
            highlightbackground="#d4b16f",
            highlightcolor=self.colors["accent"]
        )
        self.alarm_text.pack(side="left", fill="x", expand=True, ipady=5)
        self.alarm_text.insert(0, "Напоминание")

        self.book_button(alarm_box, "Добавить", self.add_alarm).pack(side="left", padx=(8, 0))

        tk.Label(page, text="Будильники выбранного дня", bg=self.colors["page"], fg=self.colors["ink"], font=("Georgia", 13, "bold")).pack(anchor="w", padx=24, pady=(0, 2))

        self.alarms_frame = tk.Frame(page, bg=self.colors["page"])
        self.alarms_frame.pack(fill="both", expand=True, padx=24, pady=(0, 14))

        self.book_button(page, "Сохранить заметку выбранного дня", self.manual_save).pack(anchor="w", padx=24, pady=(0, 18))

    def month_name_ru(self, month):
        names = [
            "", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        return names[month]

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_title.config(text=f"{self.month_name_ru(self.current_month)} {self.current_year}")

        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for col, name in enumerate(weekdays):
            tk.Label(
                self.calendar_frame,
                text=name,
                bg=self.colors["page"],
                fg=self.colors["muted"],
                font=("Segoe UI", 9, "bold"),
                width=6
            ).grid(row=0, column=col, padx=2, pady=2)

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.current_year, self.current_month)

        for r, week in enumerate(weeks, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="", bg=self.colors["page"], width=6, height=2).grid(row=r, column=c, padx=2, pady=2)
                    continue

                d = date(self.current_year, self.current_month, day)
                key = d.isoformat()
                day_info = self.data.get(key, {})
                has_note = bool(day_info.get("day_note"))
                has_alarm = bool(day_info.get("alarms"))

                text = str(day)
                if has_note:
                    text += " ✎"
                if has_alarm:
                    text += " ⏰"

                bg = "#fff8e6"
                if d == self.today:
                    bg = self.colors["today"]
                if d == self.selected_date:
                    bg = self.colors["selected"]

                btn = tk.Button(
                    self.calendar_frame,
                    text=text,
                    bg=bg,
                    fg=self.colors["ink"],
                    activebackground=self.colors["selected"],
                    relief="flat",
                    font=("Segoe UI", 9),
                    width=6,
                    height=2,
                    command=lambda chosen=d: self.select_date(chosen)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)

    def select_date(self, chosen):
        self.save_selected_note_only()
        self.selected_date = chosen
        self.draw_calendar()
        self.load_selected_day()

    def prev_month(self):
        self.save_selected_note_only()
        if self.current_month == 1:
            return
        self.current_month -= 1
        self.draw_calendar()

    def next_month(self):
        self.save_selected_note_only()
        if self.current_month == 12:
            return
        self.current_month += 1
        self.draw_calendar()

    def go_today(self):
        self.save_selected_note_only()
        self.current_month = self.today.month
        self.selected_date = self.today
        self.draw_calendar()
        self.load_selected_day()

    def save_selected_note_only(self):
        if hasattr(self, "day_note_text"):
            key = self.selected_date.isoformat()
            self.day_data(key)["day_note"] = self.day_note_text.get("1.0", "end-1c")
            DATA_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_selected_day(self):
        key = self.selected_date.isoformat()
        day_info = self.day_data(key)

        self.selected_label.config(text=f"Выбранный день: {self.selected_date.strftime('%d.%m.%Y')}")

        self.day_note_text.delete("1.0", "end")
        self.day_note_text.insert("1.0", day_info.get("day_note", ""))

        self.refresh_alarms_list()

    def add_alarm(self):
        try:
            hour = int(self.alarm_hour.get())
            minute = int(self.alarm_minute.get())
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Время должно быть в формате часы 0-23 и минуты 0-59.")
            return

        text = self.alarm_text.get().strip() or "Напоминание"
        key = self.selected_date.isoformat()

        alarm = {
            "time": f"{hour:02d}:{minute:02d}",
            "text": text,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.day_data(key).setdefault("alarms", []).append(alarm)
        self.save_data()
        self.refresh_alarms_list()
        self.draw_calendar()
        self.status_label.config(text=f"Будильник добавлен на {self.selected_date.strftime('%d.%m.%Y')} {alarm['time']}")

    def refresh_alarms_list(self):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()

        key = self.selected_date.isoformat()
        alarms = self.day_data(key).setdefault("alarms", [])

        if not alarms:
            tk.Label(
                self.alarms_frame,
                text="На этот день будильников нет.",
                bg=self.colors["page"],
                fg=self.colors["muted"],
                font=("Georgia", 11, "italic")
            ).pack(anchor="w", pady=4)
            return

        for index, alarm in enumerate(alarms):
            row = tk.Frame(self.alarms_frame, bg=self.colors["page"])
            row.pack(fill="x", pady=3)

            status = "✓ " if alarm.get("done") else "⏰ "
            label = tk.Label(
                row,
                text=f"{status}{alarm.get('time', '--:--')} — {alarm.get('text', '')}",
                bg=self.colors["page"],
                fg=self.colors["done"] if alarm.get("done") else self.colors["ink"],
                font=("Georgia", 11),
                anchor="w",
                justify="left"
            )
            label.pack(side="left", fill="x", expand=True)

            tk.Button(
                row,
                text="×",
                bg=self.colors["page"],
                fg=self.colors["danger"],
                activebackground=self.colors["page"],
                relief="flat",
                cursor="hand2",
                font=("Segoe UI", 13, "bold"),
                command=lambda i=index: self.delete_alarm(i)
            ).pack(side="right")

    def delete_alarm(self, index):
        key = self.selected_date.isoformat()
        alarms = self.day_data(key).setdefault("alarms", [])
        if 0 <= index < len(alarms):
            alarms.pop(index)
        self.save_data()
        self.refresh_alarms_list()
        self.draw_calendar()

    def check_alarms(self):
        now = datetime.now()
        current_key = now.date().isoformat()
        current_time = now.strftime("%H:%M")

        alarms = self.data.get(current_key, {}).get("alarms", [])
        for index, alarm in enumerate(alarms):
            alarm_id = f"{current_key}-{index}-{alarm.get('time')}"
            if alarm.get("done"):
                continue
            if alarm_id in self.already_alerted:
                continue
            if alarm.get("time") == current_time:
                self.already_alerted.add(alarm_id)
                alarm["done"] = True
                self.save_data()
                messagebox.showinfo(
                    "Будильник",
                    f"{alarm.get('time')} — {alarm.get('text', 'Напоминание')}"
                )
                if self.selected_date.isoformat() == current_key:
                    self.refresh_alarms_list()
                    self.draw_calendar()

        self.root.after(15000, self.check_alarms)

    def load_today(self):
        today = self.day_data(self.today_key)
        self.note_text.delete("1.0", "end")
        self.note_text.insert("1.0", today.get("note", ""))

        for task in today.get("tasks", []):
            self.create_task_row(task.get("text", ""), bool(task.get("done", False)))

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def create_task_row(self, text, done=False):
        text = text.strip()
        if not text:
            return

        row = tk.Frame(self.tasks_frame, bg=self.colors["page"])
        row.pack(fill="x", pady=4)

        var = tk.BooleanVar(value=done)

        tk.Checkbutton(
            row,
            variable=var,
            bg=self.colors["page"],
            activebackground=self.colors["page"],
            command=self.autosave_silent
        ).pack(side="left", padx=(0, 5))

        label = tk.Label(
            row,
            text=text,
            bg=self.colors["page"],
            fg=self.colors["ink"],
            font=("Georgia", 11),
            anchor="w",
            justify="left",
            wraplength=360
        )
        label.pack(side="left", fill="x", expand=True)

        tk.Button(
            row,
            text="×",
            bg=self.colors["page"],
            fg=self.colors["danger"],
            activebackground=self.colors["page"],
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 13, "bold"),
            command=lambda: self.delete_task_row(row)
        ).pack(side="right")

        row.task_text = text
        row.task_var = var

        def refresh(*_):
            if var.get():
                label.config(fg=self.colors["done"], font=("Georgia", 11, "overstrike"))
            else:
                label.config(fg=self.colors["ink"], font=("Georgia", 11))

        var.trace_add("write", refresh)
        refresh()

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        self.create_task_row(text, False)
        self.task_entry.delete(0, "end")
        self.autosave_silent()

    def delete_task_row(self, row):
        row.destroy()
        self.autosave_silent()

    def get_tasks(self):
        tasks = []
        for row in self.tasks_frame.winfo_children():
            if hasattr(row, "task_text") and hasattr(row, "task_var"):
                tasks.append({"text": row.task_text, "done": bool(row.task_var.get())})
        return tasks

    def delete_done(self):
        for row in list(self.tasks_frame.winfo_children()):
            if hasattr(row, "task_var") and row.task_var.get():
                row.destroy()
        self.autosave_silent()

    def clear_tasks(self):
        if self.tasks_frame.winfo_children() and messagebox.askyesno("Очистить задания", "Удалить все задания на сегодня?"):
            for row in list(self.tasks_frame.winfo_children()):
                row.destroy()
            self.autosave_silent()

    def clear_note(self):
        if messagebox.askyesno("Очистить запись", "Очистить запись дня?"):
            self.note_text.delete("1.0", "end")
            self.autosave_silent()

    def manual_save(self):
        self.save_data()
        self.draw_calendar()
        self.status_label.config(text=f"Сохранено: {datetime.now().strftime('%H:%M:%S')}")

    def autosave_silent(self):
        try:
            self.save_data()
            self.status_label.config(text="Автосохранение выполнено")
        except Exception:
            self.status_label.config(text="Ошибка автосохранения")

    def on_close(self):
        try:
            self.save_data()
        finally:
            self.root.destroy()


def main():
    root = tk.Tk()
    DiaryBookCalendarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
