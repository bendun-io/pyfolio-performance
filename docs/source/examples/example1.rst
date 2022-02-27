First Example: Loading the portfolio
====================================

In this example we load the portfolio and display some content.


.. code-block:: python

    from pyfolio-performance import Portfolio

    portfolio = Portfolio("portfolio.xml")

    print(portfolio.getAccounts())
    print(portfolio.getDepots())


The result will look like:

.. code-block:: console

    [Account/Comdirect Cash: 2500, Account/Norisbank: 30100, Account/P2P Bondora: 80000]
    [Depot/Comdirect, Depot/Consorsbank]

The string method for the accounts and the depots returns the `type` followed by a `/` and then the `name` 
of the object as it appears in portfolio performance.

The account representation also includes the value of the account in cents.

