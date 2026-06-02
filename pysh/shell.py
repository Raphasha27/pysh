"""pysh - A Python-powered shell alternative."""

import os
import sys
import subprocess
import atexit
from pathlib import Path

HISTORY_FILE = Path.home() / ".pysh_history"


class PyShell:
    def __init__(self):
        self.history = []
        self.cwd = Path.cwd()
        self.aliases = {"ll": "ls -la", "..": "cd ..", "q": "exit"}
        self._load_history()

    def _load_history(self):
        if HISTORY_FILE.exists():
            self.history = HISTORY_FILE.read_text().splitlines()[-500:]

    def _save_history(self):
        HISTORY_FILE.write_text("\n".join(self.history[-500:]))

    def _highlight(self, text):
        import re
        text = re.sub(r"(sudo|cd|ls|cat|grep|find|pip|git|python)", lambda m: f"\033[1;36m{m.group(1)}\033[0m", text)
        text = re.sub(r"(\-\w+)", lambda m: f"\033[1;33m{m.group(1)}\033[0m", text)
        text = re.sub(r"(\"[^\"]*\")", lambda m: f"\033[1;32m{m.group(1)}\033[0m", text)
        return text

    def _suggest(self, prefix):
        suggestions = [c for c in self.history if c.startswith(prefix)]
        return list(set(suggestions))[:5]

    def run(self):
        print("PySh - Python-powered shell. Type 'help' for commands.")
        while True:
            try:
                prompt = f"\033[1;34m{self.cwd}\033[0m $ "
                cmd = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not cmd:
                continue

            self.history.append(cmd)
            self._save_history()

            if cmd == "exit":
                break
            elif cmd == "help":
                self._show_help()
            elif cmd.startswith("alias "):
                self._set_alias(cmd[6:])
            elif cmd == "history":
                self._show_history()
            elif cmd.startswith("cd "):
                self._change_dir(cmd[3:])
            else:
                self._exec(cmd)

    def _show_help(self):
        print("\033[1;33mPySh Commands:\033[0m")
        print("  help              Show this help")
        print("  exit              Exit shell")
        print("  history           Show command history")
        print("  alias <k>=<v>     Set alias")
        print("  cd <dir>          Change directory")
        print("  <cmd>             Run any system command")

    def _show_history(self):
        for i, h in enumerate(self.history[-20:], 1):
            print(f"  {i:3d}  {h}")

    def _set_alias(self, arg):
        if "=" in arg:
            k, v = arg.split("=", 1)
            self.aliases[k.strip()] = v.strip()
            print(f"Alias set: {k.strip()} -> {v.strip()}")

    def _change_dir(self, path):
        try:
            target = Path(path)
            if not target.is_absolute():
                target = self.cwd / target
            os.chdir(target)
            self.cwd = target.resolve()
        except Exception as e:
            print(f"cd: {e}")

    def _exec(self, cmd):
        alias = self.aliases.get(cmd.split()[0])
        if alias:
            cmd = alias + cmd[len(cmd.split()[0]):]
        try:
            subprocess.run(cmd, shell=True, cwd=self.cwd)
        except Exception as e:
            print(f"error: {e}")


def main():
    shell = PyShell()
    atexit.register(shell._save_history)
    shell.run()


if __name__ == "__main__":
    main()
