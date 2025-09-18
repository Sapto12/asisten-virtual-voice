import speech_recognition as sr


def simple_mic_test():
    r = sr.Recognizer()
    
    print("simple mic test")
    print("available microphones:")
    
    for i, name  in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i} : {name}")
        
    mic_index = None
    
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("\nMicrophone terdeteksi")
            print("bicara 'HELLO TEST'untuk menguji mikrofon")
            r.adjust_for_ambient_noise(source , duration=3)
            
            print("mulai bicara")
            audio = r.listen(source)
                     
        print("Audio captured! Processing...")
        text = r.recognize_google(audio, language='en-US')
        print(f"Result: '{text}'")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Troubleshooting:")
        print("1. Cek permission mikrofon")
        print("2. Pastikan mikrofon tidak dipakai aplikasi lain")
        print("3. Bicara lebih keras/dekat")

if __name__ == "__main__":
    simple_mic_test()