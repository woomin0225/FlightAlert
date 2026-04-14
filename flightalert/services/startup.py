import os
import sys

try:
    import winreg
except Exception:  # pragma: no cover - non-Windows fallback
    winreg = None


APP_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "FlightAlert"


def startup_supported():
    return winreg is not None and os.name == "nt"


def is_startup_enabled():
    if not startup_supported():
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_RUN_KEY, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            return bool(value)
    except FileNotFoundError:
        return False
    except OSError:
        return False


def enable_startup():
    if not startup_supported():
        return False, "이 환경에서는 자동 실행 설정을 지원하지 않습니다."
    command = _startup_command()
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, command)
        return True, "컴퓨터 시작 시 자동 실행이 켜졌습니다."
    except OSError as exc:
        return False, f"자동 실행 등록 실패: {exc}"


def disable_startup():
    if not startup_supported():
        return False, "이 환경에서는 자동 실행 설정을 지원하지 않습니다."
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_NAME)
        return True, "자동 실행이 꺼졌습니다."
    except FileNotFoundError:
        return True, "자동 실행이 이미 꺼져 있습니다."
    except OSError as exc:
        return False, f"자동 실행 해제 실패: {exc}"


def _startup_command():
    if getattr(sys, "frozen", False):
        exe_path = sys.executable
        return f'"{exe_path}" --autostart'

    python_exe = sys.executable
    app_launcher = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py")
    return f'"{python_exe}" "{app_launcher}" --autostart'
