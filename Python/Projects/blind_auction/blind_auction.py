from replit import clear
#HINT: You can call clear() to clear the output in the console.
from art import logo

other_bidders = "yes"
biding_dict = {}
while other_bidders == "yes":
  print(logo)
  print("welcome to the secret auction program")
  name = input("What is your name?: ")
  bid = int(input("What's your bid?: $"))
  biding_dict[name] = bid

  to_continue = ""
  while to_continue not in ("yes","no"):
    to_continue = input("Are there any other bidders? Type 'yes' or 'no'.")
    if to_continue == "no":
      other_bidders = "no"
    elif to_continue == "yes":
      clear()

wining_bid_name = ""
winning_bid_amount = -999999
for key in biding_dict:
  if biding_dict[key] > winning_bid_amount:
    winning_bid_amount = biding_dict[key]
    winning_bid_name = key

print(f"The winner is {winning_bid_name} with a bid of ${winning_bid_amount}")