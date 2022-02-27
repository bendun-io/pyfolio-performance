Analysis: Dividend of the month
================================

In the following example we compute the dividends received this month in 2 different way.
The first one simply aggregates the dividend. The second examlpe aggregates it by security.

.. literalinclude:: example2.py

The code leads to the following two outputs. The first one simply gives the sum of all dividends.
The second one aggregates it by the security that distributes the dividend.

The value is returned in cents. There were 13,79 received through the securities `AT + T`, 
`Realty Income` and `Proctor and Gamble`. The displayed name and corresponding key used in the code
reflects the name given in portfolio performance's security section.

.. code-block:: console

    {'val': 1379}
    {'AT + T': 190, 'Realty Income': 781, 'Proctor and Gamble': 408}