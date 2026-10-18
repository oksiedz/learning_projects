from graphics import logo
# constant variables
from constant import WATER, MILK, COFFEE, COST, ESPRESSO, LATTE, CAPPUCCINO, REPORT, OFF, YES, NO, QUARTERS, DIMES, \
    NICKLES, PENNIES, ZERO, ML, G
# dictionaries
from dictionaries import MENU, resources, value_of_coin


def print_report(money, resources_dict):
    """Input: value of money and dictionary of resources
    Outcome: prints all resources state."""
    for key, value in resources_dict.items():
        if key in (WATER, MILK):
            unit = ML
        else:
            unit = G
        print(f"{key.title()}: {value} {unit}")
    print(f"Money: ${money}")


def return_resource_from_menu(order_name, ingredient, dictionary):
    """Input: order name, ingredient and dictionary
    Output: return the needed resource per order"""
    if order_name == ESPRESSO and ingredient == MILK:
        return int(0)
    else:
        return int(dictionary[order_name]["ingredients"][ingredient])


def return_resource_from_resources(ingredient, available_resources):
    """Input: ingredient name and available resources
    Output: value of resources"""
    return int(available_resources[ingredient])


def resource_enough(needed, available, resource_name):
    """Input needed and available water, coffee and milk
    Output boolean true - if available resources are higher or equal needed one"""
    if needed > available:
        return resource_name


def check_resources(order, menu, available_resources):
    """Input: type of coffee as order and dictionary with resources
    Output: boolean if there is enough resources to do the order"""
    needed_water = return_resource_from_menu(order, WATER, menu)
    needed_coffee = return_resource_from_menu(order, COFFEE, menu)
    needed_milk = return_resource_from_menu(order, MILK, menu)

    available_water = return_resource_from_resources(ingredient=WATER, available_resources=available_resources)
    available_coffee = return_resource_from_resources(ingredient=COFFEE, available_resources=available_resources)
    available_milk = return_resource_from_resources(ingredient=MILK, available_resources=available_resources)

    # print(f"Needed water: {needed_water}, coffee: {needed_coffee}, milk: {needed_milk}")
    # print(f"Available water: {available_water}, coffee: {available_coffee}, milk: {available_milk}")

    lacking_resources = ""
    if resource_enough(needed_water, available_water, WATER) == WATER:
        lacking_resources += WATER
        if resource_enough(needed_milk, available_milk, MILK) == MILK:
            lacking_resources += " and " + MILK
        if resource_enough(needed_coffee, available_coffee, COFFEE) == COFFEE:
            lacking_resources += " and " + COFFEE
    elif resource_enough(needed_milk, available_milk, MILK) == MILK:
        lacking_resources += MILK
        if resource_enough(needed_coffee, available_coffee, COFFEE) == COFFEE:
            lacking_resources += " and " + COFFEE
    elif resource_enough(needed_coffee, available_coffee, COFFEE) == COFFEE:
        lacking_resources += COFFEE

    return lacking_resources


def is_int(number):
    """functions take as input number and checks if it is integer"""
    try:
        int(number)
        return True
    except ValueError:
        return False


def coin_input(coin_type):
    number = ""
    while not is_int(number):
        number = input(f"Please provide number of {coin_type}: ")
    return number


def insert_coins():
    """function take input from the console and returns the sum of coins"""
    quarters = float(coin_input(QUARTERS))
    dimes = float(coin_input(DIMES))
    nickles = float(coin_input(NICKLES))
    pennies = float(coin_input(PENNIES))
    sum_of_coins = quarters * value_of_coin[QUARTERS] + dimes * value_of_coin[DIMES] + nickles * value_of_coin[NICKLES]\
                   + pennies * value_of_coin[PENNIES]
    return sum_of_coins


def check_price(order, menu):
    """function based on the order and menu returns the cost of the drink"""
    return float(menu[order][COST])


def update_resource(type_of_resource, available_resources, amount_to_diminish):
    """function based on type, available resource and amount_to_diminish
    decreases the value in available_resources"""
    available_resources[type_of_resource] = available_resources[type_of_resource] - amount_to_diminish


def update_all_resources(av_resources, order):
    """"function based on dictionary with resources and order updates the dictionary with resources"""
    update_resource(type_of_resource=WATER, available_resources=av_resources,
                    amount_to_diminish=return_resource_from_menu(order_name=order,
                                                                 ingredient=WATER, dictionary=MENU))
    update_resource(type_of_resource=MILK, available_resources=av_resources,
                    amount_to_diminish=return_resource_from_menu(order_name=order,
                                                                 ingredient=MILK, dictionary=MENU))
    update_resource(type_of_resource=COFFEE, available_resources=av_resources,
                    amount_to_diminish=return_resource_from_menu(order_name=order,
                                                                 ingredient=COFFEE, dictionary=MENU))


def coffee_machine():
    """Coffee Machine simulator"""
    program_working = 1
    profit = 0
    while program_working == 1:
        print(logo)
        answer = ""
        while answer not in (ESPRESSO, LATTE, CAPPUCCINO, OFF, REPORT):
            answer = input("What would you like? (espresso/latte/cappuccino): ").lower()
        if answer == OFF:
            program_working = 0
        elif answer == REPORT:
            print_report(money=profit, resources_dict=resources)
        else:
            resources_status = check_resources(order=answer, menu=MENU, available_resources=resources)
            if resources_status == "":
                # print("enough_resources")
                # print(f"price: {check_price(answer, MENU)}")

                # check price
                inserted_coins = insert_coins()
                price = check_price(order=answer, menu=MENU)
                difference = round(inserted_coins - price, 2)

                if difference < ZERO:
                    print("Sorry that's not enough money. Money refunded.")
                else:
                    if difference > ZERO:
                        print(f"Here is ${difference} dollars in change.")
                    # add price to the profit
                    profit += price
                    # update available_resources
                    update_all_resources(av_resources=resources, order=answer)
                    print(f"Here is your {answer}. Enjoy!")
                # print_report(money=profit, resources_dict=resources)
            else:
                print(f"Sorry there is not enough {resources_status}")
                new_order = ""
                while new_order not in (YES, NO):
                    new_order = input("Do you want to start new order? yes/no: ").lower()
                if new_order == NO:
                    program_working = 0
                else:
                    coffee_machine()


coffee_machine()
