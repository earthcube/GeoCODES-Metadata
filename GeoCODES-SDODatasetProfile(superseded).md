# ECO GeoCODES Profile

Doug Fils 2020-03-05
Stephen Ricahrd 2022-07-04

Note-- this document is superseded by google doc at https://docs.google.com/document/d/1z5Jo4STSBZ-zr8mmJA4G3hikm0IHBTIgTTPcbjQHbYs 

This document provides guidance for implementing Schema.org JSON-LD metadata to document geoscience datsets that will be most compatible with the [EarthCube GeoCODES resource registry](https://geocodes.earthcube.org/). This metadata profile is based on other schema.org recommendations:

 - [Google Developers Guidance](https://developers.google.com/search/docs/advanced/structured-data/dataset) helps guide use in Google Dataset Search
 - ESIP Science on Schema guides use of [Type Dataset](https://schema.org/Dataset) 
 
A JSON (v7) schema that specifies the JSON serialization that will work with the GeoCODES data entry forms 

# Metadata Profile for GeoCodes:
The following are either important in the search UI or items GeoCODES is using for value-added functionality (e.g. dataset-tool linkage).   It is important to know that these are items used by the search application.  This profile is based on the [ESIP Science on Schema.org guidance](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md), with some additional restrictions and recomendations.   

## @id
The top level @id property provides an identifier for the metadata record itself (not the resource that the metadata describes). Ideally this is a url that will resolve to return the JSON-LD metadata.

### Descriptive text
The initial search is focused mostly on text searches across the literal strings of the graph, then we conduct other graph connections as the query is processed into a set of results.   So, while it's important to publish the graph elements it is also important to provide descriptive text and keywords at every level of the JSON-LD graph.

### Distribution url
Follow ESIP Science on Schema [guidance here](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#distributions).

### Encoding format
Follow ESIP Science on Schema [guidance here](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#distributions)

### Variable measured 
This is a developing area and we will implement ESIP Science on Schema recommendations here.  See [discussion, evolving proposal](https://github.com/ESIPFed/science-on-schema.org/tree/issue27-measuredVariable/guides) and [examples](https://github.com/ESIPFed/science-on-schema.org/tree/issue27-measuredVariable/examples/dataset) in the variable measured branch at github/ESIPFed/science-on-schema.org

### Spatial
Many ways to do it, but GeoCODES may propose geosparql WKT approach
