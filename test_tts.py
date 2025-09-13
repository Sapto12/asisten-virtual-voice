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
            return
        print("\nSPEECH TO TEXT TEST")
        print("silahkan bicara setelah mendengar RECORDING")
        print("katakan sesuatu dalam bahasa indonesia atau inggris")
        print("press ctrl+c to stop ")

        while True:
            try:
                with sr.Microphone() as source:
                    print("RECORDING (bicarase sekarang)...")

                    audio = r.listen(source, timeout=1, phrase_time_limit=10)
                    print("RECORDING selesai, memproses...")

                    try:
                        text = r.recognize_google(audio, language="id-ID")
                        print(f"Anda mengatakan : {text}")
                    except sr.UnknownValueError:

                        try:
                            text = r.recognize_google(audio, language="en-US")
                            print(f"You said : {text}")
                        except sr.UnknownValueError:
                            print("Google Speech Recognition tidak dapat memahami audio")
                        except sr.RequestError as e:
                            print(f"Permintaan ke Google Speech Recognition gagal; {e}")
                            print("mungkin karena masalah koneksi internet")
                    except sr.WaitTimeoutError as e: 
