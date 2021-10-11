from NLI import NL4DV
import os

nl4dv_instance = NL4DV(data_url = os.path.join("..", "..", "dataset", "movies.csv"))

dependency_parser_config = {"name": "corenlp", "model": os.path.join("..", "..","jars","stanford-english-corenlp-2018-10-05-models.jar"),"parser": os.path.join("..", "..","jars","stanford-parser.jar")}# using Stanford Core NLP
# dependency_parser_config = {"name": "corenlp-server", "url": "http://localhost:9000"}# using Stanford CoreNLPServer
# dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}# using Spacy

nl4dv_instance.set_dependency_parser(config=dependency_parser_config)
query = "compare title in different rating?"
output = nl4dv_instance.analyze_query(query)
print(output)