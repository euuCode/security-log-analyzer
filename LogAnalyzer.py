import sqlite3
import re
from datetime import datetime
import customtkinter as ctk
import os
import tkinter as tk  

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class LogAnalyzer:
    def __init__(self):
        self.conn = sqlite3.connect('security_logs.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                ip TEXT,
                event TEXT,
                risk_level INTEGER
            )
        ''')
        self.conn.commit()

    def analyze_log(self, log_line):
        if "failed login" in log_line.lower():
            ip = re.search(r'\d+\.\d+\.\d+\.\d+', log_line)
            if ip:
                ip = ip.group()
                risk = 50
                event = "Tentativa de login falhou"
            else:
                risk = 20
                event = "Log suspeito, sem IP"
        else:
            return

        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO logs (timestamp, ip, event, risk_level) 
            VALUES (?, ?, ?, ?)
        ''', (timestamp, ip or "N/A", event, risk))
        self.conn.commit()

    def get_high_risk_logs(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM logs WHERE risk_level >= 50')
        return cursor.fetchall()

    def get_all_logs(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM logs')
        return cursor.fetchall()

class LogAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Analyzer - by euuCode")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.main_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#2b2b2b")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Log Analyzer",
                                        font=("Helvetica", 28, "bold"), text_color="#4CAF50")
        self.title_label.pack(pady=15)

        self.log_entry = ctk.CTkTextbox(self.main_frame, width=600, height=200,
                                        font=("Consolas", 12), corner_radius=10, fg_color="#3a3a3a",
                                        text_color="#e0e0e0", border_width=1, border_color="#4CAF50")
        self.log_entry.pack(pady=15)

        self.button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#2b2b2b")
        self.button_frame.pack(pady=10)

        self.analyze_button = ctk.CTkButton(self.button_frame, text="Analisar Logs",
                                            command=self.analyze, font=("Helvetica", 16, "bold"),
                                            corner_radius=10, height=40, fg_color="#4CAF50",
                                            hover_color="#45a049")
        self.analyze_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Limpar",
                                          command=self.clear, font=("Helvetica", 16, "bold"),
                                          corner_radius=10, height=40, fg_color="#f44336",
                                          hover_color="#d32f2f")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.result_text = ctk.CTkTextbox(self.main_frame, width=600, height=150,
                                          font=("Consolas", 12), corner_radius=10, fg_color="#3a3a3a",
                                          text_color="#e0e0e0", border_width=1, border_color="#4CAF50")
        self.result_text.pack(pady=15)

        self.export_button = ctk.CTkButton(self.main_frame, text="Exportar Relatório",
                                           command=self.export_report, font=("Helvetica", 16, "bold"),
                                           corner_radius=10, height=40, fg_color="#2196F3",
                                           hover_color="#1976D2")
        self.export_button.pack(pady=10)

        self.analyzer = LogAnalyzer()

    def analyze(self):
        self.result_text.delete("0.0", "end")
        logs = self.log_entry.get("0.0", "end").strip().split("\n")
        for log in logs:
            if log.strip():
                self.analyzer.analyze_log(log)
        high_risk = self.analyzer.get_high_risk_logs()
        all_logs = self.analyzer.get_all_logs()
        
        self.result_text.insert("end", "[*] Análise Concluída\n\n")
        self.result_text.insert("end", "Logs de Alto Risco (Risco >= 50):\n")
        for log in high_risk:
            self.result_text.insert("end", f"- {log}\n", "high_risk")
        self.result_text.insert("end", "\nTodos os Logs Registrados:\n")
        for log in all_logs:
            self.result_text.insert("end", f"- {log}\n", "normal")
        
        self.result_text.tag_config("high_risk", foreground="#ff4444")
        self.result_text.tag_config("normal", foreground="#e0e0e0")

    def clear(self):
        self.log_entry.delete("0.0", "end")
        self.result_text.delete("0.0", "end")

    def export_report(self):
        desktop_path = os.path.expanduser("~") + "/Desktop/security_log_report.txt"
        with open(desktop_path, "w", encoding="utf-8") as f:
            f.write("=== Relatório de Logs de Segurança ===\n")
            f.write("Data: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            f.write(self.result_text.get("0.0", "end"))
        self.result_text.insert("end", f"\n[✓] Relatório exportado para: {desktop_path}\n", "success")
        self.result_text.tag_config("success", foreground="#00FF00")

def main():
    root = ctk.CTk()
    app = LogAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()