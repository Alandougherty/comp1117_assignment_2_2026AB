def ride_fare(card_type, full_fare, follows_ride):
    # Returns the fare for this ride, after the card type and the interchange discount.
    #logic: if card_type is adualts, the fare should remains the same. 
    #if card_type is students, the fare should times 0.5
    #if card_type is elderlys, if full fare is larger than or equals to 2, the fare equals to 2.
    #                          if the full fare is less than 2, the fare remains the same.
    #if the follows_ride is true, that means the last previous transaction accpet a ride, the fare should minus 1 
    #save the fare after calculation. 
    #pass  # your code here
    if card_type == 1:
        fare = full_fare
    elif card_type == 2:
        fare = full_fare * 0.5
    elif card_type == 3:
        if full_fare >= 2:
            fare = 2
        else:
            fare = full_fare
    
    if follows_ride:
        fare = fare - 1
    
    if fare < 0:
        fare = 0
    
    return fare

def can_ride(balance, fare):
    # Returns True if the card accepts a ride costing fare, otherwise False.
    #def can_ride(balance, fare) to judge whether to refuse a ride or not. 
    #can_ride is true if both the following is true:
    #the balance before the ride is greater than 0, and
    #the balance after paying the fare would be euqal to or greater than -35.
    #pass  # your code here
    if balance > 0 and balance - fare >= -35:
        return True
    else:
        return False

def can_top_up(balance, amount):
    # Returns True if the card accepts this top-up, otherwise False.
    #def can_top_up(balance, amount) to judge whether to refuse a top-up or not.
     #can_top_up is true if all the following is true:
     #the amount is a multiple of 50
     #he amount is between 50 to 1000
     #the balance after adding it would be equal to or less than 3000. 
    #pass  # your code here
    if amount % 50 == 0 and 50 <= amount <= 1000 and balance + amount <= 3000:
        return True
    else:
        return False

def transaction_history(transactions):
    # Prints each recorded transaction in order. Returns nothing.
    #the for loop goes through the list in order 1, and number starts at 1 and increases by 1 with each record
    # if transactions is empty, the for loop runs zero times and nothing is printed
    pass  # your code here
    number = 1
    for kind, accepted, balance_after in transactions:
        if kind == 1:
            transaction_type = "Ride"
        else:
            transaction_type = "Top-up"
        
        if accepted:
            status = "accepted"
        else:
            status = "refused"
        
        print(f"{number}: {transaction_type} {status}. Balance:","{:.2f}".format(balance_after))
        number += 1

def main():
    # main() is yours to write, by working it out with the AI assistant.
    # Some things it will need to do:
    #   - keep track of the balance, whether the last transaction was an
    #     accepted ride, and the transaction history
    #   - read transactions until the input ends
    #   - for each transaction, decide what to do, using your first three functions
    #   - print the summary and call transaction_history at the end

    #1. Initialise variables (balance, follows_ride, counters, transactions list, fares_paid, lowest_balance)
    # 2. Loop while kind != 0:
    #    Read kind and amount
    #    (1) If kind == 1:
    #        First: calculate fare using ride_fare(card_type, amount, follows_ride)
    #        Second: check acceptance using can_ride(balance, fare)
    #                 If accepted: update balance, increment rides_taken, add fare to fares_paid, set follows_ride to True
    #                 If refused: balance unchanged, increment refused, set follows_ride to False
    #    (2) If kind == 2:
    #        Check acceptance using can_top_up(balance, amount)
    #        If accepted: update balance, increment top_ups, set follows_ride to False
    #        If refused: balance unchanged, increment refused, set follows_ride to False
    #    (3) Record transaction in list
    #    (4) Update lowest_balance if needed
    # 3. Print summary and call transaction_history
 
    # Ask for card type
    card_type = int(input("Card type (1 adult, 2 student, 3 elder): "))
    
    # Ask for starting balance, convert to float to handle potential .5 values
    balance = float(input("Starting balance: "))
    
    # Initialize tracking variables
    rides_taken = 0
    top_ups = 0
    fares_paid = 0.0
    refused = 0
    follows_ride = False  # First transaction never gets discount
    lowest_balance = balance  # Include starting balance
    transactions = []
    
    # Read first transaction kind
    kind = int(input("Transaction (1 ride, 2 top-up, 0 stop): "))
    
    # Process transactions until kind is 0
    while kind != 0:
        amount = float(input("Amount: "))
        
        if kind == 1:  # Ride
            # Calculate fare first (before checking acceptance)
            fare = ride_fare(card_type, amount, follows_ride)
            if can_ride(balance, fare):
                # Accepted ride
                balance = balance - fare
                rides_taken += 1
                fares_paid += fare
                follows_ride = True  # Next ride gets discount if accepted
                accepted = True
            else:
                # Refused ride
                follows_ride = False  # Next ride gets no discount
                refused += 1
                accepted = False
        
        elif kind == 2:  # Top-up
            # Check if top-up can be accepted
            if can_top_up(balance, amount):
                # Accepted top-up
                balance = balance + amount
                top_ups += 1
                follows_ride = False  # Next ride gets no discount
                accepted = True
            else:
                # Refused top-up
                follows_ride = False  # Next ride gets no discount
                refused += 1
                accepted = False
        transactions.append((kind, accepted, balance))
        
        # Update lowest balance if current balance is lower
        if balance < lowest_balance:
            lowest_balance = balance
        
        # Read next transaction kind
        kind = int(input("Transaction (1 ride, 2 top-up, 0 stop): "))
    
    # Determine card type string
    if card_type == 1:
        card_type_str = "adult"
    elif card_type == 2:
        card_type_str = "student"
    else:
        card_type_str = "elder"
    
    # Print summary
    print("Card type:", card_type_str)
    print("Rides taken:", rides_taken)
    print("Top-ups:", top_ups)
    print("Fares paid:", "{:.2f}".format(fares_paid))
    print("Lowest balance:", "{:.2f}".format(lowest_balance))
    print("Final balance:", "{:.2f}".format(balance))
    print("Refused:", refused)
    
    # Print transaction history
    transaction_history(transactions)

main()  # Don't change this
