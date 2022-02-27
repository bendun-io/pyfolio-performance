from pyfolio_performance import Portfolio, Filters
from datetime import datetime
portfolio = Portfolio("portfolio.xml")
currentNow = datetime.now()

def filter_month(entry, month, year):
    if year != entry.getYear() or month != entry.getMonth():
        return False
    return True

filter_dividend = Filters.fAnd(Filters.fEnsureTypeList(['DIVIDENDS']),
    lambda entry: filter_month(entry, currentNow.month, currentNow.year) )

# different clustering
def cluster_dividend(allCluster, entry):
    return "val"
    
def aggregate_dividend(cluster, entry):
    return cluster + entry.getValue()

divicluster = {'val': 0}
portfolio.evaluateCluster(divicluster, filter_dividend, cluster_dividend, aggregate_dividend)
print(divicluster)

# Dividends are clustered by their name
def cluster_dividend2(allCluster, entry):
    k = entry.getSourceName()
    if k not in allCluster:
        allCluster[k] = 0
    return k
divicluster = {}
portfolio.evaluateCluster(divicluster, filter_dividend, cluster_dividend2, aggregate_dividend)
print(divicluster)