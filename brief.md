# A2 Harbour Card Assignment

Before starting, read [AI-use.md](AI-use.md) for the required AI workflow, conversation exports and academic integrity rules.

## Overview

A Harbour Card is a stored-value card that you tap to pay for rides, like the card you use on the MTR. Write a program that replays one day of transactions on one card: rides and top-ups, in the order they happened. For each transaction the program decides whether the card accepts it and what it costs. At the end it prints a short summary, followed by a history of every transaction, accepted or refused.

The rules are short, but they affect each other. Whether a ride gets a discount depends on the transaction before it, and whether a ride is accepted depends on the balance left by everything before it. To get this program right you must be able to follow it, step by step, through a whole day. That is what this assignment teaches and what it checks.

## Description

### Card type

The first input is the card type: 1 means adult, 2 means student, 3 means elder.

### Starting balance

The second input is the balance on the card at the start of the day. It is a whole number from -35 to 3000. A negative balance means the card owes money.

### Transactions

Then the program reads transactions, one at a time. Each transaction is two lines: first its kind, then an amount.

- Kind 1 is a **ride**. The amount is the full adult fare for that ride, a whole number from 1 to 60.
- Kind 2 is a **top-up**. The amount is the money offered, a whole number from 1 to 2000.

Input ends when the kind entered is 0. No amount follows the 0, and the 0 is not a transaction.

Transactions are numbered 1, 2, 3 and so on, in the order they are entered. Refused transactions are counted in the numbering too.

### What a ride costs

First apply the card type:

- An adult pays the full fare.
- A student pays half the full fare. For example, a full fare of 9 costs a student 4.50.
- An elder pays 2, or the full fare if the full fare is less than 2.

Then apply the **interchange discount**. If the transaction just before this ride was a ride that the card accepted, take 1 off the fare you worked out above. A fare never goes below 0. If the transaction just before was a top-up (accepted or refused), or a refused ride, there is no discount. The first transaction of the day never gets the discount.

### When a ride is refused

The card accepts a ride only if both of these are true:

- the balance before the ride is more than 0, and
- the balance after paying the fare would be -35 or more.

The fare checked here is the fare after both steps above. If either condition is false, the ride is refused: nothing is charged and the balance does not change.

### When a top-up is refused

The card accepts a top-up only if all of these are true:

- the amount is a multiple of 50,
- the amount is from 50 to 1000, and
- the balance after adding it would be 3000 or less.

Otherwise the top-up is refused and the balance does not change. A top-up is accepted even when the balance is negative: it pays off what the card owes first.

### Refused transactions

A refused transaction does not change the balance, the fares paid, the number of rides or the number of top-ups. It adds 1 to the count of refused transactions, and it still has a transaction number. The next ride after it gets no interchange discount.

### Lowest balance

The lowest balance is the lowest the balance has been at any moment in the day, including the starting balance.

### Transaction history

Keep a list named `transactions`. Each item is a tuple with three values, in this order: `(kind, accepted, balance_after)`.

- `kind` is the integer 1 for a ride or 2 for a top-up.
- `accepted` is `True` if the transaction was accepted, otherwise `False`.
- `balance_after` is the balance after that transaction. For a refused transaction, it equals the balance before it.

Record every transaction once, in input order, including refusals. Do not record the starting balance as a transaction, and do not record the final kind 0. A day with no transactions has an empty list.

The function `transaction_history(transactions)` prints the records in list order, numbered from 1. It does not read input, calculate fares or decide acceptance again. It returns nothing and must leave the list and its records unchanged. `main()` calls it once after printing the summary. This printed history is part of the program's output.

## Input and output format

Your program is tested automatically, so it must follow this format exactly.

Read each value with these prompts:

| Value | Prompt |
|---|---|
| Card type | `Card type (1 adult, 2 student, 3 elder): ` |
| Starting balance | `Starting balance: ` |
| Kind of each transaction | `Transaction (1 ride, 2 top-up, 0 stop): ` |
| Amount of each transaction | `Amount: ` |

Input is one value per line: the card type, the starting balance, then for each transaction its kind and its amount, then `0`.

After input ends, print **exactly these seven summary lines**, then **one history line for every transaction**, in input order, and nothing else. If there were no transactions, print only the seven summary lines. Labels, capitalisation and punctuation must match exactly. The three summary money values (Fares paid, Lowest balance and Final balance), and the balance on each history line, always show two decimal places. Counts and transaction numbers are plain integers.

```
Card type: <adult|student|elder>
Rides taken: <int>
Top-ups: <int>
Fares paid: <0.00>
Lowest balance: <0.00>
Final balance: <0.00>
Refused: <int>
```

Each history line has this format, with `Ride` or `Top-up` and `accepted` or `refused`:

```text
<number>: <Ride|Top-up> <accepted|refused>. Balance: <0.00>
```

For example, a refused top-up numbered 3, leaving a balance of 14, prints:

```text
3: Top-up refused. Balance: 14.00
```

## How the program is organised

`Card.py` already contains the outline of the program in five parts, one for each function. For each one the `def` line, with its name and parameters, is given, with a comment saying what it returns, and you write the body. For `main()`, the template gives the `def` line and some comments suggesting what `main()` needs to do. They are suggestions, not steps to copy: work out how `main()` handles these requirements before writing its body.

**Do not rename the functions or change their parameters.** The tests and the marker call them by these names, so a renamed function, or one with different parameters, counts as missing. **Use only the five functions supplied in `Card.py`. Do not define additional functions, including helper functions or functions inside another function.**

| Part | Function | What it does |
|---|---|---|
| 1 | `ride_fare(card_type, full_fare, follows_ride)` | Returns what this ride costs, after the card type and the interchange discount. `follows_ride` is `True` if the transaction just before was an accepted ride. |
| 2 | `can_ride(balance, fare)` | Returns `True` if the card accepts a ride costing `fare`, otherwise `False`. |
| 3 | `can_top_up(balance, amount)` | Returns `True` if the card accepts this top-up, otherwise `False`. |
| 4 | `transaction_history(transactions)` | Prints one numbered line per record in the list. Returns nothing and does not change the list. |
| 5 | `main()` | Reads input, processes transactions using parts 1 to 3, records each transaction, and prints the summary. It then calls part 4 to print the history. |

The functions in parts 1 to 3 do no input and no printing. They take values in and return a value. All input happens in `main()`. It prints the summary; `transaction_history` prints the transaction lines.

The last line of `Card.py` is `main()  # Don't change this`, as in the lecture 5 tasks. Leave it there.

This is the whole of `Card.py` as it is in the template:

```python
def ride_fare(card_type, full_fare, follows_ride):
    # Returns the fare for this ride, after the card type and the interchange discount.
    pass  # your code here


def can_ride(balance, fare):
    # Returns True if the card accepts a ride costing fare, otherwise False.
    pass  # your code here


def can_top_up(balance, amount):
    # Returns True if the card accepts this top-up, otherwise False.
    pass  # your code here


def transaction_history(transactions):
    # Prints each recorded transaction in order. Returns nothing.
    pass  # your code here


def main():
    # main() is yours to write, by working through the requirements.
    # Some things it will need to do:
    #   - keep track of the balance, whether the last transaction was an
    #     accepted ride, and the transaction history
    #   - read transactions until the input ends
    #   - for each transaction, decide what to do, using your first three functions
    #   - print the summary and call transaction_history at the end
    pass


main()  # Don't change this
```

## Constraints

Use only what we have covered in lectures 1 to 5:

- the basic types int, float, str and bool; `input()` and `print()`; `int()`, `float()` and `str()`;
- operators, including `//` and `%`;
- conditionals `if`, `elif` and `else`; `while` and `for` loops, `range`, `break` and `continue`;
- lists, tuples, sets and dictionaries as taught in lecture 4 (for lists: indexing, `append`, `len`, `in` and looping over a list);
- the five supplied functions with parameters and `return`, as taught in lecture 5; no additional function definitions;
- basic f-strings such as `f"{x}"`, without format codes.

Do not use string methods, slicing, list methods other than `append`, `sum`, `round`, `sorted`, `try` and `except`, `import`, or anything else not yet covered.


The `"{:.2f}".format(...)` shown in Tips is supplied. Use it exactly as shown.

All code must use only the features above. You must be able to read, trace and explain every line of your program.

## Worked examples

Each example is a full console session. The value after each prompt is what the user types.

### Example 1

```
Card type (1 adult, 2 student, 3 elder): 2
Starting balance: 20
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 12
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 9
Transaction (1 ride, 2 top-up, 0 stop): 2
Amount: 100
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 5
Transaction (1 ride, 2 top-up, 0 stop): 0
Card type: student
Rides taken: 3
Top-ups: 1
Fares paid: 12.00
Lowest balance: 10.50
Final balance: 108.00
Refused: 0
1: Ride accepted. Balance: 14.00
2: Ride accepted. Balance: 10.50
3: Top-up accepted. Balance: 110.50
4: Ride accepted. Balance: 108.00
```

The first ride costs 6.00, half of 12. The second ride comes straight after an accepted ride, so it costs half of 9, less 1: 3.50. The balance is now 10.50, the lowest of the day. The top-up comes between the second ride and the last one, so the last ride gets no discount and costs 2.50. Nothing is refused, but all four accepted transactions still appear in the history.

### Example 2

```
Card type (1 adult, 2 student, 3 elder): 1
Starting balance: 10
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 30
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 14
Transaction (1 ride, 2 top-up, 0 stop): 2
Amount: 70
Transaction (1 ride, 2 top-up, 0 stop): 2
Amount: 50
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 20
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 50
Transaction (1 ride, 2 top-up, 0 stop): 0
Card type: adult
Rides taken: 2
Top-ups: 1
Fares paid: 50.00
Lowest balance: -20.00
Final balance: 10.00
Refused: 3
1: Ride accepted. Balance: -20.00
2: Ride refused. Balance: -20.00
3: Top-up refused. Balance: -20.00
4: Top-up accepted. Balance: 30.00
5: Ride accepted. Balance: 10.00
6: Ride refused. Balance: 10.00
```

Transaction 1 takes the balance from 10 to -20. That is allowed, because the balance before was more than 0 and -20 is not below -35. Transaction 2 is refused because the balance is no longer more than 0. Transaction 3 is refused because 70 is not a multiple of 50. Transaction 4 tops up 50, so the balance is 30. Transaction 5 comes after a top-up, so it gets no discount and costs 20, leaving 10. Transaction 6 comes after an accepted ride, so it costs 49, which would leave -39. That is below -35, so it is refused.

### Example 3

```
Card type (1 adult, 2 student, 3 elder): 3
Starting balance: 2950
Transaction (1 ride, 2 top-up, 0 stop): 2
Amount: 100
Transaction (1 ride, 2 top-up, 0 stop): 2
Amount: 50
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 1
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 8
Transaction (1 ride, 2 top-up, 0 stop): 1
Amount: 1
Transaction (1 ride, 2 top-up, 0 stop): 0
Card type: elder
Rides taken: 3
Top-ups: 1
Fares paid: 2.00
Lowest balance: 2950.00
Final balance: 2998.00
Refused: 1
1: Top-up refused. Balance: 2950.00
2: Top-up accepted. Balance: 3000.00
3: Ride accepted. Balance: 2999.00
4: Ride accepted. Balance: 2998.00
5: Ride accepted. Balance: 2998.00
```

Work through this example yourself before you start your specification. Why is transaction 1 refused, why does the last ride cost nothing, and why is the lowest balance the starting balance?

## Tips

### Printing the money values

The money values must always print with exactly two decimal places, for example 12.00, 10.50 and -20.00. A balance can be a whole number of type int, which would print as 12 with no decimals, or a float such as 10.5, which would print as 10.5. This handles both:

```python
print("Fares paid:", "{:.2f}".format(fares_paid))
```

`"{:.2f}"` always shows exactly two decimals. It is given to you because format codes are taught later. Use it for the three summary money values and for the balance on every history line, with your own variable in the brackets.

### Halves are exact

A student fare is half a whole number, so every fare and every balance in this assignment is a whole number or ends in .5. Python stores these values exactly, so a comparison such as `balance - fare >= -35` is safe, and so is a function check such as `ride_fare(2, 9, False) == 4.5`.


## Testing your program

**The target: every decision in the program is tested at least once in each direction, and every boundary is tested from both sides.** A boundary is tested from both sides when you have one case exactly on it and one case just past it. For example, a ride that leaves the balance at exactly -35 and a ride that would take it below -35.

There are two kinds of test, and both go in `tests.txt`.

**Function checks** test one part on its own. Each is one line: a call to one of your functions, `==`, and the value you expect. For example:

```
ride_fare(1, 12, False) == 12
can_top_up(100, 70) == False
```

Write up to 15. Function checks are the quick way to test the boundaries of one rule. These return-value checks apply to parts 1 to 3 only. Test `transaction_history` through program cases, because it prints rather than returning a value. Your cases should exercise both kinds, both outcomes, numbering, order, unchanged balances on refusals, and an empty history.

**Program cases** test the whole program, as in A1: the input, one value per line, then the expected output. Separate cases with a blank line. Write up to 8. Program cases are the way to test what happens across several transactions, such as whether a refused ride stops the next ride getting the discount. Some decisions can only be tested with a program case.

Put the function checks first, under a line `# Function checks`, then the program cases under a line `# Program cases`. `tests.txt` in the template shows the layout, with Example 1 as the first program case:

```
# Function checks
ride_fare(1, 12, False) == 12
can_top_up(100, 70) == False

# Program cases
2
20
1
12
1
9
2
100
1
5
0
Card type: student
Rides taken: 3
Top-ups: 1
Fares paid: 12.00
Lowest balance: 10.50
Final balance: 108.00
Refused: 0
1: Ride accepted. Balance: 14.00
2: Ride accepted. Balance: 10.50
3: Top-up accepted. Balance: 110.50
4: Ride accepted. Balance: 108.00
```

**Predict before you run.** For each test, work out the expected value from the rules first, then run it. A test only proves something if you predicted the result. An expected value copied from your program's output does not catch bugs.

`python test.py` checks the history function directly, runs the three worked examples and a day with no transactions, and runs all of your own tests, both kinds.

You may assume all input is valid, as described above. You do not need to test invalid input.
