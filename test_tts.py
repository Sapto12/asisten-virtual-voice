import speech_recognition as sr
import time

def test_speech_to_text():
    # Initialize recognizer
    r = sr.Recognizer()
    
    # List available microphones
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")
    
    # Test microphone
    print("\nTesting microphone...")
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... (tunggu 2 detik)")
            r.adjust_for_ambient_noise(source, duration=2)
            print("Ambient noise adjustment selesai!")
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        return
    
    print("\n=== SPEECH-TO-TEXT TEST ===")
    print("Silakan bicara setelah mendengar 'RECORDING...'")
    print("Katakan sesuatu dalam bahasa Indonesia atau Inggris")
    print("Press Ctrl+C untuk keluar\n")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("RECORDING... (bicara sekarang)")
                # Listen for audio with timeout
                audio = r.listen(source, timeout=1, phrase_time_limit=5)
                
            print("Processing...")
            
            # Try to recognize speech
            try:
                # Using Google Web Speech API (free)
                text = r.recognize_google(audio, language='id-ID')  # Indonesian
                print(f"Anda mengatakan: '{text}'")
                
            except sr.UnknownValueError:
                # Try English if Indonesian fails
                try:
                    text = r.recognize_google(audio, language='en-US')
                    print(f"You said: '{text}'")
                except sr.UnknownValueError:
                    print("Maaf, tidak dapat memahami audio")
                    
            except sr.RequestError as e:
                print(f"Error connecting to Google service: {e}")
                print("Cek koneksi internet Anda")
                
        except sr.WaitTimeoutError:
            print("Tidak ada suara terdeteksi, mencoba lagi...")
            
        except KeyboardInterrupt:
            print("\nTest selesai!")
            break
            
        print("-" * 40)

if __name__ == "__main__":
    test_speech_to_text()