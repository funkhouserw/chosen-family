from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687" , auth=("neo4j", "neo4jneo4j"))


"""
MATCH (p1:Person {name: 'katie'})-[:GENERATION_UP|GENERATION_DOWN|SAME_GENERATION*1..3]->(p2:Person)
RETURN p1,p2


MATCH (p1:Person {name: 'katie'})-[:SAME_GENERATION*1..4{status:"active"}]->(p2:Person)
RETURN p1,p2


"""

def create_edge(p1,p2,rel_type,attributes):
    _attrs = ", ".join([f'r.{k}="{v}"' for k,v in attributes.items()])
    return f"""
    MATCH (p1:Person {{name:"{p1}"}})
    MATCH (p2:Person {{name:"{p2}"}})
    CREATE (p1)-[r:{rel_type}]->(p2)
    SET {_attrs}"""



def infer_half_siblings():
    # THIS IS A QUERY TO FETCH ALL PAIRS OF BIO-CHILDREN.  lots of duplication though.
    my_query="""
    match (c1:Person)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1:Person)-[:SAME_GENERATION{type:'union',status:'active'}]->(p2:Person)-[:GENERATION_DOWN{type:'parent_of',subtype:'bio'}]->(c2:Person)
    WHERE NOT (c1)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p2)
    AND (c2)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1)
    AND c1 <> c2
    return c1,c2
    """
    results = driver.execute_query(my_query)
    result_pairs = results[0]
    name_pairs = []
    for a,b in result_pairs:
        if a._properties['name'] != b._properties['name']:
            name_pairs.append(( a._properties['name'],b._properties['name']))

    name_pairs = list(set(name_pairs))

    queries = [create_edge(a,b,'SAME_GENERATION',{'type':'sibling','subtype':'half','factuality':'inferred'}) for (a,b) in name_pairs]

    with  driver.session() as session:
        for query in queries:
            print(query)
            session.run(query)


def infer_step_siblings():
    # THIS IS A QUERY TO FETCH ALL PAIRS OF BIO-CHILDREN.  lots of duplication though.
    my_query="""
    match (c1:Person)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1:Person)-[:SAME_GENERATION{type:'union',status:'active'}]->(p2:Person)-[:GENERATION_DOWN{type:'parent_of',subtype:'bio'}]->(c2:Person)
    WHERE NOT (c1)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p2)
    AND NOT (c2)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1)
    AND c1 <> c2
    return c1,c2
    """
    results = driver.execute_query(my_query)
    result_pairs = results[0]
    name_pairs = []
    for a,b in result_pairs:
        if a._properties['name'] != b._properties['name']:
            name_pairs.append(( a._properties['name'],b._properties['name']))

    name_pairs = list(set(name_pairs))

    queries = [create_edge(a,b,'SAME_GENERATION',{'type':'sibling','subtype':'step','factuality':'inferred'}) for (a,b) in name_pairs]

    with  driver.session() as session:
        for query in queries:
            print(query)
            session.run(query)


def infer_bio_siblings():
    # THIS IS A QUERY TO FETCH ALL PAIRS OF BIO-CHILDREN.  lots of duplication though.
    my_query="""
    match (c1:Person)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1:Person)-[:SAME_GENERATION{type:'union',status:'active'}]->(p2:Person)-[:GENERATION_DOWN{type:'parent_of',subtype:'bio'}]->(c2:Person)
    WHERE (c1)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p2)
    AND (c2)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1)
    AND c1 <> c2
    return c1,c2
    """
    results = driver.execute_query(my_query)
    result_pairs = results[0]
    name_pairs = []
    for a,b in result_pairs:
        if a._properties['name'] != b._properties['name']:
            name_pairs.append(( a._properties['name'],b._properties['name']))

    name_pairs = list(set(name_pairs))

    queries = [create_edge(a,b,'SAME_GENERATION',{'type':'sibling','subtype':'bio','factuality':'inferred'}) for (a,b) in name_pairs]

    with  driver.session() as session:
        for query in queries:
            print(query)
            session.run(query)


def infer_step_parents():
    # THIS IS A QUERY TO FETCH ALL PAIRS OF BIO-CHILDREN.  lots of duplication though.
    my_query="""
    match (c1:Person)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p1:Person)-[:SAME_GENERATION{type:'union',status:'active'}]->(p2:Person)
    WHERE NOT (c1)-[:GENERATION_UP{type:'child_of',subtype:'bio'}]->(p2)
    return c1,p2
    """
    results = driver.execute_query(my_query)
    result_pairs = results[0]
    name_pairs = []
    for c,p in result_pairs:
        if c._properties['name'] != p._properties['name']:
            name_pairs.append(( c._properties['name'],p._properties['name']))

    name_pairs = list(set(name_pairs))
    queries = [create_edge(c,p,'GENERATION_UP',{'type':'child_of','subtype':'step','factuality':'inferred'}) for (c,p) in name_pairs]
    queries.append(*[create_edge(p,c,"GENERATION_DOWN",{'type':'parent_of','subtype':'step','factuality':'inferred'}) for (c,p) in name_pairs])

    with  driver.session() as session:
        for query in queries:
            print(query)
            session.run(query)


if True:
    infer_bio_siblings()
    infer_half_siblings()
    infer_step_siblings()
    infer_step_parents()
