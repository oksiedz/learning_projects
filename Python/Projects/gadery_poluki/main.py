from translator import gaderypoluki_translator


def gaderypoluki():
    main_loop = True
    while main_loop:
        action = ""
        print("Welcome to the GADERY POLUKI cipher")
        while action not in ("encrypt", "decrypt"):
            action = input("Please write:\n"
                           "- encrypt to encrypt inserted text\n"
                           "- decrypt to decrypt inserted text\n").lower()

        input_text = input(f"Please provide the text to be {action}ed:\n").lower()
        print(gaderypoluki_translator(input_text))

        continue_loop = ""
        while continue_loop not in ("yes", "no"):
            continue_loop = input("Write yes to translate next text or no to close the program.\n").lower()
            if continue_loop == "no":
                main_loop = False

gaderypoluki()