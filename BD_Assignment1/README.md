# Assignment A (PART I)

### GOAL
For homework 2, we expect you to solve the problems using object oriented programming and also multiple modules to organize your code better.

You are given a CSV file with a set of mortgages that you are going to "package" into a passthrough security. The mortgage file contains one mortgage per line with principal, rate in percentage and term in years. Every month you will receive a cashflow that is equal to the sum of all the mortgages' cashflows in the "package".

You are also given a yield curve CSV file with 2 values: term in months and rate in percentage.

Write a script that does the following:

* Calculate the value of your "packaged" security
* Using finite differences, calculate Modified Duration, Convexity and DV01 of your 


### Files ###

* fall2016_9815_hw02.py: This is the main module of hw2
* yc.py: provides a ```YieldCurve``` class to represent the yield curve
* mortgage.py: provides a ```Mortgage``` class to store mortgage information
* portfolio.py: provides a ```Portfolio``` class to store all mortgages

### Running

Run the main module using following command:
```
> python fall2016_9815_hw02.py -y yc.csv -d mortgages.csv
```
