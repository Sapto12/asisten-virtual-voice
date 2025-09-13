import speech_recognition as sr


def simple_mic_test():
    r = sr.Recognizer()
    
    print("simple mic test")
    print("available microphones:")
    