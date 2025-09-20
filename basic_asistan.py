import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

class VirtualAssistant:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Assistant name
        self.name = "Asisten"
        
    def setup_voice(self):
        """Setup voice properties"""
        voices = self.engine.getProperty('voices')
        # Try to use female voice if available
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        
        # Set speech rate
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 30)
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Mendengarkan...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                
            print("Memproses...")
            # Convert speech to text
            command = self.recognizer.recognize_google(audio, language='id-ID')
            print(f"Anda: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "tidak_jelas"
        except sr.RequestError:
            return "error_koneksi"
            
    def process_command(self, command):
        """Process voice commands and respond"""
        
        if "timeout" in command:
            return
            
        elif "tidak_jelas" in command:
            self.speak("Maaf, saya tidak dapat memahami. Bisakah Anda mengulanginya?")
            return
            
        elif "error_koneksi" in command:
            self.speak("Maaf, ada masalah dengan koneksi internet.")
            return
            
        # Greetings
        elif any(word in command for word in ["halo", "hai", "hello"]):
            self.speak("Halo! Saya adalah asisten virtual Anda. Ada yang bisa saya bantu?")
            
        # Time
        elif any(word in command for word in ["jam", "waktu", "time"]):
            current_time = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"Sekarang pukul {current_time}")
            
        # Date
        elif any(word in command for word in ["tanggal", "hari", "date"]):
            today = datetime.datetime.now()
            hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
            bulan = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                    "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            
            day_name = hari[today.weekday()]
            date_str = f"{day_name}, {today.day} {bulan[today.month]} {today.year}"
            self.speak(f"Hari ini adalah {date_str}")
            
        # Open websites
        elif "buka youtube" in command:
            self.speak("Membuka YouTube")
            webbrowser.open("https://youtube.com")
            
        elif "buka google" in command:
            self.speak("Membuka Google")
            webbrowser.open("https://google.com")
            
        elif "buka facebook" in command:
            self.speak("Membuka Facebook")
            webbrowser.open("https://facebook.com")
            
        # Search Google
        elif "cari" in command or "search" in command:
            search_query = command.replace("cari", "").replace("search", "").strip()
            if search_query:
                self.speak(f"Mencari {search_query} di Google")
                webbrowser.open(f"https://google.com/search?q={search_query}")
            else:
                self.speak("Apa yang ingin Anda cari?")
                
        # Calculator
        elif any(word in command for word in ["hitung", "calculate"]):
            self.speak("Mohon maaf, fitur kalkulator belum tersedia.")
            
        # Exit
        elif any(word in command for word in ["keluar", "exit", "bye", "selesai"]):
            self.speak("Terima kasih! Sampai jumpa lagi!")
            return "exit"
            
        # Default response
        else:
            self.speak("Maaf, saya belum mengerti perintah tersebut. Coba katakan 'halo', 'jam berapa', atau 'buka youtube'")
            
    def run(self):
        """Main loop for the assistant"""
        self.speak("Asisten virtual siap membantu Anda!")
        
        while True:
            command = self.listen()
            result = self.process_command(command)
            
            if result == "exit":
                break
                
            print("-" * 50)

if __name__ == "__main__":
    assistant = VirtualAssistant()
    assistant.run()