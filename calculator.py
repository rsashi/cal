"""
Simple Calculator — Tkinter
============================
✅ Works with Python 3.14 (built-in, NO pip install needed)
✅ Runs on Windows, macOS, Linux
✅ Package as Android APK via Google Colab (see BUILD_INSTRUCTIONS.md)

Run instantly:
    python calculator.py
"""

import tkinter as tk
from tkinter import font as tkfont


# ── Colors ────────────────────────────────────────────────────────────────────
BG       = "#0D0D0D"
C_NUM    = "#333333"
C_FUNC   = "#A5A5A5"
C_OPS    = "#FF9F0A"
C_EQUAL  = "#FF9F0A"
TXT_W    = "#FFFFFF"
TXT_B    = "#1A1A1A"
TXT_MUTE = "#888888"
HOVER_N  = "#505050"
HOVER_F  = "#C8C8C8"
HOVER_O  = "#FFB733"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Center window on screen
        w, h = 380, 620
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        # ── State ─────────────────────────────────────────────────────────────
        self._current   = ""
        self._operator  = ""
        self._first_op  = None
        self._new_input = False
        self._last_res  = ""

        self._build_ui()
        self._bind_keyboard()

    # ── UI Construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # Expression label
        self.var_expr = tk.StringVar(value="")
        tk.Label(
            self, textvariable=self.var_expr,
            bg=BG, fg=TXT_MUTE,
            font=("Helvetica", 16),
            anchor="e", padx=16,
        ).pack(fill="x", pady=(20, 0))

        # Main display
        self.var_display = tk.StringVar(value="0")
        self.lbl_display = tk.Label(
            self, textvariable=self.var_display,
            bg=BG, fg=TXT_W,
            font=("Helvetica", 56, "bold"),
            anchor="e", padx=16,
        )
        self.lbl_display.pack(fill="x", pady=(0, 12))

        # Divider
        tk.Frame(self, bg="#222222", height=1).pack(fill="x")

        # Button grid
        pad = tk.Frame(self, bg=BG, pady=10, padx=10)
        pad.pack(fill="both", expand=True)

        rows = [
            [("AC",  C_FUNC, TXT_B, HOVER_F, self._clear),
             ("+/-", C_FUNC, TXT_B, HOVER_F, self._toggle),
             ("%",   C_FUNC, TXT_B, HOVER_F, self._percent),
             ("÷",   C_OPS,  TXT_W, HOVER_O, lambda: self._op("÷"))],

            [("7", C_NUM, TXT_W, HOVER_N, lambda: self._num("7")),
             ("8", C_NUM, TXT_W, HOVER_N, lambda: self._num("8")),
             ("9", C_NUM, TXT_W, HOVER_N, lambda: self._num("9")),
             ("×", C_OPS, TXT_W, HOVER_O, lambda: self._op("×"))],

            [("4", C_NUM, TXT_W, HOVER_N, lambda: self._num("4")),
             ("5", C_NUM, TXT_W, HOVER_N, lambda: self._num("5")),
             ("6", C_NUM, TXT_W, HOVER_N, lambda: self._num("6")),
             ("−", C_OPS, TXT_W, HOVER_O, lambda: self._op("−"))],

            [("1", C_NUM, TXT_W, HOVER_N, lambda: self._num("1")),
             ("2", C_NUM, TXT_W, HOVER_N, lambda: self._num("2")),
             ("3", C_NUM, TXT_W, HOVER_N, lambda: self._num("3")),
             ("+", C_OPS, TXT_W, HOVER_O, lambda: self._op("+"))],

            [("⌫", C_NUM, TXT_W, HOVER_N, self._back),
             ("0", C_NUM, TXT_W, HOVER_N, lambda: self._num("0")),
             (".", C_NUM, TXT_W, HOVER_N, lambda: self._num(".")),
             ("=", C_EQUAL, TXT_W, HOVER_O, self._equals)],
        ]

        for r, row in enumerate(rows):
            pad.rowconfigure(r, weight=1, minsize=90)
            for c, (text, bg, fg, hover, cmd) in enumerate(row):
                pad.columnconfigure(c, weight=1)
                self._make_btn(pad, text, bg, fg, hover, cmd, r, c)

    def _make_btn(self, parent, text, bg, fg, hover, cmd, row, col):
        """Create a rounded-look button using Canvas."""
        frame = tk.Frame(parent, bg=BG, padx=5, pady=5)
        frame.grid(row=row, column=col, sticky="nsew")

        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def draw(color):
            canvas.delete("all")
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            if w < 4 or h < 4:
                return
            r = min(w, h) // 2
            # Draw filled rounded rectangle (circle for square buttons)
            canvas.create_oval(0, 0, w, h, fill=color, outline=color)
            canvas.create_text(
                w // 2, h // 2,
                text=text, fill=fg,
                font=("Helvetica", 22 if len(text) > 1 else 26, "bold" if text in ("AC", "+/-", "%") else "normal"),
                anchor="center"
            )

        def on_enter(e):
            draw(hover)
            canvas.configure(cursor="hand2")

        def on_leave(e):
            draw(bg)

        def on_click(e):
            draw(hover)
            frame.after(100, lambda: draw(bg))
            cmd()

        canvas.bind("<Configure>", lambda e: draw(bg))
        canvas.bind("<Enter>",     on_enter)
        canvas.bind("<Leave>",     on_leave)
        canvas.bind("<Button-1>",  on_click)

    # ── Keyboard support ─────────────────────────────────────────────────────
    def _bind_keyboard(self):
        for k in "0123456789.":
            self.bind(k, lambda e, v=k: self._num(v))
        self.bind("+",        lambda e: self._op("+"))
        self.bind("-",        lambda e: self._op("−"))
        self.bind("*",        lambda e: self._op("×"))
        self.bind("/",        lambda e: self._op("÷"))
        self.bind("<Return>", lambda e: self._equals())
        self.bind("<BackSpace>", lambda e: self._back())
        self.bind("c",        lambda e: self._clear())
        self.bind("C",        lambda e: self._clear())
        self.bind("%",        lambda e: self._percent())

    # ── Display helpers ───────────────────────────────────────────────────────
    def _fmt(self, value):
        if isinstance(value, float) and value == int(value) and abs(value) < 1e12:
            return str(int(value))
        return f"{value:.10g}"

    def _set_display(self, text):
        t = str(text)
        size = 56 if len(t) <= 7 else (40 if len(t) <= 11 else 28)
        self.lbl_display.config(font=("Helvetica", size, "bold"))
        self.var_display.set(t)

    def _calculate(self):
        if not self._operator or not self._current:
            return
        try:
            second = float(self._current)
            if   self._operator == "+": result = self._first_op + second
            elif self._operator == "−": result = self._first_op - second
            elif self._operator == "×": result = self._first_op * second
            elif self._operator == "÷":
                if second == 0:
                    self._set_display("Error")
                    self._current = ""
                    return
                result = self._first_op / second
            else:
                return
            fmt = self._fmt(result)
            self._set_display(fmt)
            self._current  = fmt
            self._first_op = result
        except Exception:
            self._set_display("Error")
            self._current = ""

    # ── Button handlers ───────────────────────────────────────────────────────
    def _num(self, v):
        if self._new_input:
            self._current   = ""
            self._new_input = False
        if v == "." and "." in self._current:
            return
        if not self._current and v == ".":
            self._current = "0."
        elif self._current == "0" and v != ".":
            self._current = v
        else:
            self._current += v
        self._set_display(self._current)

    def _op(self, op):
        if self._current:
            if self._operator and not self._new_input:
                self._calculate()
                self._first_op = float(self.var_display.get())
            else:
                self._first_op = float(self._current)
            self._operator  = op
            self.var_expr.set(f"{self._fmt(self._first_op)} {op}")
            self._new_input = True
        elif self._last_res:
            self._first_op  = float(self._last_res)
            self._operator  = op
            self.var_expr.set(f"{self._fmt(self._first_op)} {op}")
            self._new_input = True

    def _equals(self):
        if not self._operator or not self._current:
            return
        expr = f"{self.var_expr.get()} {self._current} ="
        self._calculate()
        self.var_expr.set(expr)
        self._last_res  = self._current
        self._operator  = ""
        self._new_input = True

    def _clear(self):
        self._current   = ""
        self._operator  = ""
        self._first_op  = None
        self._new_input = False
        self._last_res  = ""
        self._set_display("0")
        self.var_expr.set("")

    def _back(self):
        if self._new_input:
            return
        if len(self._current) > 1:
            self._current = self._current[:-1]
            self._set_display(self._current)
        elif self._current:
            self._current = ""
            self._set_display("0")

    def _percent(self):
        try:
            val = float(self._current)
            self._current = self._fmt(val / 100)
            self._set_display(self._current)
        except Exception:
            pass

    def _toggle(self):
        try:
            val = float(self._current)
            self._current = self._fmt(-val)
            self._set_display(self._current)
        except Exception:
            pass


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
