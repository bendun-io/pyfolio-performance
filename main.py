from pyfolio_performance import Portfolio, Security

if __name__ == "__main__":
    portPerf = Portfolio("02_portfolio.xml")
    
    testSecurity = Security.getSecurityByName("BP")

    print(portPerf.getShares(testSecurity)) # should be around 122

    # Testing the methods
    print(Security.getSecurityByIsin("US88579Y1010").name)
    print(Security.getSecurityByWkn("878841").name)