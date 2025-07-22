# LOCKER.EXE
/
# LOCKER

**LOCKER** is a full-screen PyQt6 application that opens a given URL and prevents the user from interacting with anything else until a countdown timer ends. It's designed to enforce focus or restrict activity temporarily.

The `watchdog.py` script monitors LOCKER and restarts it if closed too early — unless LOCKER ends normally and creates a `stop` file.

---

## 📁 Files

- `locker.py` – The main app (PyQt6 GUI).
- `locker.exe` – Packaged executable of `locker.py`.
- `watchdog.py` – Keeps `locker.exe` running unless the timer finishes.
- `stop` – Created by `locker.exe` when finished; stops `watchdog.py` from restarting it.

---

## 🚀 How to Use

### 1. Set the URL and Timer (in `locker.py` if building yourself)

```python
url = "https://example.com"
timer_seconds = 60  # Set your timer here
