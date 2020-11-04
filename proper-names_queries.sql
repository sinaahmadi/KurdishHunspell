PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX v: <http://www.wikidata.org/prop/statement/>
SELECT DISTINCT ?name WHERE {
  ?p wdt:P31/wdt:P279 wd:Q6256 .
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "ckb" .
        ?p rdfs:label ?name .
  }
}


SELECT ?item ?itemLabel ?article
{
  ?item wdt:P31 wd:Q5 . # Q6256: country, Q5: human, Q515: city
  ?article schema:about ?item .
  ?article schema:isPartOf <https://ckb.wikipedia.org/> .
  #  ?article wikibase:badge wd:Q17437796 . # ?article is a featured article
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ckb" . }
   FILTER(EXISTS {
   ?item rdfs:label ?lang_label.
   FILTER(LANG(?lang_label) = "ckb")
 })
} 