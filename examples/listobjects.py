from pyfolio_performance import Portfolio

portPerf = Portfolio("02_portfolio.xml")

print()
print("Accounts: #" + str(len(portPerf.getAccounts())))
for account in portPerf.getAccounts():
    print(account.getName() + ": " + str(account.getBalance()))
print()

print("Transactions of #1 Account:")
acc = portPerf.getAccounts()[0]
for transaction in acc.getTransactions():
    print("[" + str(transaction.date) + "] " + transaction.type + ": " + str(transaction.getAmount()))
print()

print("Depots: #" + str(len(portPerf.getDepots())))
for depot in portPerf.getDepots():
    print(depot.getName())
print()

print("Transactions of #1 Depot:")
acc = portPerf.getDepots()[0]
for transaction in acc.getTransactions():
    print("[" + str(transaction.date) + "] " + transaction.type + ": " + str(transaction.getAmount()))
print()


# print("Securities:")
# print({x.getName(): x.getLogo()==None for x in portPerf.getSecurities()})
# print()