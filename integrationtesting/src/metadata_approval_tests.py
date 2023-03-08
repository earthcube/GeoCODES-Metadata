
'''
this is to use approvals tests as part of integration testing
of the geocodes stack. It will use the metadata in this repository
as part of a data loading workflow. Approvals will be used to
pull information from the 'service' endpoints (an s3 store, and a graph database)
and use a human to approve them initially.

logic:
intially only geocodes_demo_datasets
* read config files (from gleaner and nabu) plan is to merge these codebases in the future
* setup
** create test datastores for this testing
*** s3 - test bucket
*** graph -- test namespace,
** run gleaner and nabu
*** ./glcon gleaner batch --cfgName {} --source geocodes_demo_datasets
*** ./glcon nabu prefix --cfgName {} --prefix geocodes_demo_datasets/summon
* read sitemap and generate url list
* generate identifiers for each file.
* approval for identifiers
** approve that identifiers for each are generated.
* approval test for s3.
** approve counts. Note this will be less, because there is a duplicate ID
** did the data get to s3, and does it look good.
* approval test for graph
** did the data get to the graph store, and look good?
** approve counts.
* run nabu a second time
** ./glcon nabu prefix --cfgName {} --prefix geocodes_demo_datasets/summon
* Approval test to see that duplicates are not loaded
** approve counts
'''
import json
import os
import unittest
import urllib

import pandas
import requests
import sparqldataframe as sparqldataframe
import simplejson
from string import Template
from parameterized import parameterized
from approvaltests.approvals import verify
from approval_utilities.utilities.exceptions.exception_collector import gather_all_exceptions_and_throw
from approvaltests.namer import NamerFactory
from s3.s3 import getFileFroms3, gets3ObjectNameClean
from graph.manageGraph import ManageBlazegraph as mg
from sitemapparser import SiteMapParser
from sitemapparser.exporters import JSONExporter
import minio
import logging

from gleanerio.gleaner import runIdentifier, getGleaner,getNabu, runNabu,runGleaner



def load_test_cases():
   # tree = sitemap_tree_for_homepage(
    smu = 'https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml'
    if (os.getenv('GC_SITEMAP_URL')):
      smu = os.getenv('GC_SITEMAP_URL')
    sm =  SiteMapParser(smu)
    json_exporter = JSONExporter(sm)
    jsonurls = json.loads( json_exporter.export_urls() )
    urls = list(map( lambda a:  a['loc'], jsonurls ))
    urls.sort()
    return urls

def custom_name_func(testcase_func, param_num, param):
    return "%s_%s" %(
        testcase_func.__name__,
        parameterized.to_safe_name("_".join(str(x) for x in param.args)),
    )
def getFromUrl(url):
    r = requests.get(url)
    if r.status_code == 200:
        # '<?xml version="1.0"?><data modified="0" milliseconds="7"/>'
        if 'data modified="0"' in r.text:
            raise Exception("No Data Added: " + r.text)
        return r.text
    else:
        raise Exception(f"query failed. {r.text}")
def getFilename(url):
    uri = urllib.parse.urlparse(url).path.split('/')
    name = uri[len(uri) - 1]
    return name


def getFileFromResources(filename):
    with open(f"../resources/{filename}", "r") as stream:
        try:
            return stream.read()
        except Exception as exc:
            print(exc)
def getAGraph(g,  g_template, endpoint):
    thsGraphQuery = g_template.substitute(g=g)
    g_df = sparqldataframe.query(endpoint, thsGraphQuery)

    #results = g_df.to_csv(index=False)
    # might dump results to files in the future.

    # the blind node id's change, the order of triples changes
    # the count should not change unless the code changes, so
    # that is what we return
    approval = f"triplecount: {len(g_df.index)}   graph: '{g}'  "
    return approval

class GeocodesItegrationTesting(unittest.TestCase):

    # run once, so use setupClass
    # read the parameters from the config files
    # setup the s3 and graph client objects

    @classmethod
    def setUpClass(cls):
        glcon = "/Users/valentin/development/dev_earthcube/gleanerio/gleaner/glcon_darwin"
        if (os.getenv('GC_GLCON')):
            glcon = os.getenv('GC_GLCON')
        cls.glcon = glcon

        nabuFile = "../resources/configs/geocodesintegration/nabu"
        if (os.getenv('GC_NABUFILE')):
            nabuFile = os.getenv('GC_NABUFILE')
        cls.nabuFile = nabuFile
        graphendpoint, nabucfg = getNabu(cls.nabuFile)

        glnFile = "../resources/configs/geocodesintegration/gleaner"
        if (os.getenv('GC_GLNRFILE')):
            glnFile = os.getenv('GC_GLNRFILE')
        cls.glnFile = glnFile
        s3endpoint, bucket, glncfg = getGleaner(cls.glnFile)

        cls.s3 = minio.Minio(s3endpoint)
        cls.glncfg = glncfg

        cls.bucket = bucket # from config file

        repo = "geocodes_demo_datasets"
        if (os.getenv('GC_REPO')):
            repo = os.getenv('GC_REPO')
        cls.repo = repo
        cls.nabucfg = nabucfg

        graphnamespace =  "citesting"
        if (os.getenv('GC_GRAPH')):
            graphnamespace = os.getenv('GC_GRAPH')

        ep = mg.graphFromEndpoint(graphendpoint)
        cls.graphendpoint = ep
        cls.graph = mg(ep,graphnamespace)

        # still an issue or two with gleaner.
       # runGleaner(glncfg, cls.repo,cls.glcon)
       # runNabu(nabucfg,cls.repo, cls.glcon)

    def test_sitemap_urls_same(self):
        verify(load_test_cases())

# note in pycharm you will not be able to run this as an individual test
    # https://youtrack.jetbrains.com/issue/PY-56529/PyCharm-interprets-.-as-when-specifying-parameters-for-pytest.mark.parametrize
    @parameterized.expand(load_test_cases, name=custom_name_func)
   # @unittest.skip("issue with location of the context assets.")
    def test_identifiers(self, url):

         verify(runIdentifier(getFromUrl(url), glncfg=self.glnFile, glcon=self.glcon),
         options=NamerFactory.with_parameters(getFilename(url))
         )


# did the file count change
    def test_s3_counts(self):
        objects = self.s3.list_objects(self.bucket, prefix=f"summoned/{self.repo}/")
        count = len(list(objects))
        verify(f"object count for {self.repo}: {count}")
        #verify("Hello ApprovalTests")

# did the filenames change
    def test_s3_jsonld_filelist(self):
        objects = self.s3.list_objects(self.bucket, prefix=f"summoned/{self.repo}/")
        filelist = list(map( lambda o: o.object_name, objects))
        filelist.sort()
        verify(filelist)

  # how do the files look, did they change

    def test_s3_jsonld(self):
        objects = self.s3.list_objects(self.bucket, prefix=f"summoned/{self.repo}/")
        gather_all_exceptions_and_throw(
            objects,
            lambda obj: verify(
                getFileFroms3(self.s3, obj),
                options=NamerFactory.with_parameters(gets3ObjectNameClean(obj.object_name)),
            ),
        )

#  foreach loaded file with
    # verify(
    #     f"is Leap {str(year)}: {str(is_leap_year(year))}",
    #     options=NamerFactory.with_parameters(year),
    # )
    def test_graph_dataset_counts(self):
        results = self.graph.query(getFileFromResources('sparql/count_datasets.txt'))
        verify(results['results']['bindings'])

    def test_graph_counts(self):
        results = self.graph.query(getFileFromResources('sparql/count_triples.txt'))
        verify(results['results']['bindings'])
        #verify("Hello ApprovalTests")

# this grabs all triples for a graph, and returns a count
    # this could be problematic if the order of the results changes.
    # if so, we might just keep a count of the triples
    # or find some quick way to do a row level diff, and implement in approval code.
   #  @unittest.skip("Works, but not sure if the content will work for approvals.")
    def test_graph_results(self):
        query = getFileFromResources('sparql/select_all_datasets.txt')
        singlegraphquery = getFileFromResources('sparql/triples_for_a_graph.txt')
        g_template = Template(singlegraphquery)
        df = sparqldataframe.query(self.graph.graphEndpointWithNamespace(), query)
        gs = pandas.array(df['g'])
        # for index, row in df.iterrows():
        #     thsGraphQuery = g_template.substitute(g=row["g"])
        #     g_df = sparqldataframe.query(self.graph.graphEndpointWithNamespace(), thsGraphQuery)
        #     results = g_df.to_csv(index = False)
        #     verify(results, options=NamerFactory.with_parameters(row["g"]) )
        gather_all_exceptions_and_throw(
            gs,
            lambda g: verify(
                #(g,  g_template, endpoint
                getAGraph(g,g_template, self.graph.graphEndpointWithNamespace()),
                options=NamerFactory.with_parameters(g),
            ),
        )
        #verify("Hello ApprovalTests")
    #query to get all graph {g}
    # for each graph g,
    # verify(
    #     f"is Leap {str(g)}: {str(is_leap_year(g))}",
    #     options=NamerFactory.with_parameters(g),
    # )

if __name__ == "__main__":

    logging.info("Env variables")
    envnames = """
    GC_SITEMAP_URL
    GC_GLCON
    GC_NABUFILE
    GC_GLNRFILE
    GC_GRAPH
    GC_REPO
    """
    logging.info("envnames")
    unittest.main()