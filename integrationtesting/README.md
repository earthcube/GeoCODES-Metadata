# Integration Testing 
The goal of this is to see that the data is loaded

This intially takes an effort to approve results.

After this, if the code in gleaner changes, then it will take time to 
again, approve the results

## Approving Results.
in the integration directory, theere is an approved_files directory

Files with the extenstion, .approved.txt represent approved results.
When you run a set of tests, if there is a difference, then a 
result with .received. will appear.

Examine this file, diff the changes, if needed, and if you think 
the result is ok mv the file to .approved.


## Running
Right now, things are hard coded in the setup class

* glcon
* 
