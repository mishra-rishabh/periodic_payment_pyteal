This smart contract is simply written to transfer salary1 to employee1 and salary2 to employee2
by the manager of the company. The transaction will take place every month for exactly one year.

This is a demonstration of Periodic Payment smart contract in Signature mode.

reference: https://pyteal.readthedocs.io/en/stable/examples.html

"decouple" library is used to access environment variables.

Transactions
1. manager => employee1
2. manager => employee2

Transaction 1 and Transaction 2 mentioned above should have the same sender

All the remaining money should go to the manager's address after closing the contract

Txn.lease() is used to safeguard replay attacks and duplicate payments
