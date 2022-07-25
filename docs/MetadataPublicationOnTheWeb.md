# Considerations for publishing metadata for web harvesting.

## On the server side:
The following are items of use to the GeoCODES harvest and indexing process.  

### Sitemap or Sitemap index
You can leverage a sitemap (up to 50K resources) or a sitemap index to go beyond that.  An index will point to multiple sitemaps.  Note, you can use the index pattern to point to different resource types too.  For example, a sitemap index can point to various sitemaps for tools/software, people, dataset, etc.  This is also completely compatible with Google and other commercial site index systems.  

### Leverage Sitemap with dates
Adding the dates node and updating it will be useful as we move to an automated indexing pattern with GeoCODES.   If present we will use this to guide the architecture to do faster and less burdensome indexing.   Sites that do not provide this date node will need to be periodically completely indexed to ensure updates to metadata records are found and indexed.  

### Content negotiate
Though note required, we do support content negotiation for accessing your resources.  This can be both faster and less stressful on servers.  You do not need to provide any guidance back to EarthCube if you implement this.

### Headless vs static
Both static and dynamic inclusion of the JSON-LD data graph into the page DOM is supported.  EarthCube (and all commercial indexes) support this "headless" rendering of pages for indexing.   At present we do not have a good standards based way to communicate this to EarthCube.  We are addressing approaches, both in the indexing code and via the web architecture to do this.   We will provide further guidance, if necessary, as it develops on this point.   Providers should feel free to select either approach as it addresses their own criteria.  
