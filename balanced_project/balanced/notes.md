# what are models, or what can they be...
- a collection of things with shared set of information needed on each thing (e.g. books, movies, authors, etc.)
- can be used for user selection input when selection input isn't known or can grow overtime

## so in the case of the balanced
1. Transaction
    - trans id
    - date
    - name
    - description
    - amount
    - reocuring or not <-- another model: Reocurring, Not Reocurring (1:1 relationship, must have)
    - merchant name
    - category <-- another model: food, fun, bills, etc. (1:many relationship, optional)
    - etc.

2. Reoccurring Transaction
    - reoc id
    - next credit/debit date
    - prev credit/debit dates/transactions (1:many relationship, must have at least 1)
    - daily fixed amount
    - etc.