import sys
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

try:
    import hid
except ImportError:
    print("Manca il pacchetto hidapi. Installalo con:\n    pip install hidapi")
    sys.exit(1)

VENDOR_ID = 0xFEED
PRODUCT_ID = 0x0001
RAW_USAGE_PAGE = 0xFF60
RAW_USAGE = 0x61
REPORT_LENGTH = 32

MATRIX_ROWS = 5
MATRIX_COLS = 15

KEYCODES = {
    "KC_NO": 0x00,
    "KC_A": 0x04, "KC_B": 0x05, "KC_C": 0x06, "KC_D": 0x07, "KC_E": 0x08,
    "KC_F": 0x09, "KC_G": 0x0A, "KC_H": 0x0B, "KC_I": 0x0C, "KC_J": 0x0D,
    "KC_K": 0x0E, "KC_L": 0x0F, "KC_M": 0x10, "KC_N": 0x11, "KC_O": 0x12,
    "KC_P": 0x13, "KC_Q": 0x14, "KC_R": 0x15, "KC_S": 0x16, "KC_T": 0x17,
    "KC_U": 0x18, "KC_V": 0x19, "KC_W": 0x1A, "KC_X": 0x1B, "KC_Y": 0x1C,
    "KC_Z": 0x1D,
    "KC_1": 0x1E, "KC_2": 0x1F, "KC_3": 0x20, "KC_4": 0x21, "KC_5": 0x22,
    "KC_6": 0x23, "KC_7": 0x24, "KC_8": 0x25, "KC_9": 0x26, "KC_0": 0x27,
    "KC_ENT": 0x28, "KC_ESC": 0x29, "KC_BSPC": 0x2A, "KC_TAB": 0x2B,
    "KC_SPC": 0x2C, "KC_MINS": 0x2D, "KC_EQL": 0x2E, "KC_LBRC": 0x2F,
    "KC_RBRC": 0x30, "KC_BSLS": 0x31, "KC_SCLN": 0x33, "KC_QUOT": 0x34,
    "KC_GRV": 0x35, "KC_COMM": 0x36, "KC_DOT": 0x37, "KC_SLSH": 0x38,
    "KC_CAPS": 0x39,
    "KC_F1": 0x3A, "KC_F2": 0x3B, "KC_F3": 0x3C, "KC_F4": 0x3D,
    "KC_F5": 0x3E, "KC_F6": 0x3F, "KC_F7": 0x40, "KC_F8": 0x41,
    "KC_F9": 0x42, "KC_F10": 0x43, "KC_F11": 0x44, "KC_F12": 0x45,
    "KC_PSCR": 0x46, "KC_INS": 0x49, "KC_HOME": 0x4A, "KC_PGUP": 0x4B,
    "KC_DEL": 0x4C, "KC_END": 0x4D, "KC_PGDN": 0x4E,
    "KC_RGHT": 0x4F, "KC_LEFT": 0x50, "KC_DOWN": 0x51, "KC_UP": 0x52,
    "KC_LCTL": 0xE0, "KC_LSFT": 0xE1, "KC_LALT": 0xE2, "KC_LGUI": 0xE3,
    "KC_RCTL": 0xE4, "KC_RSFT": 0xE5, "KC_RALT": 0xE6, "KC_RGUI": 0xE7,
}


def find_raw_hid_device():
    for d in hid.enumerate(VENDOR_ID, PRODUCT_ID):
        if d.get("usage_page") == RAW_USAGE_PAGE and d.get("usage") == RAW_USAGE:
            return d["path"]
    return None


class Controller:
    def __init__(self):
        self.device = None

    def connect(self):
        path = find_raw_hid_device()
        if path is None:
            raise RuntimeError(
                "Tastiera non trovata. Controlla che sia collegata, che il "
                "firmware con RAW_ENABLE sia flashato, e che VID/PID "
                f"({VENDOR_ID:#06x}:{PRODUCT_ID:#06x}) combacino con info.json."
            )
        self.device = hid.device()
        self.device.open_path(path)

    def _send(self, payload):
        if self.device is None:
            raise RuntimeError("Non connesso.")
        report = bytes([0]) + payload + bytes(REPORT_LENGTH - len(payload))
        self.device.write(report)

    def set_color(self, r, g, b):
        self._send(bytes([0x01, r, g, b]))

    def remap_key(self, row, col, keycode):
        self._send(bytes([0x02, row, col, (keycode >> 8) & 0xFF, keycode & 0xFF]))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HexKey60 Controller")
        self.resizable(False, False)
        self.controller = Controller()

        self._build_ui()
        self._try_connect()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        self.status_var = tk.StringVar(value="Non connesso")
        ttk.Label(self, textvariable=self.status_var, foreground="red").grid(
            row=0, column=0, columnspan=3, sticky="w", **pad
        )
        ttk.Button(self, text="Riconnetti", command=self._try_connect).grid(
            row=0, column=3, **pad
        )

        color_frame = ttk.LabelFrame(self, text="Colore LED")
        color_frame.grid(row=1, column=0, columnspan=4, sticky="we", **pad)

        self.color_preview = tk.Canvas(color_frame, width=40, height=24, bg="white")
        self.color_preview.grid(row=0, column=0, padx=10, pady=10)

        ttk.Button(
            color_frame, text="Scegli colore...", command=self._pick_color
        ).grid(row=0, column=1, padx=10, pady=10)

        remap_frame = ttk.LabelFrame(self, text="Rimappa un tasto")
        remap_frame.grid(row=2, column=0, columnspan=4, sticky="we", **pad)

        ttk.Label(remap_frame, text="Riga (0-4):").grid(row=0, column=0, **pad)
        self.row_var = tk.IntVar(value=0)
        ttk.Spinbox(
            remap_frame, from_=0, to=MATRIX_ROWS - 1, textvariable=self.row_var, width=5
        ).grid(row=0, column=1, **pad)

        ttk.Label(remap_frame, text="Colonna (0-14):").grid(row=0, column=2, **pad)
        self.col_var = tk.IntVar(value=0)
        ttk.Spinbox(
            remap_frame, from_=0, to=MATRIX_COLS - 1, textvariable=self.col_var, width=5
        ).grid(row=0, column=3, **pad)

        ttk.Label(remap_frame, text="Nuovo tasto:").grid(row=1, column=0, **pad)
        self.keycode_var = tk.StringVar(value="KC_A")
        keycode_combo = ttk.Combobox(
            remap_frame,
            textvariable=self.keycode_var,
            values=sorted(KEYCODES.keys()),
            width=15,
            state="readonly",
        )
        keycode_combo.grid(row=1, column=1, columnspan=2, sticky="w", **pad)

        ttk.Button(remap_frame, text="Applica", command=self._apply_remap).grid(
            row=1, column=3, **pad
        )

        note = (
            "Nota: la rimappatura e il colore sono persistenti,\n"
            "salvati nell'EEPROM emulata del Pico."
        )
        ttk.Label(self, text=note, foreground="gray").grid(
            row=3, column=0, columnspan=4, sticky="w", **pad
        )

    def _try_connect(self):
        try:
            self.controller.connect()
            self.status_var.set("Connesso")
        except Exception as e:
            self.status_var.set("Non connesso")
            messagebox.showerror("Connessione fallita", str(e))

    def _pick_color(self):
        result = colorchooser.askcolor(title="Scegli il colore dei LED")
        if result is None or result[0] is None:
            return
        r, g, b = (int(v) for v in result[0])
        hex_color = result[1]
        self.color_preview.configure(bg=hex_color)
        try:
            self.controller.set_color(r, g, b)
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def _apply_remap(self):
        row = self.row_var.get()
        col = self.col_var.get()
        name = self.keycode_var.get()
        keycode = KEYCODES.get(name)
        if keycode is None:
            messagebox.showerror("Errore", f"Keycode sconosciuto: {name}")
            return
        try:
            self.controller.remap_key(row, col, keycode)
        except Exception as e:
            messagebox.showerror("Errore", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
