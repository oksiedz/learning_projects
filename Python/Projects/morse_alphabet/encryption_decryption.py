from morse_dict import morse_dict


def encrypt(text):
    output_text = "/"
    for char in text:
        if char in morse_dict:
            output_text += morse_dict[char] + "/"
        if char in (" ", ",", "."):
            output_text += "/"
    # end text
    output_text += "/"
    return output_text + "/"


def decrypt(text):
    output_text = ""
    # example: /.../___/...//.../___/...//
    decryption_list = text.split("/")
    decode_morse = dict(zip(morse_dict.values(), morse_dict.keys()))
    for element in decryption_list:
        if element == "":
            output_text += " "
        else:
            output_text += decode_morse[element]
    return output_text
