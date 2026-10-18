def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1 / n2


operation = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def select_operator():
    operator = ""
    while operator not in operation:
        operator = input("Please provide operation you would like to do. Insert +, -, * or /.\n")
    return operator


def provide_number():
    num_is_number = False
    number = ""
    while not num_is_number:
        try:
            number = float(input("Please provide number (example 1.2): "))
            num_is_number = True
        except ValueError:
            num_is_number = False
    return number


def calculator():
    while True:
        print("Welcome to the Python simple calculator.")
        number_1 = provide_number()
        operator = select_operator()
        number_2 = provide_number()
        calculation = operation[operator]
        result = calculation(number_1, number_2)

        print(f"{number_1} {operator} {number_2} equals {result}")

        continue_question = ""
        while continue_question not in ("yes", "no"):
            continue_question = input("Do you want to continue using calculator on above result? yes/no: ").lower()
            if continue_question == "no":
                continue_question2 = ""
                while continue_question2 not in ("clear", "close"):
                    continue_question2 = input("To close application write close, "
                                               "to clear and start from the beginning write clear. ").lower()
                    if continue_question2 == "clear":
                        calculator()
                    elif continue_question2 == "close":
                        print("Application calculator is closed")
                        return 0
            elif continue_question == "yes":
                operator = select_operator()
                number_1 = result
                number_2 = provide_number()
                calculation = operation[operator]
                result = calculation(number_1, number_2)
                print(f"{number_1} {operator} {number_2} equals {result}")
                continue_question = ""


calculator()
