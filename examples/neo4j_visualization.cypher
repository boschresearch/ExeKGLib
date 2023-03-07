//*********** Requirements ***********//
// Neo4j version: 4.4.*               //
// Plugins: APOC, Neosemantics (n10s) //
////////////////////////////////////////

// prepare DB for RDF data import
CALL n10s.graphconfig.init();

CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// add required namespaces
CALL n10s.nsprefixes.add("ds","https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#");
CALL n10s.nsprefixes.add("ml","https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl#");
CALL n10s.nsprefixes.add("stats","https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl#");
CALL n10s.nsprefixes.add("visu","https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl#");

// import RDF data (replace 1st arg with the path of the desired executable KG)
CALL n10s.rdf.import.fetch("https://raw.githubusercontent.com/boschresearch/ExeKGLib/main/examples/pipelines/StatsPipeline.ttl","Turtle");

// shorten URIs for more clear visualization
MATCH (n)-[r]-()
SET n.uri = apoc.text.replace(n.uri, "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ds_exeKGOntology.ttl#", "ds:");

MATCH (n)-[r]-()
SET n.uri = apoc.text.replace(n.uri, "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/ml_exeKGOntology.ttl#", "ml:");

MATCH (n)-[r]-()
SET n.uri = apoc.text.replace(n.uri, "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/stats_exeKGOntology.ttl#", "stats:");

MATCH (n)-[r]-()
SET n.uri = apoc.text.replace(n.uri, "https://raw.githubusercontent.com/nsai-uio/ExeKGOntology/main/visu_exeKGOntology.ttl#", "visu:");

MATCH (n)-[r]-()
SET n.uri = apoc.text.replace(n.uri, "http://www.w3.org/2001/XMLSchema#", "xsd:");

// improve readability of data entities
MATCH (n)-[r]-()
SET n.uri = apoc.text.replace(n.uri, ":Data(In|Out)", ":");



// fetch the executable KG
// !! run separately !!
MATCH (n)-[r]-()
WHERE type(r) <> 'rdf__type'
RETURN n, r;
