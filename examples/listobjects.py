from pyfolio_performance import Portfolio

portPerf = Portfolio("02_portfolio.xml")

print()
print("Accounts: #" + str(len(portPerf.getAccounts())))
for account in portPerf.getAccounts():
    print(account.getName() + ": " + str(account.getBalance()))
print()

print("Depots: #" + str(len(portPerf.getDepots())))
for depot in portPerf.getDepots():
    print(depot.getName())
print()

# print("Securities:")
# print({x.getName(): x.getLogo()==None for x in portPerf.getSecurities()})
# print()