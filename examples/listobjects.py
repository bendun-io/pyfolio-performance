from pyfolio_performance import Portfolio

portPerf = Portfolio("02_portfolio.xml")

print()
print("Accounts: #" + str(len(portPerf.getAccounts())))
for account in portPerf.getAccounts():
    print(account.getName() + ": " + str(account.getBalance()))
print()

num = 0
print("Transactions of #1 Account:")
acc = portPerf.getAccounts()[0]
for transaction in acc.getTransactions():
    print("[" + str(transaction.date) + "] " + transaction.type + ": " + str(transaction.getAmount()))
    num += 1
    if num >= 5:
        break
print()

print("Depots: #" + str(len(portPerf.getDepots())))
for depot in portPerf.getDepots():
    print(depot.getName())
print()

num = 0
print("Transactions of #1 Depot:")
acc = portPerf.getDepots()[0]
for transaction in acc.getTransactions():
    print("[" + str(transaction.date) + "] " + transaction.type + ": " + str(transaction.getAmount()))
    print("\t" + str(transaction.getSecurity()))
    num += 1
    if num >= 5:
        break
print()


print("New purchases in ")
# def filter_month(entry, month, year):
#     if entry.getYear() != year or month != entry.getMonth():
#         return False
#     return True
print()

# print("Securities:")
# print({x.getName(): x.getLogo()==None for x in portPerf.getSecurities()})
# print()