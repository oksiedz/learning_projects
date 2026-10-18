import dict

def gaderypoluki_translator(text):
    output_text = ""
    for char in text:
        if char in dict.dictionary:
            output_text += dict.dictionary[char]
        else:
            output_text += char
    return output_text