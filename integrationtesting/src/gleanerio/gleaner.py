import copy
import json
import os
import shutil
import subprocess

import yaml


def endpointUpdateNamespace( fullendpoint, namepsace='temp'):
    paths = fullendpoint.split('/')
    paths[len(paths)-2] = namepsace
    newurl= '/'.join(paths)
    return newurl

def getNabu( cfgfile):
    with open(cfgfile, "r") as stream:
        try:
            cfg =(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    endpoint = cfg['sparql']['endpoint']
    return endpoint, cfg

def reviseNabuConf(cfg, endpoint, bucket):
    newcfg = copy.deepcopy(cfg)
    newcfg['sparql']['endpoint'] = endpoint
    newcfg['s3']['bucket'] = bucket
    return newcfg

def runNabu(cfg, repo,glcon="~/indexing/glcon"):
    if shutil.which(glcon) is not None:
        filename = f"nabu_{repo}" # avoid possible naming conflicts
        with open(filename, 'w') as f:
            yaml.dump(cfg, f)
        executeNabu = f"{glcon} nabu prefix --cfg {filename} --prefix summoned/{repo}"
        fullpath = os.path.abspath(filename)
        try:
            result = subprocess.run([glcon, "nabu", "prefix",
                                     "--cfg", fullpath,
                                     "--prefix", f"summoned/{repo}",
                                     ],
                                    capture_output=True,
                                    )
            if result.returncode != 0:
                raise Exception(f"return code:{result.returncode} try from command line: '{glcon}  nabu prefix --cfg {filename} --prefix summoned/{repo}'  {result}")
        except Exception as ex:
            raise Exception(f"failed  try from command line:  '{glcon}  nabu prefix --cfg {filename} --prefix summoned/{repo}'  reason{ex}")
        # delete config file here
        return result.stdout
    else:
        raise Exception(f"glcon not found at {glcon}. Pass path to glcon with --glcon")



def getGleaner( cfgfile):
    with open(cfgfile, "r") as stream:
        try:
            cfg =(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    bucket = cfg['minio']['bucket']
    s3endpoint = cfg['minio']['address']
    return s3endpoint,  bucket, cfg

def reviseGleanerConf(cfg, bucket):
    newcfg = copy.deepcopy(cfg)
    newcfg['minio']['bucket'] = bucket
    return newcfg

def runGleaner(cfg, repo,glcon="~/indexing/glcon"):
    if shutil.which(glcon) is not None:
        filename = f"gleaner_{repo}" # avoid possible naming conflicts
        with open(filename, 'w') as f:
            yaml.dump(cfg, f)

        executeApp = f"{glcon} gleaner batch --cfg {filename} --source {repo}"
        fullpath = os.path.abspath(filename)
        try:
            result = subprocess.run([glcon, "gleaner", "batch",
                                     "--cfg", fullpath,
                                     "--source", repo,
                                     ],
                                    capture_output=True,
                                    )
            if result.returncode != 0:
                raise Exception(f"return code:{result.returncode} try from command line: '{glcon}  gleaner batch --cfg {filename} --source {repo}'  {result}")
        except Exception as ex:
            raise Exception(f"failed  try from command line:  '{glcon}  gleaner batch --cfg {filename} --source {repo}'  reason{ex}")
        # delete config file here
        return result.stdout
    else:
        raise Exception(f"glcon not found at {glcon}. Pass path to glcon with --glcon")

## this takes a string with the jsonld, and
def runIdentifier( jsonld_str,glncfg="../resources/configs/geocodedemo/gleaner", glcon="~/indexing/glcon"):
    isvalid, err = validateJSON(jsonld_str)
    if not isvalid:
         raise Exception( f"invalid json:  {err}" )
    if shutil.which(glcon) is not None:
    #     filename = f"./gleaner_id" # avoid possible naming conflicts
    #     with open(filename, 'w') as f:
    #         yaml.dump(cfg, f)
    #     executeApp = f"{glcon}  tools id --idtype identifiersha "
        try:
            result = subprocess.run([glcon,  "tools", "id",
                                     "--idtype", "identifiersha",
                                    "--cfg", glncfg
                                     ],
                                    capture_output=True,
                                     input=bytes(jsonld_str, 'utf-8')
                                    )
            if result.returncode != 0:
                raise Exception(f"return code:{result.returncode} try from command line: '{glcon} tools id --idtype identifiersha'  {result}")
        except Exception as ex:
            raise Exception(f"failed  try from command line:  '{glcon} tools id --idtype identifiersha'  reason{ex}")
        # delete config file here
        return result.stdout
    else:
        raise Exception(f"glcon not found at {glcon}. Pass path to glcon with --glcon")

## needs to be in utils
def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False, err
    return True, None