import replit
import encryption_decryption


def morse_translator():
    continue_loop = True
    while continue_loop:
        print("Welcome to the morse translator!")
        action = ""
        while action not in ("encrypt", "decrypt"):
            action = input("Please write:\n"
                           "- 'encrypt' if you want to translate text into Morse code\n"
                           "- 'decrypt' if you want to translate Morse code into text\n").lower()

        input_text = input(f"Please write down text to be {action}ed:\n").lower()

        if action == "encrypt":
            print(encryption_decryption.encrypt(input_text))
        if action == "decrypt":
            print(encryption_decryption.decrypt(input_text))

        next_translation = ""
        while next_translation not in ("yes", "no"):
            next_translation = input("Do you want to translate further? Please write yes or no:\n").lower()
            if next_translation == "no":
                continue_loop = False
            else:
                replit.clear()