import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os
import webbrowser
from tkinter import *
from scipy import stats

class ResultWindow:
    def __init__(self, parent, text_content):
        self.window = tk.Toplevel(parent)
        self.window.title("Szczegółowe wyniki analizy")
        self.window.geometry("800x600")
        
        # Ustawienie minimalnego rozmiaru okna
        self.window.minsize(600, 400)
        
        # Konfiguracja kolorów
        self.colors = parent.colors
        self.window.configure(bg=self.colors['bg'])
        
        # Kontener główny
        self.main_frame = ttk.Frame(self.window, style='Panel.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Pole tekstowe
        self.text = tk.Text(self.main_frame,
                           font=('Consolas', 11),
                           bg=self.colors['text_bg'],
                           fg=self.colors['text_fg'],
                           wrap=tk.WORD,
                           padx=15,
                           pady=15)
        self.text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame,
                                     orient="vertical",
                                     command=self.text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # Wstawienie tekstu
        if text_content:
            self.text.insert('1.0', text_content)
            self.text.see('1.0')
        
        # Ustawienie stanu tylko do odczytu
        self.text.config(state='disabled')
        
        # Ustawienie okna na wierzchu i fokus
        self.window.transient(parent)
        self.window.focus_set()
        
        # Centrowanie okna względem rodzica
        self.center_window(parent)
    
    def center_window(self, parent):
        """Centruje okno względem okna rodzica."""
        self.window.update_idletasks()
        
        # Pobierz wymiary i pozycję okna rodzica
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Pobierz wymiary okna
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Oblicz pozycję
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        # Ustaw pozycję
        self.window.geometry(f"+{x}+{y}")

class AIDataAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Data Assistant")
        self.root.geometry("1200x800")
        
        # Pozycjonowanie okna
        screen_width = self.root.winfo_screenwidth()
        window_width = 1200
        window_height = 800
        x = (screen_width - window_width) // 2
        y = 20
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Nowoczesna paleta kolorów
        self.colors = {
            'bg': '#1a1a2e',  # Ciemny granatowy (tło)
            'secondary_bg': '#16213e',  # Ciemniejszy niebieski (tło paneli)
            'accent': '#0f3460',  # Akcent niebieski
            'button': '#533483',  # Fioletowy dla przycisków
            'button_hover': '#e94560',  # Czerwony dla hover
            'text_bg': '#f5f5f5',  # Jasny szary
            'text_fg': '#2c2c2c',  # Ciemny szary dla tekstu
            'status_bg': '#16213e',  # Ciemniejszy niebieski
            'dark_bg': '#0a0a0a',  # Ciemne tło dla trybu ciemnego
            'dark_fg': '#00ff00',  # Zielony "hakerski" kolor tekstu
            'light_bg': '#f5f5f5',  # Jasne tło (poprzedni kolor)
            'light_fg': '#2c2c2c'   # Ciemny tekst (poprzedni kolor)
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Inicjalizacja typów wykresów
        self.viz_types = {
            'Mapa korelacji': self.plot_correlation,
            'Wykres rozrzutu': self.plot_scatter,
            'Histogram': self.plot_histogram,
            'Wykres pudełkowy': self.plot_boxplot,
            'Wykres liniowy': self.plot_line,
            'Wykres kołowy': self.plot_pie,
            'Wykres słupkowy': self.plot_bar,
            'Wykres skrzypcowy': self.plot_violin,
            'Mapa cieplna': self.plot_heatmap,
            'Wykres obszarowy': self.plot_area
        }
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Definicje wszystkich stylów
        style.configure('Main.TFrame',
                       background=self.colors['bg'])
        
        style.configure('Panel.TFrame',
                       background=self.colors['secondary_bg'],
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Action.TButton',
                       padding=(15, 8),
                       font=('Segoe UI', 11),
                       background=self.colors['button'],
                       foreground='white',
                       borderwidth=0)
        
        style.map('Action.TButton',
                 background=[('active', self.colors['button_hover'])],
                 foreground=[('active', 'white')])
        
        style.configure('Toggle.TButton',
                       padding=(15, 12),
                       font=('Segoe UI', 12, 'bold'),
                       background=self.colors['button'],
                       foreground='white',
                       borderwidth=0)
        
        style.map('Toggle.TButton',
                 background=[('active', self.colors['button_hover'])],
                 foreground=[('active', 'white')])
        
        style.configure('Generate.TButton',
                       padding=(20, 10),
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0)
        
        style.map('Generate.TButton',
                 background=[('active', self.colors['button_hover'])],
                 foreground=[('active', 'white')])
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       padding=20,
                       background=self.colors['bg'],
                       foreground='white')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       padding=10,
                       background=self.colors['secondary_bg'],
                       foreground='white')
        
        style.configure('Status.TLabel',
                       font=('Segoe UI', 10),
                       background=self.colors['status_bg'],
                       foreground='white',
                       padding=8)
        
        style.configure('Logo.TFrame',
                       background=self.colors['bg'])
        
        style.configure('Separator.TFrame',
                       background='#2980b9',
                       relief='flat')
        
        # Główny kontener
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=30, pady=30)
        
        # Tytuł aplikacji
        title_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        title_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 30))
        
        # Logo container
        logo_frame = ttk.Frame(title_frame, style='Logo.TFrame')
        logo_frame.grid(row=0, column=0, sticky='w')
        
        # Logo z ikoną i tekstem
        logo_text = "AI Data Assistant"
        logo_label = tk.Label(logo_frame,
                            text="🤖 " + logo_text,
                            font=('Segoe UI', 32, 'bold'),
                            bg=self.colors['bg'],
                            fg='white')
        logo_label.grid(row=0, column=0, sticky='w', padx=20)
        
        # Efekt cienia dla logo
        shadow_label = tk.Label(logo_frame,
                              text="🤖 " + logo_text,
                              font=('Segoe UI', 32, 'bold'),
                              bg=self.colors['bg'],
                              fg='#2980b9')  # Kolor cienia
        shadow_label.grid(row=0, column=0, sticky='w', padx=21, pady=1)
        
        # Podtytuł
        subtitle_label = tk.Label(logo_frame,
                                text="Analiza Danych",
                                font=('Segoe UI', 16),
                                bg=self.colors['bg'],
                                fg='#bdc3c7')  # Jaśniejszy kolor dla podtytułu
        subtitle_label.grid(row=1, column=0, sticky='w', padx=20, pady=(0, 10))
        
        # Linia dekoracyjna pod tytułem
        separator = ttk.Frame(title_frame, height=2, style='Separator.TFrame')
        separator.grid(row=2, column=0, sticky='ew', padx=20)
        
        # Konfiguracja rozszerzania
        title_frame.grid_columnconfigure(0, weight=1)
        
        # Kontener dla górnego rzędu (menu i wizualizacji)
        top_container = ttk.Frame(self.main_frame, style='Panel.TFrame')
        top_container.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(0, 20))
        
        # Przycisk rozwijania - większy i bardziej widoczny
        self.toggle_button = ttk.Button(top_container,
                                      text="🔽 Pokaż opcje",
                                      command=self.toggle_actions,
                                      style='Toggle.TButton')
        self.toggle_button.grid(row=0, column=0, sticky='w', padx=15, pady=10)
        
        # Separator pionowy
        separator = ttk.Frame(top_container, width=2, style='Separator.TFrame')
        separator.grid(row=0, column=1, sticky='ns', padx=15, pady=10)
        
        # Nagłówek wizualizacji z ikoną
        viz_label = ttk.Label(top_container,
                            text="📊 Wizualizacja danych",
                            style='Subtitle.TLabel')
        viz_label.grid(row=0, column=2, sticky='w', padx=15, pady=10)
        
        # Combobox z typami wykresów - większy i bardziej czytelny
        self.viz_combo = ttk.Combobox(top_container,
                                    values=list(self.viz_types.keys()),
                                    state='readonly',
                                    width=35,
                                    font=('Segoe UI', 11))
        self.viz_combo.grid(row=0, column=3, sticky='ew', padx=15, pady=10)
        self.viz_combo.set('Mapa korelacji')
        self.viz_combo.bind('<<ComboboxSelected>>', self.on_viz_type_change)
        
        # Przycisk generowania wykresu - większy i bardziej widoczny
        generate_btn = ttk.Button(top_container,
                                text="📈 Generuj wykres",
                                command=self.generate_plot,
                                style='Generate.TButton')
        generate_btn.grid(row=0, column=4, padx=15, pady=10, sticky='e')

        # Ramka dla wyboru kolumn
        self.column_frame = ttk.Frame(top_container, style='Panel.TFrame')
        self.column_frame.grid(row=1, column=0, columnspan=5, sticky='ew', padx=15, pady=(0, 10))
        
        # Inicjalizacja etykiet i combobox-ów dla wyboru kolumn
        self.x_label = ttk.Label(self.column_frame, text="Kolumna X:", style='Subtitle.TLabel')
        self.x_combo = ttk.Combobox(self.column_frame, state='readonly', width=20, font=('Segoe UI', 11))
        
        self.y_label = ttk.Label(self.column_frame, text="Kolumna Y:", style='Subtitle.TLabel')
        self.y_combo = ttk.Combobox(self.column_frame, state='readonly', width=20, font=('Segoe UI', 11))
        
        # Panel wyników (powiększony)
        results_frame = ttk.Frame(self.main_frame, style='Panel.TFrame')
        results_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')
        
        # Panel wyników z przyciskiem trybu ciemnego
        results_header = ttk.Frame(results_frame, style='Panel.TFrame')
        results_header.grid(row=0, column=0, sticky='ew', padx=15, pady=(10, 5))
        
        results_label = ttk.Label(results_header,
                                text="Wyniki analizy",
                                style='Subtitle.TLabel')
        results_label.pack(side='left')
        
        # Przycisk przełączania trybu ciemnego
        self.dark_mode_btn = ttk.Button(results_header,
                                      text="🌙 Tryb ciemny",
                                      command=self.toggle_dark_mode,
                                      style='Action.TButton')
        self.dark_mode_btn.pack(side='right')
        
        # Pole tekstowe na wyniki (powiększone)
        text_frame = ttk.Frame(results_frame, style='Panel.TFrame')
        text_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        
        self.result_text = tk.Text(text_frame,
                                 height=30,
                                 width=100,
                                 font=('Consolas', 11),
                                 bg=self.colors['light_bg'],
                                 fg=self.colors['light_fg'],
                                 wrap=tk.WORD,
                                 padx=15,
                                 pady=15)
        self.result_text.grid(row=0, column=0, sticky='nsew')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame,
                                orient="vertical",
                                command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_bar = ttk.Label(self.main_frame,
                                  text="Gotowy do pracy",
                                  style='Status.TLabel')
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
        # Konfiguracja rozszerzania się elementów
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=3)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Większa waga dla panelu wyników
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_columnconfigure(1, weight=1)
        
        self.data = None
        self.current_plot_file = "wykres.html"
        self.actions_visible = False
        self.dark_mode = False
        
        # Inicjalizacja menu akcji
        self.action_popup = tk.Toplevel(self.root)
        self.action_popup.withdraw()  # Ukryj menu na początku
        self.action_popup.overrideredirect(True)  # Usuń dekoracje okna
        self.action_popup.configure(bg=self.colors['secondary_bg'])
        
        # Kontener dla przycisków menu
        action_container = ttk.Frame(self.action_popup, style='Panel.TFrame')
        action_container.pack(fill='x', padx=2, pady=2)
        
        # Przyciski menu z ikonami i tooltipami
        actions = [
            ("📂 Wczytaj dane", self.load_data, "Wczytaj plik CSV z danymi do analizy"),
            ("📊 Podstawowe statystyki", self.analyze_data, "Wyświetl podstawowe informacje o danych: typy kolumn, statystyki opisowe, brakujące wartości"),
            ("📈 Testy statystyczne", self.statistical_analysis, "Wykonaj testy normalności, analizę korelacji i podstawowe testy statystyczne"),
            ("🔬 Analiza szczegółowa", self.advanced_statistical_analysis, "Wykonaj zaawansowaną analizę rozkładów, wartości odstających i korelacji"),
            ("💾 Eksportuj wyniki", self.export_results, "Zapisz wyniki do pliku"),
            ("🗑️ Wyczyść", self.clear_results, "Wyczyść pole wyników")
        ]
        
        for text, command, tooltip in actions:
            btn_frame = ttk.Frame(action_container, style='Panel.TFrame')
            btn_frame.pack(fill='x', padx=2, pady=1)
            
            btn = ttk.Button(btn_frame,
                           text=text,
                           command=lambda cmd=command: self.execute_action(cmd),
                           style='Action.TButton')
            btn.pack(fill='x', padx=5, pady=3, ipady=5)
            self.create_tooltip(btn, tooltip)

    def execute_action(self, command):
        """Wykonuje akcję i ukrywa menu."""
        self.toggle_actions()  # Ukryj menu
        command()  # Wykonaj wybraną akcję
        
    def toggle_actions(self):
        """Przełącza widoczność panelu akcji."""
        if self.actions_visible:
            self.action_popup.withdraw()
            self.toggle_button.configure(text="🔽 Pokaż opcje")
            self.root.unbind('<Button-1>')
            self.actions_visible = False
        else:
            # Oblicz pozycję dla wyskakującego okna
            button_x = self.toggle_button.winfo_rootx()
            button_y = self.toggle_button.winfo_rooty() + self.toggle_button.winfo_height()
            
            # Aktualizuj geometrię menu
            self.action_popup.geometry(f"+{button_x}+{button_y}")
            
            # Pokaż menu
            self.action_popup.deiconify()
            self.action_popup.lift()
            self.toggle_button.configure(text="🔼 Ukryj opcje")
            
            # Dodaj obsługę kliknięcia poza menu
            self.root.bind('<Button-1>', self.check_click_outside)
            self.actions_visible = True
        
    def check_click_outside(self, event):
        """Sprawdza czy kliknięcie było poza menu i zamyka je jeśli tak."""
        if not self.actions_visible:
            return
            
        # Sprawdź czy kliknięcie było w przycisk toggle - jeśli tak, nie rób nic
        if event.widget == self.toggle_button:
            return
            
        # Pobierz współrzędne kliknięcia względem ekranu
        x, y = event.x_root, event.y_root
        
        # Pobierz geometrię menu
        popup_x = self.action_popup.winfo_x()
        popup_y = self.action_popup.winfo_y()
        popup_width = self.action_popup.winfo_width()
        popup_height = self.action_popup.winfo_height()
        
        # Sprawdź czy kliknięcie było poza menu
        if not (popup_x <= x <= popup_x + popup_width and
               popup_y <= y <= popup_y + popup_height):
            self.toggle_actions()

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update()

    def load_data(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if file_path:
                self.update_status("Wczytywanie danych...")
                self.data = pd.read_csv(file_path)
                self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
                self.result_text.insert(tk.END, "✅ Dane zostały wczytane pomyślnie!\n\n")
                self.result_text.insert(tk.END, f"📊 Wymiary danych: {self.data.shape[0]} wierszy, {self.data.shape[1]} kolumn\n\n")
                self.result_text.insert(tk.END, "📋 Pierwsze 5 wierszy danych:\n\n")
                self.result_text.insert(tk.END, str(self.data.head()) + "\n\n")
                self.result_text.insert(tk.END, "="*50 + "\n")
                self.update_status("Dane wczytane pomyślnie")
        except Exception as e:
            self.update_status("Błąd wczytywania danych")
            messagebox.showerror("Błąd", f"Nie można wczytać danych: {str(e)}")

    def analyze_data(self):
        if self.data is None:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wczytaj dane!")
            return
        
        try:
            self.update_status("Analizowanie danych...")
            # Podstawowe statystyki
            self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            self.result_text.insert(tk.END, "=== Podstawowa analiza danych ===\n\n")
            
            # Informacje o typach danych
            self.result_text.insert(tk.END, "📊 Typy danych w kolumnach:\n\n")
            self.result_text.insert(tk.END, str(self.data.dtypes) + "\n\n")
            
            # Statystyki numeryczne
            numeric_data = self.data.select_dtypes(include=[np.number])
            if not numeric_data.empty:
                self.result_text.insert(tk.END, "📈 Statystyki dla kolumn numerycznych:\n\n")
                self.result_text.insert(tk.END, str(numeric_data.describe()) + "\n\n")
            
            # Analiza brakujących danych
            self.result_text.insert(tk.END, "❗ Brakujące wartości:\n\n")
            missing_data = self.data.isnull().sum()
            self.result_text.insert(tk.END, str(missing_data) + "\n\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            
            self.result_text.see("1.0")  # Przewijanie na początek zamiast na koniec
            self.update_status("Analiza zakończona pomyślnie")
        except Exception as e:
            self.update_status("Błąd podczas analizy")
            messagebox.showerror("Błąd", f"Błąd podczas analizy: {str(e)}")

    def export_results(self):
        try:
            # Pobierz zawartość pola tekstowego
            results_content = self.result_text.get(1.0, tk.END)
            
            if not results_content.strip():
                messagebox.showwarning("Ostrzeżenie", "Brak wyników do eksportu!")
                return
            
            self.update_status("Eksportowanie wyników...")
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Plik tekstowy", "*.txt"),
                    ("Plik CSV", "*.csv"),
                    ("Wszystkie pliki", "*.*")
                ]
            )
            
            if file_path:
                file_extension = os.path.splitext(file_path)[1].lower()
                
                if file_extension == '.txt':
                    # Eksport do TXT
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(results_content)
                
                elif file_extension == '.csv':
                    # Eksport do CSV z obsługą polskich znaków
                    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
                        # Dodajemy BOM dla Excel
                        content = results_content.replace('\t', ',')
                        f.write(content)
                
                self.update_status("Wyniki wyeksportowane pomyślnie")
                messagebox.showinfo("Sukces", f"Wyniki zostały wyeksportowane do pliku {file_path}")
        except Exception as e:
            self.update_status("Błąd podczas eksportu")
            messagebox.showerror("Błąd", f"Nie można wyeksportować wyników: {str(e)}")

    def clear_results(self):
        """Czyści pole wyników, ale zachowuje informacje o wczytanych danych."""
        self.result_text.delete(1.0, tk.END)
        
        # Jeśli dane są wczytane, wyświetl podstawowe informacje
        if self.data is not None:
            self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            self.result_text.insert(tk.END, "✨ Dane są wczytane i gotowe do analizy ✨\n\n")
            self.result_text.insert(tk.END, f"📊 Wymiary danych: {self.data.shape[0]} wierszy, {self.data.shape[1]} kolumn\n\n")
            
            # Informacja o typach kolumn
            numeric_cols = len(self.data.select_dtypes(include=[np.number]).columns)
            categorical_cols = len(self.data.select_dtypes(include=['object']).columns)
            self.result_text.insert(tk.END, f"🔢 Kolumny numeryczne: {numeric_cols}\n")
            self.result_text.insert(tk.END, f"📝 Kolumny kategoryczne: {categorical_cols}\n\n")
            
            self.result_text.insert(tk.END, "Wybierz opcję z menu, aby rozpocząć analizę.\n\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.update_status("Wyniki wyczyszczone, dane pozostają wczytane")
        else:
            self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            self.result_text.insert(tk.END, "⚠️ Brak wczytanych danych. Użyj opcji 'Wczytaj dane' aby rozpocząć analizę.\n\n")
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.update_status("Wyniki wyczyszczone")

    def on_viz_type_change(self, event=None):
        """Obsługuje zmianę typu wizualizacji."""
        selected = self.viz_combo.get()
        
        # Konfiguracja dla różnych typów wykresów
        viz_config = {
            'Wykres rozrzutu': {'x': 'numeric', 'y': 'numeric', 'color': 'both', 'size': 'numeric'},
            'Wykres liniowy': {'x': 'both', 'y': 'numeric'},
            'Wykres obszarowy': {'x': 'both', 'y': 'numeric'},
            'Wykres słupkowy': {'x': 'categorical', 'y': 'numeric'},
            'Wykres kołowy': {'x': 'categorical', 'y': 'numeric'},
            'Histogram': {'x': 'numeric'},
            'Wykres pudełkowy': {'x': 'numeric'},
            'Wykres skrzypcowy': {'x': 'numeric'},
            'Mapa korelacji': {'x': None, 'y': None},
            'Mapa cieplna': {'x': 'categorical', 'y': 'numeric'}
        }
        
        if selected in viz_config:
            config = viz_config[selected]
            
            # Ukryj wszystkie elementy na początku
            self.hide_column_selection()
            
            if self.data is not None:
                # Przygotuj listy kolumn
                numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()
                all_cols = self.data.columns.tolist()
                
                # Dodaj etykiety i combobox-y dla dodatkowych kolumn tylko dla wykresu rozrzutu
                if selected == 'Wykres rozrzutu':
                    self.color_label = ttk.Label(self.column_frame, text="🎨 Kolor:", style='Subtitle.TLabel')
                    self.color_combo = ttk.Combobox(self.column_frame, state='readonly', width=20, font=('Segoe UI', 11))
                    self.color_combo['values'] = ['Brak'] + all_cols
                    self.color_combo.set('Brak')
                    self.color_label.grid(row=1, column=0, padx=5, pady=5)
                    self.color_combo.grid(row=1, column=1, padx=5, pady=5)
                    
                    self.size_label = ttk.Label(self.column_frame, text="⭕ Rozmiar:", style='Subtitle.TLabel')
                    self.size_combo = ttk.Combobox(self.column_frame, state='readonly', width=20, font=('Segoe UI', 11))
                    self.size_combo['values'] = ['Brak'] + numeric_cols
                    self.size_combo.set('Brak')
                    self.size_label.grid(row=1, column=2, padx=5, pady=5)
                    self.size_combo.grid(row=1, column=3, padx=5, pady=5)
                
                # Konfiguracja dla osi X
                if config.get('x') is not None:
                    if config['x'] == 'numeric':
                        self.x_label.configure(text="📊 Kolumna numeryczna (X):")
                        self.x_combo['values'] = numeric_cols
                        if numeric_cols:
                            self.x_combo.set(numeric_cols[0])
                    elif config['x'] == 'categorical':
                        self.x_label.configure(text="📑 Kolumna kategoryczna (X):")
                        self.x_combo['values'] = categorical_cols
                        if categorical_cols:
                            self.x_combo.set(categorical_cols[0])
                    elif config['x'] == 'both':
                        self.x_label.configure(text="📊 Kolumna X:")
                        self.x_combo['values'] = all_cols
                        if all_cols:
                            self.x_combo.set(all_cols[0])
                    self.x_label.grid(row=0, column=0, padx=5, pady=5)
                    self.x_combo.grid(row=0, column=1, padx=5, pady=5)
                
                # Konfiguracja dla osi Y
                if config.get('y') is not None:
                    if config['y'] == 'numeric':
                        self.y_label.configure(text="📈 Kolumna numeryczna (Y):")
                        self.y_combo['values'] = numeric_cols
                        if numeric_cols:
                            self.y_combo.set(numeric_cols[-1] if len(numeric_cols) > 1 else numeric_cols[0])
                    elif config['y'] == 'categorical':
                        self.y_label.configure(text="📑 Kolumna kategoryczna (Y):")
                        self.y_combo['values'] = categorical_cols
                        if categorical_cols:
                            self.y_combo.set(categorical_cols[0])
                    elif config['y'] == 'both':
                        self.y_label.configure(text="📊 Kolumna Y:")
                        self.y_combo['values'] = all_cols
                        if all_cols:
                            self.y_combo.set(all_cols[-1])
                    self.y_label.grid(row=0, column=2, padx=5, pady=5)
                    self.y_combo.grid(row=0, column=3, padx=5, pady=5)

    def hide_column_selection(self):
        """Ukrywa wybór kolumn."""
        self.x_label.grid_remove()
        self.x_combo.grid_remove()
        self.y_label.grid_remove()
        self.y_combo.grid_remove()
        if hasattr(self, 'color_label'):
            self.color_label.grid_remove()
            self.color_combo.grid_remove()
        if hasattr(self, 'size_label'):
            self.size_label.grid_remove()
            self.size_combo.grid_remove()

    def validate_plot_inputs(self, selected_viz):
        """Sprawdza poprawność danych wejściowych dla wybranego typu wykresu."""
        if self.data is None:
            return False, "⚠️ Najpierw wczytaj dane! Użyj przycisku 'Wczytaj dane' aby rozpocząć."
            
        if selected_viz in ['Wykres rozrzutu', 'Wykres liniowy', 'Wykres obszarowy']:
            if not self.x_combo.get() or not self.y_combo.get():
                return False, "⚠️ Wybierz kolumny dla osi X i Y."
            if self.x_combo.get() == self.y_combo.get():
                return False, "⚠️ Wybierz różne kolumny dla osi X i Y."
                
        if selected_viz in ['Histogram', 'Wykres pudełkowy', 'Wykres skrzypcowy']:
            if not self.x_combo.get():
                return False, "⚠️ Wybierz kolumnę do analizy."
                
        if selected_viz in ['Wykres kołowy', 'Wykres słupkowy']:
            if not self.x_combo.get() or not self.y_combo.get():
                return False, "⚠️ Wybierz kolumnę kategoryczną (X) i numeryczną (Y)."
            if self.x_combo.get() == self.y_combo.get():
                return False, "⚠️ Wybierz różne kolumny dla kategorii i wartości."
                
        if selected_viz == 'Mapa korelacji':
            numeric_data = self.data.select_dtypes(include=[np.number])
            if numeric_data.empty:
                return False, "⚠️ Brak kolumn numerycznych w danych. Mapa korelacji wymaga co najmniej dwóch kolumn numerycznych."
            if len(numeric_data.columns) < 2:
                return False, "⚠️ Potrzebne są co najmniej dwie kolumny numeryczne do utworzenia mapy korelacji."
                
        if selected_viz == 'Mapa cieplna':
            if not self.x_combo.get() or not self.y_combo.get():
                return False, "⚠️ Wybierz kolumnę kategoryczną (X) i numeryczną (Y) dla mapy cieplnej."
            
        # Sprawdzenie koloru i rozmiaru tylko dla wykresu rozrzutu
        if selected_viz == 'Wykres rozrzutu':
            if hasattr(self, 'color_combo') and self.color_combo.get() != 'Brak':
                if self.color_combo.get() == self.x_combo.get() or self.color_combo.get() == self.y_combo.get():
                    return False, "⚠️ Kolumna użyta do kolorowania nie może być taka sama jak kolumna na osi X lub Y."
            if hasattr(self, 'size_combo') and self.size_combo.get() != 'Brak':
                if self.size_combo.get() == self.x_combo.get() or self.size_combo.get() == self.y_combo.get():
                    return False, "⚠️ Kolumna użyta do rozmiaru punktów nie może być taka sama jak kolumna na osi X lub Y."
                    
        return True, ""

    def generate_plot(self):
        """Generuje wykres na podstawie wybranych opcji."""
        selected_viz = self.viz_combo.get()
        
        try:
            # Sprawdzenie poprawności danych wejściowych
            is_valid, error_message = self.validate_plot_inputs(selected_viz)
            if not is_valid:
                messagebox.showwarning("Nieprawidłowe dane", error_message)
                return
            
            self.update_status(f"Generowanie wykresu: {selected_viz}...")
            self.viz_types[selected_viz]()
            self.update_status(f"✅ Wykres {selected_viz.lower()} został wygenerowany")
            
        except pd.errors.EmptyDataError:
            messagebox.showerror("Błąd danych", "⚠️ Dane są puste lub nie zawierają odpowiednich wartości.")
        except ValueError as e:
            if "could not convert string to float" in str(e):
                messagebox.showerror("Błąd danych", "⚠️ Wybrane kolumny zawierają nieprawidłowe wartości numeryczne.")
            else:
                messagebox.showerror("Błąd", f"⚠️ Wystąpił błąd podczas generowania wykresu:\n{str(e)}")
        except Exception as e:
            error_message = str(e)
            if "Invalid element" in error_message:
                if "color" in error_message:
                    messagebox.showerror("Błąd", "⚠️ Nieprawidłowa kolumna wybrana do kolorowania punktów.")
                elif "size" in error_message:
                    messagebox.showerror("Błąd", "⚠️ Nieprawidłowa kolumna wybrana do określania rozmiaru punktów.")
                else:
                    messagebox.showerror("Błąd", "⚠️ Nieprawidłowe wartości w wybranych kolumnach.")
            else:
                messagebox.showerror("Błąd", f"⚠️ Wystąpił nieoczekiwany błąd:\n{error_message}")

    def plot_correlation(self):
        numeric_data = self.data.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            corr = numeric_data.corr()
            fig = px.imshow(corr,
                          labels=dict(color="Korelacja"),
                          title="Mapa korelacji",
                          color_continuous_scale="RdBu")
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_scatter(self):
        """Generuje rozszerzony wykres rozrzutu z opcjonalnym kolorem i rozmiarem punktów."""
        if self.x_combo.get() and self.y_combo.get():
            # Podstawowe dane
            x_data = self.data[self.x_combo.get()]
            y_data = self.data[self.y_combo.get()]
            
            # Użyj px.scatter zamiast go.Figure dla lepszej obsługi kolorów kategorycznych
            plot_args = {
                'data_frame': self.data,
                'x': self.x_combo.get(),
                'y': self.y_combo.get(),
                'title': f"Wykres rozrzutu: {self.x_combo.get()} vs {self.y_combo.get()}"
            }
            
            # Dodaj kolor jeśli wybrano
            if hasattr(self, 'color_combo') and self.color_combo.get() != 'Brak':
                plot_args['color'] = self.color_combo.get()
                plot_args['title'] += f" (kolor: {self.color_combo.get()})"
            
            # Dodaj rozmiar jeśli wybrano
            if hasattr(self, 'size_combo') and self.size_combo.get() != 'Brak':
                plot_args['size'] = self.size_combo.get()
                plot_args['title'] += f" (rozmiar: {self.size_combo.get()})"
            
            fig = px.scatter(**plot_args)
            
            # Dodaj linię trendu
            if self.color_combo.get() == 'Brak':  # Dodaj linię trendu tylko gdy nie ma grupowania po kolorze
                z = np.polyfit(x_data, y_data, 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=p(x_data),
                    mode='lines',
                    name='Linia trendu',
                    line=dict(color='red')
                ))
            
            # Formatowanie wykresu
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_x=0.5,
                title_font_size=20,
                showlegend=True
            )
            
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_histogram(self):
        """Generuje histogram dla wybranej kolumny numerycznej."""
        if self.x_combo.get():
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=self.data[self.x_combo.get()],
                name=self.x_combo.get(),
                opacity=0.7,
                nbinsx=30
            ))
            fig.update_layout(
                title=f"Histogram dla {self.x_combo.get()}",
                xaxis_title=self.x_combo.get(),
                yaxis_title="Liczba wystąpień",
                bargap=0.1
            )
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_boxplot(self):
        """Generuje wykres pudełkowy dla wybranej kolumny numerycznej."""
        if self.x_combo.get():
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=self.data[self.x_combo.get()],
                name=self.x_combo.get(),
                boxpoints='outliers'
            ))
            fig.update_layout(
                title=f"Wykres pudełkowy dla {self.x_combo.get()}",
                showlegend=False,
                yaxis_title=self.x_combo.get()
            )
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_line(self):
        if self.x_combo.get() and self.y_combo.get():
            fig = px.line(self.data,
                         x=self.x_combo.get(),
                         y=self.y_combo.get(),
                         title=f"Wykres liniowy: {self.x_combo.get()} vs {self.y_combo.get()}")
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_pie(self):
        """Generuje wykres kołowy dla wybranych kolumn."""
        if self.x_combo.get() and self.y_combo.get():
            # Agregacja danych
            df_grouped = self.data.groupby(self.x_combo.get())[self.y_combo.get()].sum().reset_index()
            
            fig = go.Figure(data=[go.Pie(
                labels=df_grouped[self.x_combo.get()],
                values=df_grouped[self.y_combo.get()],
                hole=0.3
            )])
            
            fig.update_layout(
                title=f"Wykres kołowy: {self.y_combo.get()} według {self.x_combo.get()}",
                showlegend=True
            )
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_bar(self):
        """Generuje wykres słupkowy dla wybranych kolumn."""
        if self.x_combo.get() and self.y_combo.get():
            # Agregacja danych
            df_grouped = self.data.groupby(self.x_combo.get())[self.y_combo.get()].sum().reset_index()
            
            fig = go.Figure(data=[go.Bar(
                x=df_grouped[self.x_combo.get()],
                y=df_grouped[self.y_combo.get()],
                name=self.y_combo.get()
            )])
            
            fig.update_layout(
                title=f"Wykres słupkowy: {self.y_combo.get()} według {self.x_combo.get()}",
                xaxis_title=self.x_combo.get(),
                yaxis_title=self.y_combo.get(),
                bargap=0.2
            )
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_violin(self):
        """Generuje wykres skrzypcowy dla wybranej kolumny numerycznej."""
        if self.x_combo.get():
            fig = go.Figure()
            fig.add_trace(go.Violin(
                y=self.data[self.x_combo.get()],
                name=self.x_combo.get(),
                box_visible=True,
                meanline_visible=True,
                points='outliers'
            ))
            fig.update_layout(
                title=f"Wykres skrzypcowy dla {self.x_combo.get()}",
                showlegend=True,
                yaxis_title=self.x_combo.get()
            )
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_heatmap(self):
        """Generuje mapę cieplną dla wybranych kolumn numerycznych."""
        if self.x_combo.get() and self.y_combo.get():
            # Tworzenie tabeli przestawnej dla mapy cieplnej
            pivot_table = pd.pivot_table(
                self.data, 
                values=self.y_combo.get(),
                index=self.x_combo.get(),
                aggfunc='mean'
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_table.values,
                x=pivot_table.columns,
                y=pivot_table.index,
                colorscale='Viridis'
            ))
            
            fig.update_layout(
                title=f"Mapa cieplna: {self.y_combo.get()} według {self.x_combo.get()}",
                xaxis_title=self.x_combo.get(),
                yaxis_title=self.y_combo.get()
            )
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def plot_area(self):
        if self.x_combo.get() and self.y_combo.get():
            x_data = self.data[self.x_combo.get()]
            y_data = self.data[self.y_combo.get()]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                fill='tozeroy',
                name='Obszar'
            ))
            
            fig.update_layout(
                title=f"Wykres obszarowy: {self.x_combo.get()} vs {self.y_combo.get()}",
                xaxis_title=self.x_combo.get(),
                yaxis_title=self.y_combo.get(),
                showlegend=True
            )
            
            fig.write_html(self.current_plot_file)
            webbrowser.open(self.current_plot_file)

    def statistical_analysis(self):
        if self.data is None:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wczytaj dane!")
            return
        
        try:
            self.update_status("Przeprowadzanie analizy statystycznej...")
            self.result_text.insert(tk.END, "=== Zaawansowana analiza statystyczna ===\n\n")
            
            # 1. Test normalności dla zmiennych numerycznych
            numeric_data = self.data.select_dtypes(include=[np.number])
            self.result_text.insert(tk.END, "1. Test normalności (Shapiro-Wilk):\n")
            self.result_text.insert(tk.END, "Sprawdzanie rozkładu normalnego dla każdej zmiennej numerycznej:\n\n")
            
            for column in numeric_data.columns:
                if len(numeric_data[column]) > 3:  # Shapiro-Wilk wymaga co najmniej 3 obserwacji
                    statistic, p_value = stats.shapiro(numeric_data[column].dropna())
                    result = "normalny" if p_value > 0.05 else "nie-normalny"
                    self.result_text.insert(tk.END, f"{column}: p-wartość = {p_value:.4f} (rozkład {result})\n")
            self.result_text.insert(tk.END, "\n")
            
            # 2. Wykrywanie wartości odstających (outliers)
            self.result_text.insert(tk.END, "2. Wykrywanie wartości odstających (metoda IQR):\n")
            for column in numeric_data.columns:
                Q1 = numeric_data[column].quantile(0.25)
                Q3 = numeric_data[column].quantile(0.75)
                IQR = Q3 - Q1
                outliers = numeric_data[(numeric_data[column] < (Q1 - 1.5 * IQR)) | 
                                     (numeric_data[column] > (Q3 + 1.5 * IQR))][column]
                outliers_count = len(outliers)
                if outliers_count > 0:
                    self.result_text.insert(tk.END, f"{column}: znaleziono {outliers_count} wartości odstających\n")
                    self.result_text.insert(tk.END, f"Zakres prawidłowych wartości: ({Q1 - 1.5 * IQR:.2f}, {Q3 + 1.5 * IQR:.2f})\n")
                    self.result_text.insert(tk.END, f"Wartości odstające: {outliers.values[:5]}")
                    if len(outliers) > 5:
                        self.result_text.insert(tk.END, " ...")
                    self.result_text.insert(tk.END, "\n\n")
            
            # 3. Analiza korelacji i sugestie
            if len(numeric_data.columns) > 1:
                self.result_text.insert(tk.END, "3. Analiza korelacji i sugestie:\n")
                corr_matrix = numeric_data.corr()
                
                # Znajdowanie silnych korelacji
                strong_correlations = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i + 1, len(corr_matrix.columns)):
                        corr_value = corr_matrix.iloc[i, j]
                        if abs(corr_value) > 0.7:  # Próg dla silnej korelacji
                            strong_correlations.append({
                                'var1': corr_matrix.columns[i],
                                'var2': corr_matrix.columns[j],
                                'corr': corr_value
                            })
                
                if strong_correlations:
                    self.result_text.insert(tk.END, "\nWykryto silne korelacje:\n")
                    for corr in strong_correlations:
                        direction = "dodatnią" if corr['corr'] > 0 else "ujemną"
                        strength = "bardzo silną" if abs(corr['corr']) > 0.9 else "silną"
                        self.result_text.insert(tk.END, 
                            f"- {corr['var1']} i {corr['var2']}: {strength} korelację {direction} ({corr['corr']:.3f})\n")
                        
                        # Dodanie sugestii
                        if corr['corr'] > 0.95:
                            self.result_text.insert(tk.END, 
                                "  Sugestia: Zmienne są prawie idealnie skorelowane, można rozważyć usunięcie jednej z nich.\n")
                else:
                    self.result_text.insert(tk.END, "Nie wykryto silnych korelacji między zmiennymi.\n")
            
            # 4. Testy statystyczne
            self.result_text.insert(tk.END, "\n4. Testy statystyczne:\n")
            
            # T-test dla każdej zmiennej numerycznej (test czy średnia różni się od 0)
            self.result_text.insert(tk.END, "\na) Jednoprzykładowy test t-Studenta:\n")
            for column in numeric_data.columns:
                t_stat, p_value = stats.ttest_1samp(numeric_data[column].dropna(), 0)
                significant = "istotnie" if p_value < 0.05 else "nie"
                self.result_text.insert(tk.END, 
                    f"{column}: średnia {significant} różni się od 0 (p-wartość = {p_value:.4f})\n")
            
            # ANOVA dla zmiennych kategorycznych (jeśli istnieją)
            categorical_cols = self.data.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0 and len(numeric_data.columns) > 0:
                self.result_text.insert(tk.END, "\nb) Analiza wariancji (ANOVA):\n")
                for cat_col in categorical_cols:
                    for num_col in numeric_data.columns:
                        groups = [group for name, group in self.data.groupby(cat_col)[num_col] if len(group) > 0]
                        if len(groups) > 1:  # ANOVA wymaga co najmniej 2 grup
                            try:
                                f_stat, p_value = stats.f_oneway(*groups)
                                significant = "istotne" if p_value < 0.05 else "brak istotnych"
                                self.result_text.insert(tk.END, 
                                    f"{cat_col} vs {num_col}: {significant} różnic między grupami (p-wartość = {p_value:.4f})\n")
                            except:
                                continue
            
            self.result_text.see(tk.END)
            self.update_status("Analiza statystyczna zakończona pomyślnie")
            
        except Exception as e:
            self.update_status("Błąd podczas analizy statystycznej")
            messagebox.showerror("Błąd", f"Błąd podczas analizy statystycznej: {str(e)}")

    def advanced_statistical_analysis(self):
        """Wykonuje zaawansowaną analizę statystyczną danych."""
        if self.data is None:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wczytaj dane!")
            return
        
        try:
            self.update_status("Przeprowadzanie zaawansowanej analizy statystycznej...")
            self.result_text.insert(tk.END, "=== Zaawansowana analiza statystyczna ===\n\n")
            
            numeric_data = self.data.select_dtypes(include=[np.number])
            if numeric_data.empty:
                messagebox.showwarning("Ostrzeżenie", "Brak danych numerycznych do analizy!")
                return
            
            # 1. Szczegółowa analiza rozkładów
            self.result_text.insert(tk.END, "1. Analiza rozkładów:\n\n")
            for column in numeric_data.columns:
                data = numeric_data[column].dropna()
                if len(data) > 0:
                    # Podstawowe statystyki
                    mean = data.mean()
                    median = data.median()
                    std = data.std()
                    skew = data.skew()
                    kurtosis = data.kurtosis()
                    
                    self.result_text.insert(tk.END, f"Kolumna: {column}\n")
                    self.result_text.insert(tk.END, f"- Średnia: {mean:.4f}\n")
                    self.result_text.insert(tk.END, f"- Mediana: {median:.4f}\n")
                    self.result_text.insert(tk.END, f"- Odchylenie standardowe: {std:.4f}\n")
                    self.result_text.insert(tk.END, f"- Skośność: {skew:.4f}")
                    if abs(skew) > 1:
                        self.result_text.insert(tk.END, " (znacząca asymetria)")
                    self.result_text.insert(tk.END, "\n")
                    self.result_text.insert(tk.END, f"- Kurtoza: {kurtosis:.4f}")
                    if abs(kurtosis) > 2:
                        self.result_text.insert(tk.END, " (rozkład znacząco odbiega od normalnego)")
                    self.result_text.insert(tk.END, "\n\n")
                    
                    # Test Shapiro-Wilka
                    if len(data) >= 3 and len(data) <= 5000:
                        statistic, p_value = stats.shapiro(data)
                        self.result_text.insert(tk.END, f"Test Shapiro-Wilka:\n")
                        self.result_text.insert(tk.END, f"- p-wartość: {p_value:.4f}\n")
                        if p_value < 0.05:
                            self.result_text.insert(tk.END, "- Wniosek: Rozkład istotnie różni się od normalnego\n")
                        else:
                            self.result_text.insert(tk.END, "- Wniosek: Brak podstaw do odrzucenia hipotezy o normalności rozkładu\n")
                    
                    # Test D'Agostino-Pearson
                    statistic, p_value = stats.normaltest(data)
                    self.result_text.insert(tk.END, f"\nTest D'Agostino-Pearson:\n")
                    self.result_text.insert(tk.END, f"- p-wartość: {p_value:.4f}\n")
                    if p_value < 0.05:
                        self.result_text.insert(tk.END, "- Wniosek: Rozkład istotnie różni się od normalnego\n")
                    else:
                        self.result_text.insert(tk.END, "- Wniosek: Brak podstaw do odrzucenia hipotezy o normalności rozkładu\n")
                    
                    self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            
            # 2. Zaawansowane wykrywanie outlierów
            self.result_text.insert(tk.END, "2. Zaawansowana analiza wartości odstających:\n\n")
            for column in numeric_data.columns:
                data = numeric_data[column].dropna()
                if len(data) > 0:
                    # Metoda IQR
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers_iqr = data[(data < lower_bound) | (data > upper_bound)]
                    
                    # Metoda Z-score
                    z_scores = np.abs(stats.zscore(data))
                    outliers_zscore = data[z_scores > 3]
                    
                    # Metoda Modified Z-score
                    median = data.median()
                    mad = stats.median_abs_deviation(data)
                    modified_z_scores = 0.6745 * (data - median) / mad
                    outliers_modified_z = data[np.abs(modified_z_scores) > 3.5]
                    
                    self.result_text.insert(tk.END, f"Kolumna: {column}\n")
                    self.result_text.insert(tk.END, f"Metoda IQR:\n")
                    self.result_text.insert(tk.END, f"- Znaleziono {len(outliers_iqr)} wartości odstających\n")
                    self.result_text.insert(tk.END, f"- Zakres prawidłowych wartości: ({lower_bound:.2f}, {upper_bound:.2f})\n")
                    if len(outliers_iqr) > 0:
                        self.result_text.insert(tk.END, f"- Przykładowe wartości odstające: {list(outliers_iqr[:5])}\n")
                    
                    self.result_text.insert(tk.END, f"\nMetoda Z-score (|z| > 3):\n")
                    self.result_text.insert(tk.END, f"- Znaleziono {len(outliers_zscore)} wartości odstających\n")
                    if len(outliers_zscore) > 0:
                        self.result_text.insert(tk.END, f"- Przykładowe wartości odstające: {list(outliers_zscore[:5])}\n")
                    
                    self.result_text.insert(tk.END, f"\nMetoda Modified Z-score (|z_mod| > 3.5):\n")
                    self.result_text.insert(tk.END, f"- Znaleziono {len(outliers_modified_z)} wartości odstających\n")
                    if len(outliers_modified_z) > 0:
                        self.result_text.insert(tk.END, f"- Przykładowe wartości odstające: {list(outliers_modified_z[:5])}\n")
                    
                    # Podsumowanie i rekomendacje
                    all_methods = set(outliers_iqr.index) & set(outliers_zscore.index) & set(outliers_modified_z.index)
                    if len(all_methods) > 0:
                        self.result_text.insert(tk.END, f"\nWartości uznane za odstające przez wszystkie metody: {len(all_methods)}\n")
                        self.result_text.insert(tk.END, "Rekomendacja: Te wartości powinny zostać szczególnie dokładnie przeanalizowane.\n")
                    
                    self.result_text.insert(tk.END, "\n" + "="*50 + "\n\n")
            
            # 3. Rozszerzona analiza korelacji
            if len(numeric_data.columns) > 1:
                self.result_text.insert(tk.END, "3. Rozszerzona analiza korelacji:\n\n")
                
                # Korelacja Pearsona
                pearson_corr = numeric_data.corr(method='pearson')
                
                # Korelacja Spearmana
                spearman_corr = numeric_data.corr(method='spearman')
                
                # Korelacja Kendalla
                kendall_corr = numeric_data.corr(method='kendall')
                
                for i in range(len(numeric_data.columns)):
                    for j in range(i + 1, len(numeric_data.columns)):
                        col1 = numeric_data.columns[i]
                        col2 = numeric_data.columns[j]
                        
                        pearson = pearson_corr.iloc[i, j]
                        spearman = spearman_corr.iloc[i, j]
                        kendall = kendall_corr.iloc[i, j]
                        
                        self.result_text.insert(tk.END, f"Korelacja między {col1} a {col2}:\n")
                        self.result_text.insert(tk.END, f"- Pearson: {pearson:.4f}\n")
                        self.result_text.insert(tk.END, f"- Spearman: {spearman:.4f}\n")
                        self.result_text.insert(tk.END, f"- Kendall: {kendall:.4f}\n")
                        
                        # Interpretacja
                        if abs(pearson) > 0.7 and abs(spearman) > 0.7:
                            self.result_text.insert(tk.END, "Interpretacja: Silna korelacja liniowa i monotoniczna\n")
                        elif abs(pearson) > 0.7 and abs(spearman) <= 0.7:
                            self.result_text.insert(tk.END, "Interpretacja: Silna korelacja liniowa, ale słabsza monotoniczna\n")
                        elif abs(pearson) <= 0.7 and abs(spearman) > 0.7:
                            self.result_text.insert(tk.END, "Interpretacja: Silna korelacja monotoniczna, ale słabsza liniowa\n")
                        
                        # Test istotności
                        _, p_value = stats.pearsonr(numeric_data[col1].dropna(), numeric_data[col2].dropna())
                        if p_value < 0.05:
                            self.result_text.insert(tk.END, "Korelacja jest istotna statystycznie (p < 0.05)\n")
                        else:
                            self.result_text.insert(tk.END, "Korelacja nie jest istotna statystycznie (p >= 0.05)\n")
                        
                        self.result_text.insert(tk.END, "\n")
            
            self.result_text.see("1.0")
            self.update_status("Zaawansowana analiza statystyczna zakończona pomyślnie")
            
        except Exception as e:
            self.update_status("Błąd podczas zaawansowanej analizy statystycznej")
            messagebox.showerror("Błąd", f"Błąd podczas analizy: {str(e)}")

    def show_expanded_results(self):
        """Pokazuje wyniki w osobnym, powiększonym oknie."""
        if self.result_text.get(1.0, tk.END).strip():
            ResultWindow(self.root, self.result_text.get(1.0, tk.END))
        else:
            messagebox.showinfo("Informacja", "Brak wyników do wyświetlenia.")

    def create_tooltip(self, widget, text):
        """Tworzy tooltip dla widgetu."""
        def enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, justify='left',
                           background="#ffffe0", relief='solid', borderwidth=1,
                           font=("Segoe UI", 9))
            label.pack()
            
            widget.tooltip = tooltip
            
        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def toggle_dark_mode(self):
        """Przełącza między trybem ciemnym a jasnym dla pola tekstowego."""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.result_text.configure(
                bg=self.colors['dark_bg'],
                fg=self.colors['dark_fg'],
                insertbackground=self.colors['dark_fg']  # Kolor kursora
            )
            self.dark_mode_btn.configure(text="☀️ Tryb jasny")
        else:
            self.result_text.configure(
                bg=self.colors['light_bg'],
                fg=self.colors['light_fg'],
                insertbackground=self.colors['light_fg']  # Kolor kursora
            )
            self.dark_mode_btn.configure(text="🌙 Tryb ciemny")

def main():
    root = tk.Tk()
    app = AIDataAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
