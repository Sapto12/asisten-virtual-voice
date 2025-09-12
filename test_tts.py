import pyttsx3

def test_text_to_speech():
    engine = pyttsx3.init()
    
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    
    voices = engine.getProperty('voices')
    if len(voices) > 1 :
        engine.setProperty('voice' , voices[1].id)
        
    print("testing text to speech...")
    engine.say("Hallo! saya adalah asisten virtual anda. selamat datang!")
    engine.runAndWait()
    
    print("text-to-speech test selesai!")
    
if __name__ == "__main__":
    test_text_to_speech()
    