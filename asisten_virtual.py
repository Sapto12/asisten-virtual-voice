import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import winreg
import glob
from pathlib import Path

class EnhancedAssistant:
    def __init__(self):
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Assistant state
        self.listening = False
        self.running = True
        
        # Scan for all applications
        self.applications = {}
        self.scan_installed_applications()
        
        self.setup_gui()
        
    def setup_voice(self):
        """Setup voice properties"""
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 20)
        
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("🤖 AI Virtual Assistant")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        # Title
        title_label = tk.Label(self.root, text="🤖 Virtual Assistant", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=10)
        
        # Status indicator
        self.status_frame = tk.Frame(self.root, bg='#2c3e50')
        self.status_frame.pack(pady=5)
        
        self.status_light = tk.Label(self.status_frame, text="●", 
                                   font=('Arial', 20), fg='red', bg='#2c3e50')
        self.status_light.pack(side=tk.LEFT)
        
        self.status_text = tk.Label(self.status_frame, text="Standby", 
                                  font=('Arial', 12), fg='white', bg='#2c3e50')
        self.status_text.pack(side=tk.LEFT, padx=5)
        
        # Chat area
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=('Arial', 10),
            bg='#34495e',
            fg='white',
            insertbackground='white'
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        self.button_frame = tk.Frame(self.root, bg='#2c3e50')
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            self.button_frame,
            text="🎤 Start Listening",
            command=self.toggle_listening,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=5,
            relief=tk.FLAT
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(
            self.button_frame,
            text="❌ Quit",
            command=self.quit_app,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=5,
            relief=tk.FLAT
        )
        self.quit_button.pack(side=tk.LEFT, padx=5)
        
        # Initial message
        self.add_message("Assistant", "Halo! Saya siap membantu Anda. Sedang memindai aplikasi yang terinstall...")
        
        # Start app scanning in background
        threading.Thread(target=self.complete_app_scan, daemon=True).start()
        
    def add_message(self, sender, message):
        """Add message to chat area"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if sender == "You":
            formatted_msg = f"[{timestamp}] 🗣️ {sender}: {message}\n"
            color_tag = "user"
        else:
            formatted_msg = f"[{timestamp}] 🤖 {sender}: {message}\n"
            color_tag = "assistant"
        
        self.chat_area.insert(tk.END, formatted_msg)
        
        # Configure colors
        self.chat_area.tag_configure("user", foreground="#3498db")
        self.chat_area.tag_configure("assistant", foreground="#2ecc71")
        
        self.chat_area.see(tk.END)
        self.root.update()
        
    def scan_installed_applications(self):
        """Scan for basic system applications first"""
        # System apps that are always available
        basic_apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'file explorer': 'explorer.exe',
            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe',
            'command prompt': 'cmd.exe',
            'media player': 'wmplayer.exe'
        }
        
        for app_name, exe_name in basic_apps.items():
            self.applications[app_name] = exe_name
            
    def complete_app_scan(self):
        """Complete application scanning in background"""
        try:
            # Scan Windows Registry for installed programs
            self.scan_registry_applications()
            
            # Scan common installation directories
            self.scan_program_directories()
            
            # Scan Start Menu shortcuts
            self.scan_start_menu()
            
            # Update GUI when scanning complete
            total_apps = len(self.applications)
            self.add_message("Assistant", f"Pemindaian selesai! Saya menemukan {total_apps} aplikasi. Sekarang klik 'Start Listening' untuk mulai.")
            
        except Exception as e:
            self.add_message("Assistant", f"Ada kendala saat memindai aplikasi: {str(e)}. Menggunakan aplikasi dasar saja.")
            
    def scan_registry_applications(self):
        """Scan Windows Registry for installed applications"""
        try:
            # Registry paths for installed programs
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for registry_path in registry_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                        try:
                                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                            if install_location and os.path.exists(install_location):
                                                # Look for .exe files in install location
                                                exe_files = glob.glob(os.path.join(install_location, "*.exe"))
                                                if exe_files:
                                                    app_name = display_name.lower().replace(" ", "")
                                                    self.applications[app_name] = exe_files[0]
                                        except FileNotFoundError:
                                            pass
                                    except FileNotFoundError:
                                        pass
                            except (OSError, FileNotFoundError):
                                continue
                except (OSError, FileNotFoundError):
                    continue
                    
        except Exception as e:
            print(f"Registry scan error: {e}")
            
    def scan_program_directories(self):
        """Scan common program directories"""
        try:
            # Common program directories
            program_dirs = [
                r"C:\Program Files",
                r"C:\Program Files (x86)",
                os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'Programs'),
                os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Roaming')
            ]
            
            for program_dir in program_dirs:
                if os.path.exists(program_dir):
                    # Limit depth to avoid long scanning
                    for root, dirs, files in os.walk(program_dir):
                        # Limit depth to 3 levels
                        level = root.replace(program_dir, '').count(os.sep)
                        if level < 3:
                            for file in files:
                                if file.endswith('.exe') and not file.startswith('unins'):
                                    app_name = os.path.splitext(file)[0].lower()
                                    full_path = os.path.join(root, file)
                                    
                                    # Skip system files and uninstallers
                                    if ('uninstall' not in app_name and 
                                        'setup' not in app_name and 
                                        'installer' not in app_name and
                                        app_name not in self.applications):
                                        self.applications[app_name] = full_path
                        else:
                            dirs.clear()  # Don't go deeper
                            
        except Exception as e:
            print(f"Directory scan error: {e}")
            
    def scan_start_menu(self):
        """Scan Start Menu shortcuts"""
        try:
            # Start Menu paths
            start_menu_paths = [
                os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
                os.path.join('C:', 'ProgramData', 'Microsoft', 'Windows', 'Start Menu', 'Programs')
            ]
            
            for start_path in start_menu_paths:
                if os.path.exists(start_path):
                    for root, dirs, files in os.walk(start_path):
                        for file in files:
                            if file.endswith('.lnk'):
                                try:
                                    import win32com.client
                                    shell = win32com.client.Dispatch("WScript.Shell")
                                    shortcut = shell.CreateShortCut(os.path.join(root, file))
                                    target_path = shortcut.Targetpath
                                    
                                    if target_path and target_path.endswith('.exe') and os.path.exists(target_path):
                                        app_name = os.path.splitext(file)[0].lower().replace(" ", "")
                                        if app_name not in self.applications:
                                            self.applications[app_name] = target_path
                                            
                                except:
                                    # If win32com not available, just use filename
                                    app_name = os.path.splitext(file)[0].lower().replace(" ", "")
                                    if app_name not in self.applications:
                                        self.applications[app_name] = f"start {file}"
                                        
        except Exception as e:
            print(f"Start menu scan error: {e}")
            
    def find_application_smart(self, app_name):
        """Smart application finder with fuzzy matching"""
        app_name = app_name.lower().replace(" ", "")
        
        # Direct match
        if app_name in self.applications:
            return self.applications[app_name]
            
        # Partial match
        for key, path in self.applications.items():
            if app_name in key or key in app_name:
                return path
                
        # Fuzzy match for common variations
        variations = {
            'word': ['winword', 'microsoftword', 'msword'],
            'excel': ['msexcel', 'microsoftexcel'],
            'powerpoint': ['mspowerpoint', 'microsoftpowerpoint', 'powerpnt'],
            'chrome': ['googlechrome', 'chromebrowser'],
            'firefox': ['mozillafirefox', 'firefoxbrowser'],
            'vscode': ['visualstudiocode', 'code', 'vs'],
            'photoshop': ['adobephotoshop', 'ps'],
            'discord': ['discordapp'],
            'spotify': ['spotifymusic'],
            'steam': ['steamclient']
        }
        
        for standard_name, variants in variations.items():
            if app_name == standard_name or app_name in variants:
                for key, path in self.applications.items():
                    if standard_name in key or any(variant in key for variant in variants):
                        return path
                        
        return None
        
    def speak(self, text):
        """Convert text to speech"""
        self.add_message("Assistant", text)
        self.engine.say(text)
        self.engine.runAndWait()
        
    def update_status(self, status, color):
        """Update status indicator"""
        self.status_light.configure(fg=color)
        self.status_text.configure(text=status)
        self.root.update()
        
    def open_application(self, app_name):
        """Open any installed application"""
        try:
            app_path = self.find_application_smart(app_name)
            if app_path:
                if app_path.startswith('start '):
                    # For shortcuts
                    os.system(app_path)
                elif app_path.startswith('ms-'):
                    # For Windows Store apps
                    os.system(f'start {app_path}')
                elif os.path.exists(app_path):
                    # For regular applications
                    subprocess.Popen([app_path])
                else:
                    # Try running as command
                    subprocess.Popen([app_path], shell=True)
                return True
            else:
                # Last resort: try Windows start command
                try:
                    os.system(f'start {app_name}')
                    return True
                except:
                    return False
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
            return False
            
    def listen(self):
        """Listen for voice input"""
        try:
            with sr.Microphone() as source:
                self.update_status("Listening...", "green")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
            self.update_status("Processing...", "yellow")
            command = self.recognizer.recognize_google(audio, language='id-ID')
            self.add_message("You", command)
            return command.lower()
            
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "tidak_jelas"
        except sr.RequestError:
            return "error_koneksi"
            
    def process_command(self, command):
        """Process voice commands with enhanced responses"""
        
        if "timeout" in command:
            self.update_status("Timeout", "red")
            return
            
        elif "tidak_jelas" in command:
            self.speak("Maaf, saya tidak dapat memahami. Bisakah Anda mengulanginya dengan lebih jelas?")
            return
            
        elif "error_koneksi" in command:
            self.speak("Maaf, ada masalah dengan koneksi internet. Silakan coba lagi.")
            return
            
        # Enhanced greetings with more natural responses
        elif any(word in command for word in ["halo", "hai", "hello", "selamat"]):
            responses = [
                "Halo! Senang bertemu dengan Anda. Ada yang bisa saya bantu?",
                "Hai! Saya siap membantu Anda hari ini. Apa yang Anda butuhkan?",
                "Hello! Asisten virtual Anda siap bekerja. Silakan berikan perintah."
            ]
            import random
            self.speak(random.choice(responses))
            
        # Time queries with natural responses
        elif any(word in command for word in ["jam", "waktu", "time", "pukul"]):
            current_time = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"Sekarang pukul {current_time}. Apakah ada yang perlu saya ingatkan untuk waktu ini?")
            
        # Date queries
        elif any(word in command for word in ["tanggal", "hari", "date"]):
            today = datetime.datetime.now()
            hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
            bulan = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                    "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            
            day_name = hari[today.weekday()]
            date_str = f"{day_name}, {today.day} {bulan[today.month]} {today.year}"
            self.speak(f"Hari ini adalah {date_str}. Semoga hari Anda menyenangkan!")
            
        # Enhanced website opening
        elif "buka youtube" in command:
            self.speak("Baik, saya akan membuka YouTube untuk Anda. Selamat menonton!")
            webbrowser.open("https://youtube.com")
            
        elif "buka google" in command:
            self.speak("Membuka Google. Anda bisa mulai mencari informasi yang dibutuhkan.")
            webbrowser.open("https://google.com")
            
        elif "buka facebook" in command:
            self.speak("Membuka Facebook. Jangan lupa untuk berinteraksi positif dengan teman-teman Anda!")
            webbrowser.open("https://facebook.com")
            
        # Show available applications
        elif any(word in command for word in ["daftar aplikasi", "list aplikasi", "aplikasi apa", "show apps"]):
            app_count = len(self.applications)
            sample_apps = list(self.applications.keys())[:10]  # Show first 10
            self.speak(f"Saya menemukan {app_count} aplikasi yang terinstall. Beberapa contohnya: {', '.join(sample_apps)}. Katakan 'buka' diikuti nama aplikasi untuk membukanya.")
            
        # Enhanced application opening with better feedback
        elif "buka" in command or "open" in command:
            # Extract app name
            app_name = command.replace("buka", "").replace("open", "").strip()
            
            if app_name:
                self.speak(f"Mencari aplikasi {app_name}...")
                if self.open_application(app_name):
                    self.speak(f"Berhasil membuka {app_name}. Aplikasi sedang dimuat, mohon tunggu sebentar.")
                else:
                    # Suggest similar apps
                    suggestions = []
                    app_name_clean = app_name.lower().replace(" ", "")
                    for app_key in self.applications.keys():
                        if app_name_clean in app_key or app_key in app_name_clean:
                            suggestions.append(app_key)
                    
                    if suggestions:
                        self.speak(f"Tidak menemukan {app_name}, tetapi saya menemukan aplikasi serupa: {', '.join(suggestions[:3])}. Coba sebutkan salah satunya.")
                    else:
                        self.speak(f"Maaf, saya tidak dapat menemukan aplikasi {app_name}. Katakan 'daftar aplikasi' untuk melihat aplikasi yang tersedia.")
            else:
                self.speak("Silakan sebutkan nama aplikasi yang ingin dibuka. Contoh: 'buka chrome' atau 'buka notepad'.")
                
        # Enhanced search
        elif "cari" in command or "search" in command:
            search_query = command.replace("cari", "").replace("search", "").strip()
            if search_query:
                self.speak(f"Baik, saya akan mencari informasi tentang {search_query} di Google untuk Anda.")
                webbrowser.open(f"https://google.com/search?q={search_query}")
            else:
                self.speak("Silakan beritahu saya apa yang ingin Anda cari. Saya akan membantunya.")
                
        # System commands
        elif "tutup" in command or "close" in command:
            self.speak("Fitur menutup aplikasi akan segera tersedia. Untuk saat ini, silakan tutup manual.")
            
        elif "restart" in command:
            self.speak("Untuk keamanan, silakan restart komputer secara manual melalui Start menu.")
            
        # Exit with friendly goodbye
        elif any(word in command for word in ["keluar", "exit", "bye", "selesai", "sampai jumpa"]):
            self.speak("Terima kasih telah menggunakan layanan saya! Sampai jumpa lagi. Semoga hari Anda menyenangkan!")
            return "exit"
            
        # Default response with suggestions
        else:
            suggestions = [
                "Maaf, saya belum memahami perintah tersebut. Coba katakan:",
                "• 'Halo' untuk menyapa saya",
                "• 'Jam berapa' untuk cek waktu",
                "• 'Buka Google' untuk membuka website",
                "• 'Buka Notepad' untuk membuka aplikasi",
                "• 'Cari Python tutorial' untuk mencari di Google"
            ]
            self.speak(" ".join(suggestions))
            
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.listening:
            self.listening = True
            self.start_button.configure(text="🔇 Stop Listening", bg='#e74c3c')
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.listening = False
            self.start_button.configure(text="🎤 Start Listening", bg='#27ae60')
            self.update_status("Standby", "red")
            
    def listen_loop(self):
        """Main listening loop"""
        while self.listening and self.running:
            command = self.listen()
            if command and self.listening:
                result = self.process_command(command)
                if result == "exit":
                    self.quit_app()
                    break
            time.sleep(0.5)
            
    def quit_app(self):
        """Quit application"""
        self.running = False
        self.listening = False
        if hasattr(self, 'root'):
            self.root.quit()
            self.root.destroy()
            
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit_app()

if __name__ == "__main__":
    assistant = EnhancedAssistant()
    assistant.run()