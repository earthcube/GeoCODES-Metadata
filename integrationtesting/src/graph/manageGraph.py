import requests
import logging

class ManageGraph:
    baseurl = "http://localhost:3030" # basically fuskei
    namespace = "temp_summary"
    path = "namespace"
    sparql = "/sparql" # blazegraph uses sparql after namespace, but let's not assume this

    def __init__(self, graphurl, namespace):
        self.baseurl = graphurl
        self.namespace = namespace

    def createNamespace(self, quads=True):
        pass

    def deleteNamespace(self):
        pass
    def graphFromEndpoint(endpoint):
        pass
    def graphEndpointWithNamespace(self):
        return  f"{self.baseurl}/namespace/{self.namespace}{self.sparql}"

class ManageBlazegraph(ManageGraph):

    createTemplateQuad ="""com.bigdata.namespace.fffff.spo.com.bigdata.btree.BTree.branchingFactor=1024
com.bigdata.rdf.store.AbstractTripleStore.textIndex=true
com.bigdata.namespace.fffff.lex.com.bigdata.btree.BTree.branchingFactor=400
com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
com.bigdata.rdf.sail.isolatableIndices=false
com.bigdata.rdf.sail.truthMaintenance=false
com.bigdata.rdf.store.AbstractTripleStore.justify=false
com.bigdata.rdf.store.AbstractTripleStore.quads=true
com.bigdata.journal.Journal.groupCommit=false
com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false
com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
"""

    createTemplateTriples = """com.bigdata.namespace.fffff.spo.com.bigdata.btree.BTree.branchingFactor=1024
com.bigdata.rdf.store.AbstractTripleStore.textIndex=true
com.bigdata.namespace.fffff.lex.com.bigdata.btree.BTree.branchingFactor=400
com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
com.bigdata.rdf.sail.isolatableIndices=false
com.bigdata.rdf.sail.truthMaintenance=false
com.bigdata.rdf.store.AbstractTripleStore.justify=false
com.bigdata.rdf.sail.namespace=fffff
com.bigdata.rdf.store.AbstractTripleStore.quads=false
com.bigdata.journal.Journal.groupCommit=false
com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false
com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
"""
    def graphFromEndpoint(endpoint):
        paths = endpoint.split('/')
        paths = paths[0:len(paths) -3]
        newurl = '/'.join(paths)
        return newurl

    def createNamespace(self, quads=True):
        # POST / bigdata / namespace
        # ...
        # Content - Type
        # ...
        # BODY
       # add this to the createTemplates
        # # com.bigdata.rdf.sail.namespace = {namespace}
        if quads:
            template = self.createTemplateQuad
        else:
            template = self.createTemplateTriples
        template = template + f"com.bigdata.rdf.sail.namespace = {self.namespace}\n"
        url = f"{self.baseurl}/namespace"
        headers = {"Content-Type": "text/plain"}
        r = requests.post(url,data=template, headers=headers)
        if r.status_code==201:
            return "Created"
        elif  r.status_code==409:
            return "Exists"
        else:
            raise Exception("Create Failed.")


    def deleteNamespace(self):
        # DELETE /bigdata/namespace/NAMESPACE
        url = self.graphEndpointWithNamespace()
        headers = {"Content-Type": "text/plain"}
        r = requests.delete(url, headers=headers)
        if r.status_code == 200:
            return "Deleted"
        else:
            raise Exception("Delete Failed.")

    def insert(self, data, content_type="text/x-nquads"):
        # rdf datatypes: https://github.com/blazegraph/database/wiki/REST_API#rdf-data
        # insert: https://github.com/blazegraph/database/wiki/REST_API#insert
        url = self.graphEndpointWithNamespace()
        headers = {"Content-Type": f"{content_type}"}
        r = requests.post(url,data=data, headers=headers)
        if r.status_code == 200:
            # '<?xml version="1.0"?><data modified="0" milliseconds="7"/>'
            if 'data modified="0"'  in r.text:
                raise Exception("No Data Added: " + r.text)
            return True
        else:
            return False

    def query(self,query):
        url = self.graphEndpointWithNamespace()
        headers = {"Accept": "application/sparql-results+json"}
        payload= {"query": query}
        r = requests.get(url, params=payload, headers=headers)
        if r.status_code == 200:
            # '<?xml version="1.0"?><data modified="0" milliseconds="7"/>'
            if 'data modified="0"' in r.text:
                raise Exception("No Data Added: " + r.text)
            return r.json()
        else:
            raise Exception(f"query failed. {r.text}")

    def ping(self):
        try:
            test = self.query("SELECT * { ?s ?p ?o } LIMIT 1")
            if len(test.results) == 1:
                return True
            else:
                return False
        except Exception:
            raise Exception(f"failed to connect to graph endpoint. {Exception}")