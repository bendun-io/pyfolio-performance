# pyfolio-performance
A python library to read in your portfolio performance XML-file.


## Installation


pip install pyfolio-performance 


## Get started

This is a small example for loading a portfolio performance file and getting account information.

### Looking into Accounts


from pyfolio-performance import Portfolio

portfolio = Portfolio("portfolio.xml")
print(portfolio.getAccounts())


The result will look like:

[]



### Looking into Depots

You can also display the securities in a Depot.


from pyfolio-performance import Portfolio

portfolio = Portfolio("portfolio.xml")
print(portfolio.getDepots())


The result will look like:

[Depot/Comdirect, Depot/Consorsbank]
