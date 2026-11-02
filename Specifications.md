# A2 Harbour Card: My Specifications

**Finish this file first, before any code is written.** You supply the
reasoning and fill in this worksheet in your own words, with the AI
assistant's help. It describes the problem only, not how your program will solve
it.

## Input and output types

What the program reads and what it prints, with the type of each value:
int, float, str, bool. Say why.

- **Inputs:** what values does the program read, in what order, and what
  type is each?
1. card type (int)
2. starting balance (int)
3. kind of each trasaction (int)
4. amount of each transaction (int)

- **Outputs:** what does the program print, what type is each value, and
  how are the money values printed?
1. Card type: str
2. Rides taken: int
3. Top-ups: int
4. Fares paid: float
5. Lowest balance: float
6. Final balance: float
7. Refused: int
8. history for each transaction, in the oder of <number>: <Ride|Top-up> <accepted|refused>. Balance: <0.00>
The money values should be printed in exactly two decimal places.

## The rules in my own words

State each rule in your own words, not the assignment's wording pasted back.
For every boundary, write **both sides**: what happens exactly on it, and
what happens just past it.

- **What a ride costs:** the card type, then the interchange discount.
1. An adult pays the full fare.
2. A student pays half the full fare. 
3. An elder pays: 2, if full fare is larger than or equals to 2, or full fare, if the full fare is less than 2.
rules of interchange discount: 
1. take 1 off the fare of the present ride costs if and only if the last previous transaction was a accepted ride. That means if the transaction just before was a top-up (accepted or refused), or a refused ride, there is no discount. 
2. the fare should be not less than 0.
3. The first transaction of the day never gets the discount.

- **When a ride is refused:**
The ride is refused if either condition below is true:
1. he balance before the ride is equal or less than 0, and
2. the balance after paying the fare would be less than -35.
if the ride is refused, the balance will not change. 

- **When a top-up is refused:**
A top-up is refused if either condition below is true:
1. the amount is not a multiple of 50
2. the amount is smaller than 50 or greater than 1000
3. the balance after adding it would be more than 3000. 
if the top-up is refused, the balance will not change. 

Otherwise the top-up is refused and the balance does not change. A top-up is accepted even when the balance is negative: it pays off what the card owes first.

- **What a refused transaction changes, and what it does not:**
not change: balance, fares paid, number of rides or number of top-ups. 
change: adds 1 to the count of refused transactions, and it still has a transaction number. The next ride after it gets no interchange discount.

- **The lowest balance:**

The lowest balance is the minimum of the balance at any moment in the day, including the starting balance.

- **The transaction history:** which transactions appear, their order and numbering, and what each line shows. How is this different from your chat history?
1. Which transactions appear: Every transaction from the day—rides and top-ups, both accepted and refused 
The starting balance and the final 0 are not transactions. 
2. Their order and numbering: They appear in input order, numbered starting from 1. Refused transactions still get a number and appear in their original position 
3. What each line shows: Each line shows the number, whether it was a Ride or Top-up, whether it was accepted or refused, and the balance after that transaction (with two decimal places). For refused transactions, this balance equals the balance before.

difference: the chat history only shows the type and the amount of the transaction. the transaction history not only shows the trype of the transaction, but also shows whether it was accepted or refused, and the balance after that transaction (with two decimal places).

boundaries:
1. starting balance = 0: ride is refused
   starting balance = 1: ride is accepted
2. balance after paying the fare = -34: ride is accepted
   balance after paying the fare = -35: ride is accepted 
   balance after paying the fare = -36: ride is refused
3. an elderly pays for a full fare that cost $2: the amount of payment should be 2.
   an elderly pays for a full fare that cost $1: the amount of payment should be 1
4. addition of top-up = 999: top-up is accepted.
   addition of top-up = 1000: top-up is accepted.
   addition of top-up = 1001: top-up is refused.
5. addition of top-up = 51: top-up is accepted.
   addition of top-up = 50: top-up is accepted.
   addition of top-up = 49: top-up is refused.
   addition of top-up = 70: top-up is refused.
6. total top-up = 2999: top-up is accepted.
   total top-up = 3000: top-up is accepted.
   total top-up = 3001: top-up is refused.
7. Full fare = 1 for student. Half is 0.50. Then if discount applies: 0.50 - 1 = -0.50 → 0.00.



## Edge cases

The inputs where something special happens, and what the program must do in
each. For example: a ride straight after a refused ride, or a top-up that
lands exactly on 3000.

1. a ride straight after a refused ride: discount = 0
2. a top-up that lands exactly on 3000: accpet the top-up
3. a day with no transactions: Rides taken: 0, Top-ups: 0, Fares paid: 0.00, Lowest balance = starting balance, Final balance = beginning balance, Refused: 0, trasaction history: there is no transaction today. 
4. The first transaction ever (no previous transaction for discount): no discount 
5. A ride costing 0 after discount: transaction history: ride, accpeted, balance does not change
   e.g. an elderly's fare that originally cost $1, after the discount of following ride it cost 0.
6. A starting balance that is already negative: 
   top-up can be accepted when balance after adding is equal to or larger than -35.
   ride can not be accpeted
7. All transactions refused. Final balance = starting balance, Fares paid = 0
8. A ride that exactly hits a balance of 0 after paying: accepted
9. Full fare = 1 for student. Half is 0.50. Then if discount applies: 0.50 - 1 = -0.50 → 0.00.
10. Multiple top-ups in a row, then a ride: The ride gets no discount because the previous transaction was a top-up, not an accepted ride


## logic：
   1 def ride_fare(card_type, full_fare, follows_ride) to calculate the fare of each transaction.
     if card_type is adualts, the fare should remains the same. 
     if card_type is students, the fare should times 0.5
     if card_type is elderlys, if full fare is larger than or equals to 2, the fare equals to 2.
                               if the full fare is less than 2, the fare remains the same.
     if the follows_ride is true, that means the last previous transaction accpet a ride, the fare should minus 1 
     save the fare after calculation. 
   2 def can_ride(balance, fare) to judge whether to refuse a ride or not. 
     can_ride is true if both the following is true:
     the balance before the ride is greater than 0, and
     the balance after paying the fare would be euqal to or greater than -35.
   3 def can_top_up(balance, amount) to judge whether to refuse a top-up or not.
     can_top_up is true if all the following is true:
     the amount is a multiple of 50
     the amount is between 50 to 1000
     the balance after adding it would be equal to or less than 3000. 
   4 def transaction_history(transactions) to record each transaction by creating a list and add a tuple for each transaction. 
      The tuple include three values, in this order: (kind, accepted, balance_after)
      it prints the records in list order, numbered from 1. 
      if there is an empty list (no transactions) , it prints nothing
      if there is a refused transaction balance_after equal the balance before 
     
   5 def main() to assemble each functions.
     keep track of the balance, whether the last transaction was an accepted ride, and the transaction history
     read transactions until the input ends
     for each transaction, decide what to do, using your first three functions
     print the summary and call transaction_history at the end

     1. Initialise variables (balance, follows_ride, counters, transactions list, fares_paid, lowest_balance)
     2. Loop while kind != 0:
        Read kind and amount
        (1) If kind == 1:
            First: calculate fare using ride_fare(card_type, amount, follows_ride)
            Second: check acceptance using can_ride(balance, fare)
                     If accepted: update balance, increment rides_taken, add fare to fares_paid, set follows_ride to True
                     If refused: balance unchanged, increment refused, set follows_ride to False
        (2) If kind == 2:
            Check acceptance using can_top_up(balance, amount)
            If accepted: update balance, increment top_ups, set follows_ride to False
            If refused: balance unchanged, increment refused, set follows_ride to False
        (3) Record transaction in list
        (4) Update lowest_balance if needed
     3. Print summary and call transaction_history


