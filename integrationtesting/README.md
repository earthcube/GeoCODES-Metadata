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
the result is ok mv the file to .approved.txt


## Running
### Environment variables can be used to run in locally or in CI env

```
 GC_SITEMAP_URL
GC_GLCON
GC_NABUFILE
GC_GLNRFILE
GC_GRAPH
GC_REPO
```

```python
   def setUpClass(cls):
        cls.glcon = "/Users/valentin/development/dev_earthcube/gleanerio/gleaner/glcon_darwin"
        cls.nabuFile = "../resources/configs/geocodesintegration/nabu"
        graphendpoint, nabucfg = getNabu(cls.nabuFile)
        cls.glnFile = "../resources/configs/geocodesintegration/gleaner"
        s3endpoint, bucket, glncfg = getGleaner(cls.glnFile)
        cls.s3 = minio.Minio(s3endpoint)
        cls.glncfg = glncfg

        cls.bucket = bucket
        cls.repo = "geocodes_demo_datasets"
        cls.nabucfg = nabucfg
        ep = mg.graphFromEndpoint(graphendpoint)
        cls.graphendpoint = ep
        cls.graph = mg(ep, "citesting")

``` 


## From pycharm 
select metadata_approval_tests.py
run

This will run approval tests and put results of 'failed' tests with a name of
received.
If tests match the approved.txt, then no 'received.txt' files will be generated.
