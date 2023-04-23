from pyfolio_performance import Portfolio, Security

if __name__ == "__main__":
    portPerf = Portfolio("02_portfolio.xml")
    
    testSecurity = Security.getSecurityByName("BP")

    print(portPerf.getShares(testSecurity)) # should be around 122

    # Testing the methods
    print(Security.getSecurityByIsin("DE0005190003").getMostRecentValue())
    print(Security.getSecurityByWkn("878841").name)

    print(portPerf.getAccounts())
    print(portPerf.getDepots())

    for sec in portPerf.getSecurities():
        print(sec.getName())
        print(sec.getMostRecentValue())