from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687" , auth=("neo4j", "neo4jneo4j"))


# GLOBAL EDGE PROPERTIES:
{
    'relationship_type':['kith','kin'],
    'factuality':['stated','inferred'],
    'traversal_type':['direct','jump'],
}



# GENERATION_DOWN PROPERTIES
{
    'type':['parent_of','guardian_of','caregiver_of','godparent_of'],
    'subtype':['bio','half','adopted','guardian','other'],
}

# OPTIONS:
# GENERATION_UP
# child_of relationship_type: 
# GENERATION_DOWN
# type:  parent_of, guardian_of
# SAME_GENERATION
# type: sibling_of,  union_of,
# SHORTCUT

#SUBTYPES:
# - 
# Create a session

def generate_parent_child_relationship(mom,dad,child, subtype='bio'):
    #super dirty assumptions etc just to get ball rolling
    return [
        (dad,child,'GENERATION_DOWN',{'type':'parent_of','subtype':subtype,'factuality':'stated'}),
        (mom,child,'GENERATION_DOWN',{'type':'parent_of','subtype':subtype,'factuality':'stated'}),
        (child,mom,'GENERATION_UP',{'type':'child_of','subtype':subtype,'factuality':'stated'}),
        (child,dad,'GENERATION_UP',{'type':'child_of','subtype':subtype,'factuality':'stated'})]

def create_edge(p1,p2,rel_type,attributes):
    _attrs = ", ".join([f'r.{k}="{v}"' for k,v in attributes.items()])
    return f"""
    MATCH (p1:Person {{name:"{p1}"}})
    MATCH (p2:Person {{name:"{p2}"}})
    CREATE (p1)-[r:{rel_type}]->(p2)
    SET {_attrs}"""

people = [
        ('erin','f'),
        ('chandler','f'),
        ('ted','m'),
        ('fred','m'),
        ('debbie','f'),
        ('heidi','f'),
        ('worf','m'),
        ('gus','m'),
        ('esther','f'),
        ('maggie','f'),
        ('robert','m'),
        ('alexis','f'),
        ('erik','m'),
        ('chris','m'),
        ('lisa','f'),
        ('hilary','f'),
        ('billy','m'),
        ('john','m'),
        ('alyssa','f'),
        ('vinny','m'),
        ('amanda','f'),
        ('roger','m'),
        ('mary','f'),
        ('ed','m'),
        ('monica','f'),
        ('kurt','m'),
        ('corey','m'),
        ('meadow','f'),
        ('geoff','m'),
        ('beth','f'),
        ('anne','m'),
        ('lydia','f'),
        ('norma','f'),
        ('emily','f'),
        ('nancy','f'),
        ('shirley','f'),
        ('larry','m'),
        ('dave','m'),
        ('chucky','m'),
        ('timmy','m'),
        ('gigi','f'),
        ('nadia','f'),
        ('alice','f'),
        ('norman','m'),
        ('steven','m'),
        ]

relationships = [
        ('erin','chandler','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('maggie','robert','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('lisa','billy','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('chris','hilary','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('gus','esther','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('heidi','worf','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('worf','debbie','SAME_GENERATION',{'type':'union','status':'divorced','factuality':'stated'}),
        *generate_parent_child_relationship('heidi','worf','chandler'),
        *generate_parent_child_relationship('heidi','worf','maggie'),
        *generate_parent_child_relationship('robert','maggie','erik'),
        *generate_parent_child_relationship('robert','maggie','alexis'),
        *generate_parent_child_relationship('chandler','erin','ted','adopted'),
        *generate_parent_child_relationship('chandler','erin','fred','adopted'),
        *generate_parent_child_relationship('gus','esther','heidi'),
        *generate_parent_child_relationship('gus','esther','chris'),
        *generate_parent_child_relationship('gus','esther','lisa'),
        *generate_parent_child_relationship('gus','esther','john'),
        ('alyssa','vinny','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('ed','mary','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('monica','kurt','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('monica','steven','SAME_GENERATION',{'type':'union','status':'divorce','factuality':'stated'}),
        ('geoff','beth','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('alice','norman','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('norma','dave','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('emily','larry','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        ('chucky','shirley','SAME_GENERATION',{'type':'union','status':'active','factuality':'stated'}),
        *generate_parent_child_relationship('alyssa','vinny','erin'),
        *generate_parent_child_relationship('alyssa','vinny','amanda'),
        *generate_parent_child_relationship('alyssa','vinny','roger'),
        *generate_parent_child_relationship('ed','mary','monica'),
        *generate_parent_child_relationship('ed','mary','geoff'),
        *generate_parent_child_relationship('ed','mary','alyssa'),
        *generate_parent_child_relationship('monica','kurt','corey'),
        *generate_parent_child_relationship('monica','steven','meadow'),
        *generate_parent_child_relationship('geoff','beth','anne'),
        *generate_parent_child_relationship('geoff','beth','lydia'),
        *generate_parent_child_relationship('alice','norman','vinny'),
        *generate_parent_child_relationship('alice','norman','norma'),
        *generate_parent_child_relationship('alice','norman','emily'),
        *generate_parent_child_relationship('alice','norman','nancy'),
        *generate_parent_child_relationship('alice','norman','shirley'),
        *generate_parent_child_relationship('norma','dave','timmy'),
        *generate_parent_child_relationship('shirley','chucky','gigi'),
        *generate_parent_child_relationship('shirley','chucky','nadia'),
        ]


template = "CREATE ({name}:Person {{name: '{name}', gender: '{gender}'}})"
cypher_makes = [template.format(name=x,gender=y) for (x,y) in people]

cypher_matches = [create_edge(*x) for x in relationships]


delete_all = True
if delete_all:
    query = "match (n) detach delete n"
    with driver.session() as session:
        session.run(query)
    

if True:
    with  driver.session() as session:
        for query in cypher_makes:
            print(query)
            session.run(query)
        for query in cypher_matches:
            print(query)
            session.run(query)



# Close the driver
driver.close()


