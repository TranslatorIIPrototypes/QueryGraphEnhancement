import os
from neo4j import GraphDatabase

"""
We want to build a list of good expansions of edges.
Specifically, given a query (A)-[x]-(B) where A and B are semantic types and x is a specific predicate,
we want to find expanded queries of the form (A)-[p]-(C)-[q]-(B) with which [x] may be replaced.

To do this we are going to
1) Get the counts of every (A)-[x]-(B) query.
2) For each (A,x,B), get counts of (A)-[x]-(B)-[q]-(C)-[p]-(A), as well as (A)-[p]-(C)-[q]-(B).
2a) the latter query should be cached and reused.
3) Calculate sensitivity/specificity [for each direction], as well as overall correlation.
"""

class ExpansionManagement:
    def __init__(self,db_url,neo4j_password):
        self._driver = self.driver(db_url,neo4j_password)

    def driver(self,url,neo4j_password):
        auth=("neo4j", neo4j_password)
        return GraphDatabase.driver(url, auth=auth)

    def query(self,cypher):
        with self._driver.session() as session:
            results = session.run(cypher)
        return list(results)

    def update_one_hops(self):
        q= '''MATCH (a)-[x]->(b) 
                   WHERE NOT a:Concept and NOT b:Concept 
                   RETURN labels(a) AS lsa, type(x) AS typex, labels(b) AS lbs, COUNT(*) as c'''
        results = self.query(q)



