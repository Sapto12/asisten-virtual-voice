import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os



class VirtualAssistant:
        def __init__(self):
            self.recognizer = sr.Recognizer()
            
            self.engine = pyttsx3.init()
            self.setup_voice()
            
            self.name = "Asisten"
            
        def setup_voice(self):
            """setup voice properties"""
            voices = self.engine.getProperty('voices')
            
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
                
                
            rate =  self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate - 30)
            
        def speak(self, text):
            """Convert text to speech"""
            print(f"{self.name}: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        
        def listen(self):
            """listen for voice and convert to text"""
            
            try:
                with sr.Microphone() as source:
                    print('mendengrarkan...')
                    
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                    
                print("memproses...")
                
                command = self.recognizer.recognize_google(audio, language='id-ID')
                print(f"Anda: {command}")
                return command.lower()
            except sr.WaitTimeoutError:
                return "timeout"
            except sr.UnknownValueError:
                return "tidak_mengerti"
            except sr.RequestError:
                return "error_koneksi"
        
        def process_command(self, command):
            """process voice command and respond"""
            
            if "timeout" in command:
                return
            
            elif "tidak_mengerti" in command:       
                self.speak("Maaf, saya tidak mengerti. Bisa ulangi?")
                return
            elif "error_koneksi" in command:
                self.speak("Maaf, ada masalah koneksi. Coba lagi nanti.")
                return
            elif any(word in command for word in [""halo", "hai", "hello""]):
                self.speak("Halo! saya asisten virtual mu Ada yang bisa saya bantu?")
                      
            