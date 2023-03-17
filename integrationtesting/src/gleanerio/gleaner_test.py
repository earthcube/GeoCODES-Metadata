import os
import unittest
import logging

from gleanerio import gleaner

class MyTestCase(unittest.TestCase):
    def test_endpointUpdate(self):
        endpoint = gleaner.endpointUpdateNamespace("https://example.com/blazegraph/namespace/earhtcube/sparql")
        self.assertEqual( "https://example.com/blazegraph/namespace/temp/sparql",endpoint)  # add assertion here
        endpoint =gleaner.endpointUpdateNamespace("https://example.com/blazegraph/namespace/earhtcube/sparql", namepsace="temp_summary")
        self.assertEqual("https://example.com/blazegraph/namespace/temp_summary/sparql", endpoint)

    def test_nabuCfg(self):
        with open('../resources/testing/nabu', 'r') as f:
            endpoint, cfg = gleaner.getNabu(f)
        self.assertEqual("https://graph.geodex.org/blazegraph/namespace/earthcube/sparql", endpoint)

    def test_reviseNabuCfg(self):
        with open('../resources/testing/nabu', 'r') as f:
            endpoint, cfg = gleaner.getNabu(f)
            endpoint = gleaner.endpointUpdateNamespace(
                "https://example.com/blazegraph/namespace/earhtcube/sparql")
            cfgnew = gleaner.reviseNabuConf(cfg, endpoint)

        self.assertEqual("https://example.com/blazegraph/namespace/temp/sparql", cfgnew['sparql']['endpoint'])

    def test_runIdentifier(self):
         #with open('../../resources/testing/gleaner', 'r') as f:
         path =  os.getcwd()
         logging.info("executatble path", path)
         f= '../../resources/configs/geocodetest/gleaner'
         s3endpoint, bucket, cfg = gleaner.getGleaner(f)
         json = '''{
"@context": 
    { "@vocab":"http://schema.org/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dct": "http://purl.org/dc/terms/",
    "ecrro": "http://cor.esipfed.org/ont/earthcube/",
    "ecrr": "https://n2t.net/ark:/23942/g2"
    } ,
"@type": ["Dataset"],
"@id": "metadata:doi:10.7288/V4/MAGIC/14104",

"name": "Paleomagnetism of Paleozoic asphaltic deposits in southern Oklahoma, USA (DataSet).",
"description": "<p>Paleomagnetic measurements on asphaltic samples from two formations in southern Oklahoma have been performed. A bioclastic unit from the Bog...e, possibly authigenic magnetite, like that show...tion during minor uplift in the Early Permian of the Arbuckle Mounta...cing bacteria. © American Geophysical Union 1988</p>"
}
'''
         # yeah, I know the fixed path is bad... but
         result = gleaner.runIdentifier( json,glncfg=f, glcon="/Users/valentin/development/dev_earthcube/gleanerio/gleaner/cmd/glcon/glcon_darwin")
         self.assertIsNotNone(result)
         result = result.decode("utf-8")
         self.assertFalse("ERROR"  in result )

if __name__ == '__main__':
    unittest.main()
