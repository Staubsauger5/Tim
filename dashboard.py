#!/usr/bin/env python3
"""
Beeindruckendes Terminal-Dashboard mit Live-Animationen
Erstellt mit Claude Code
"""

import time
import sys
import os
import random
from datetime import datetime
import platform
import shutil

class Color:
    """ANSI Farbcodes für Terminal-Output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Bildschirm löschen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_terminal_size():
    """Terminal-Größe ermitteln"""
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def create_box(text, width=60, color=Color.CYAN):
    """Erstellt eine schöne Box um Text"""
    lines = text.split('\n')
    box = []
    box.append(color + '╔' + '═' * (width - 2) + '╗' + Color.END)
    for line in lines:
        padding = width - len(line) - 4
        box.append(color + '║ ' + Color.END + line + ' ' * padding + color + ' ║' + Color.END)
    box.append(color + '╚' + '═' * (width - 2) + '╝' + Color.END)
    return '\n'.join(box)

def animated_title():
    """Animierter Titel mit coolem Effekt"""
    title = """
 ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗
██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
██║     ██║     ███████║██║   ██║██║  ██║█████╗
██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
 ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

    ██████╗ ██████╗ ██████╗ ███████╗
   ██╔════╝██╔═══██╗██╔══██╗██╔════╝
   ██║     ██║   ██║██║  ██║█████╗
   ██║     ██║   ██║██║  ██║██╔══╝
   ╚██████╗╚██████╔╝██████╔╝███████╗
    ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
    """

    colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.HEADER]

    for i in range(3):
        clear_screen()
        color = colors[i % len(colors)]
        print(color + title + Color.END)
        print(Color.BOLD + Color.CYAN + "           Willkommen zum Demo-Dashboard!" + Color.END)
        time.sleep(0.3)

def progress_bar(percentage, width=40, label=""):
    """Erstellt einen animierten Fortschrittsbalken"""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)

    # Farbwahl basierend auf Prozentsatz
    if percentage < 33:
        color = Color.GREEN
    elif percentage < 66:
        color = Color.YELLOW
    else:
        color = Color.RED

    return f"{label:20} [{color}{bar}{Color.END}] {percentage:3}%"

def get_system_info():
    """Sammelt System-Informationen"""
    return {
        'platform': platform.system(),
        'version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor() or "Unknown",
        'python': platform.python_version()
    }

def matrix_rain_effect(duration=3):
    """Matrix-ähnlicher Regen-Effekt"""
    cols, rows = get_terminal_size()
    chars = "01" + "アイウエオカキクケコサシスセソタチツテト"

    # Initialisiere Spalten
    columns = []
    for _ in range(min(cols, 80)):
        columns.append({
            'y': random.randint(-rows, 0),
            'speed': random.randint(1, 3),
            'char': random.choice(chars)
        })

    start_time = time.time()
    while time.time() - start_time < duration:
        clear_screen()

        # Erstelle leeres Gitter
        grid = [[' ' for _ in range(min(cols, 80))] for _ in range(rows)]

        # Update und zeichne Spalten
        for i, col in enumerate(columns):
            if col['y'] >= 0 and col['y'] < rows:
                grid[col['y']][i] = col['char']

            col['y'] += col['speed']
            if col['y'] > rows:
                col['y'] = random.randint(-rows, 0)
                col['char'] = random.choice(chars)

        # Ausgabe
        for row in grid:
            print(Color.GREEN + ''.join(row) + Color.END)

        time.sleep(0.05)

def live_dashboard():
    """Haupt-Dashboard mit Live-Updates"""
    iteration = 0

    try:
        while True:
            clear_screen()
            iteration += 1

            # Header
            print(Color.BOLD + Color.CYAN + "=" * 70 + Color.END)
            print(Color.BOLD + Color.HEADER + "         CLAUDE CODE - LIVE SYSTEM DASHBOARD         " + Color.END)
            print(Color.BOLD + Color.CYAN + "=" * 70 + Color.END)
            print()

            # Zeit und Datum
            now = datetime.now()
            print(f"{Color.YELLOW}⏰ Zeit:{Color.END} {now.strftime('%H:%M:%S')}  "
                  f"{Color.YELLOW}📅 Datum:{Color.END} {now.strftime('%d.%m.%Y')}")
            print()

            # System Info
            info = get_system_info()
            print(Color.BOLD + Color.GREEN + "🖥️  SYSTEM INFORMATION" + Color.END)
            print(Color.CYAN + "─" * 70 + Color.END)
            print(f"  Platform:     {Color.BLUE}{info['platform']}{Color.END}")
            print(f"  Architektur:  {Color.BLUE}{info['architecture']}{Color.END}")
            print(f"  Python:       {Color.BLUE}{info['python']}{Color.END}")
            print()

            # Simulierte Metriken mit animierten Balken
            print(Color.BOLD + Color.GREEN + "📊 LIVE METRIKEN" + Color.END)
            print(Color.CYAN + "─" * 70 + Color.END)

            # Simulierte Werte die sich ändern
            cpu = 20 + abs(30 * __import__('math').sin(iteration * 0.3))
            memory = 45 + abs(20 * __import__('math').sin(iteration * 0.2))
            disk = 65 + abs(15 * __import__('math').sin(iteration * 0.1))
            network = random.randint(10, 95)

            print("  " + progress_bar(int(cpu), 45, "CPU Auslastung"))
            print("  " + progress_bar(int(memory), 45, "Speicher"))
            print("  " + progress_bar(int(disk), 45, "Festplatte"))
            print("  " + progress_bar(network, 45, "Netzwerk"))
            print()

            # Statistiken
            print(Color.BOLD + Color.GREEN + "📈 STATISTIKEN" + Color.END)
            print(Color.CYAN + "─" * 70 + Color.END)
            print(f"  Iterationen:  {Color.YELLOW}{iteration}{Color.END}")
            print(f"  Updates/Sek:  {Color.YELLOW}~2{Color.END}")
            print(f"  Uptime:       {Color.YELLOW}{iteration // 2}s{Color.END}")
            print()

            # Animierte Spinner
            spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            spin_char = spinner[iteration % len(spinner)]

            print(Color.BOLD + Color.CYAN + "=" * 70 + Color.END)
            print(f"{Color.GREEN}{spin_char}{Color.END} Live-Updates aktiv... "
                  f"(Drücke {Color.BOLD}Ctrl+C{Color.END} zum Beenden)")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Dashboard beendet. Auf Wiedersehen!{Color.END}\n")

def main():
    """Hauptprogramm"""
    try:
        # Willkommens-Animation
        animated_title()
        time.sleep(1)

        # Matrix-Effekt
        clear_screen()
        print(Color.GREEN + Color.BOLD + "Initialisiere Matrix-Effekt..." + Color.END)
        time.sleep(1)
        matrix_rain_effect(3)

        # Lade-Animation
        clear_screen()
        print(Color.CYAN + Color.BOLD + "Lade Dashboard...\n" + Color.END)
        for i in range(101):
            print(f"\r  {progress_bar(i, 50, 'Fortschritt')}", end='', flush=True)
            time.sleep(0.02)
        print("\n")
        time.sleep(0.5)

        # Starte Dashboard
        live_dashboard()

    except Exception as e:
        print(f"{Color.RED}Fehler: {e}{Color.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
