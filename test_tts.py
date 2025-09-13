import speech_recognition as sr
import time

def test_speech_to_text():
    r =sr.Recognizer()
    
    
    print("testing microphone..")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index} : {name}")

        print("\nTesting microphone")
        try:
            with sr.Microphone() as source:
                print("adjusting for ambient noise (tunggu 2 detik)")
                r.adjust_for_ambient_noise(source, duration=2)
                print("ambient noise adjustment selesai")
        
        except Exception as e:
            print(f"error acessing microphone {e}")