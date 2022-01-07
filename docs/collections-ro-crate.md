
# Collections

A collection is intended to be a way to pass information to services

We are proposing to use [Research Object Crates](https://www.researchobject.org/ro-crate/1.1/data-entities.html#web-based-data-entities)

## Thought model:
* collection
  * queries
    * stored query that may be used
  * datsets
    * (link to query used to retrieve dataset?)
  * tools
    * dataset to input linkage, aak what url are we using in a dataset

## Scenario:
* search first (this is out present path)
  * user queries, saves query, saves data from query, 
  * user creates collection, adds query
  * user adds datasets to collection

* tool/task first (from science perspective, this is the ideal path)
   * user searches for a tool to accomplish a task
   * creates a collection, saves tool to collection
   * for each input, a query is run to find datasets
   * datasets saved to a tool input
  
## Examples:
* [rocrate-placeholder.json](../metadata/rocrate/rocrate-placeholder.json) is just a  file from the researchobject.org website



