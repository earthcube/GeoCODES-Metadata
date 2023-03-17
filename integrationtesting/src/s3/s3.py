def getFileFroms3(s3client, s3ObjectInfo):
    resp = s3client.get_object(s3ObjectInfo.bucket_name, s3ObjectInfo.object_name)
    return resp.data

'''Cleans the name of slashes... might need more in the future.'''
def gets3ObjectNameClean(s3ObjectName):
    return s3ObjectName.replace('/','_')