import customtkinter
from datetime import datetime, timedelta
import ctypes
import sys
from pathlib import Path
import tkinter.font as tkfont

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  
except Exception:
    pass

def get_base_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  
    return Path(__file__).parent   

base_path = get_base_path()
font_path = base_path / "font" / "Cubic_11.ttf"
_font_added = False
if font_path.exists():
    try:
        added = ctypes.windll.gdi32.AddFontResourceExW(str(font_path), 0x10, None)
        _font_added = bool(added)
    except Exception:
        pass

def get_exec_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent

def parse_time_str(s: str) -> tuple[int, int, int]:
    parts = s.strip().split(":")
    if len(parts) == 2:
        h, m = int(parts[0]), int(parts[1])
        return h, m, 0
    if len(parts) == 3:
        h, m, sec = int(parts[0]), int(parts[1]), int(parts[2])
        return h, m, sec
    raise ValueError("Invalid time format, expected HH:MM or HH:MM:SS")

def load_target_from_config(default_h=18, default_m=0, default_s=0) -> datetime:
    cfg_dir = get_exec_dir()
    cfg_path = cfg_dir / "work_time.txt"
    hour, minute, second = default_h, default_m, default_s
    
    if not cfg_path.exists():
        try:
            with cfg_path.open("w", encoding="utf-8") as f:
                f.write(f"{default_h:02d}:{default_m:02d}")
        except Exception:
            pass  
    try:
        if cfg_path.exists():
            raw = cfg_path.read_text(encoding="utf-8").strip()
            hour, minute, second = parse_time_str(raw)
    except Exception:
        pass  
    return today_target(hour, minute, second)

def today_target(hour: int, minute: int, second: int = 0) -> datetime:
    now = datetime.now()
    t = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
    if t <= now:
        t = t + timedelta(days=1)
    return t

TARGET = load_target_from_config()
five_min_alerted = False

def update():
    global five_min_alerted
    now = datetime.now()
    remaining = int((TARGET - now).total_seconds())
    if remaining < 0:
        label.configure(text="時間到！", text_color="white")
    else:
        if remaining <= 300 and not five_min_alerted:
            try:
                root.attributes("-topmost", True)
                label.configure(text_color="orange")
                def _restore():
                    try:
                        root.attributes("-topmost", False)
                        label.configure(text_color="white")
                    except Exception:
                        pass
                root.after(3000, _restore)
            except Exception:
                pass
            five_min_alerted = True

        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60
        label.configure(text=f"{hrs} H {mins} M {secs} S")

    root.after(1000, update)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.title("小工具")

icon_path = base_path / "liver.ico"
if not icon_path.exists():
    icon_path = get_exec_dir() / "liver.ico"
try:
    root.iconbitmap(default=str(icon_path))
except Exception:
    pass
root.attributes("-topmost", True)
root.geometry("300x100+1200+800")  
root.overrideredirect(True)  
root._borderless = True


families = list(tkfont.families(root))
candidates = [name for name in families if ("俐方體11號" in name.lower())]
app_font = candidates[0] if candidates else "微軟正黑體"

label = customtkinter.CTkLabel(root, text="", font=(app_font, 32, "bold"))
label.pack(expand=True, fill="both", padx=6, pady=6)

def _start_move(event):
    if not getattr(root, "_borderless", True):
        return
    if getattr(root, "_dc_block", False):
        return
    root._drag_x = event.x
    root._drag_y = event.y

def _do_move(event):
    if not getattr(root, "_borderless", True):
        return
    if getattr(root, "_dc_block", False):
        return
    x = root.winfo_pointerx() - getattr(root, "_drag_x", 0)
    y = root.winfo_pointery() - getattr(root, "_drag_y", 0)
    root.geometry(f"+{x}+{y}")

def _toggle_border(event=None):
    root._dc_block = True
    new_state = not root.overrideredirect()  
    root.overrideredirect(new_state)
    root.attributes("-topmost", True if new_state else False)
    root._dc_block = False
    return "break"

def _close(event=None):
    try:
        if _font_added and font_path.exists():
            ctypes.windll.gdi32.RemoveFontResourceExW(str(font_path), 0x10, None)
    except Exception:
        pass
    root.destroy()

for w in (root, label):
    w.bind("<Button-1>", _start_move)
    w.bind("<B1-Motion>", _do_move)
    w.bind("<Button-3>", _toggle_border)  

root.protocol("WM_DELETE_WINDOW", _close)

update()
root.mainloop()