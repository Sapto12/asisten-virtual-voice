import speech_recognition as sr
import time

def test_speech_to_text():
    r =sr.Recognizer()
    
    
    print("testing microphone..")
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... (tunggu 2 detik)")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Ambient noise adjustment selesai!")
        
    print("\n==SPEECH-TO-TEXT TEST==")
    print("Silakan bicara sekarang...")
    print("katakan sesuatu dalam bahasa indonesia atau bahasa inggris")
    
    while True:
        with sr.Microphone() as source:
            print("RECORDING...(bicara sekarang)")
            
            audio = r.listen(source, timeout=1 , phrase_time_limit=5)
            
        print("Processing...")
        
        try:
            text = r.recognize_google(audio, language="id-ID")
            print(f"you said : {text}")
        except sr.UnknownValueError:
            print("maaf, saya tidak mengerti. Silakan coba lagi.")
        
        except sr.RequestError as e:
            print(f"error connecting to google service : {e}")
            print("cek koneksi internet anda")
        
        except sr.WaitTimeoutError:
            print("waktu habis, tidak ada suara yang terdeteksi. Silakan coba lagi.")
            
        except KeyboardInterrupt:
            print("\nTest selesai.")
            break
        
        print("-" * 40)
        
if __name__ == "__main__":
    test_speech_to_text()
        
    
        