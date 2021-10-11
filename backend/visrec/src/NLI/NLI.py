# In-built Libraries
import os
import time
from collections import OrderedDict
import json

# Third-Party Libraries
import spacy
from nltk.stem.porter import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.corenlp import CoreNLPDependencyParser

# from vega import VegaLite

# NL4DV Imports
from NLI.datagenie import DataGenie
from NLI.querygenie import QueryGenie
from NLI.attributegenie import AttributeGenie
from NLI.taskgenie import DecideTask
import NLI.helpers as helpers
import NLI.constants as constants
from conceptnet.conceptnet_api import word2column


class NL4DV:
    """
    Class exposed to users to interact with the package. Exposes modules in the package via
    public methods

    """

    def __init__(self, data_url=None,
                 data_value=None,
                 alias_url=None,
                 alias_value=None,
                 label_attribute=None,
                 ignore_words=list(),
                 reserve_words=list(),
                 dependency_parser_config=None,
                 thresholds=None,
                 importance_scores=None,
                 attribute_datatype=None,
                 verbose=False,
                 language='en',
                 debug=False):

        # inputs
        self.data_url = data_url
        self.data_value = data_value
        self.alias_url = alias_url
        self.alias_value = alias_value
        self.label_attribute = label_attribute
        self.ignore_words = ignore_words
        self.reserve_words = reserve_words
        self.verbose = verbose
        self.debug = debug
        self.language=language
        if self.language=="en":
            self.dependency_parser_config = {"name": "corenlp", "model": os.path.join("..", "..","jars","stanford-english-corenlp-2018-10-05-models.jar"),"parser": os.path.join("..", "..","jars","stanford-parser.jar")}
        elif self.language=="cn":
            self.dependency_parser_config = {"name": "corenlp", "model": os.path.join("..", "..","jars","stanford-corenlp-4.2.0-models-chinese"),"parser": os.path.join("..", "..","jars","stanford-parser.jar")}
        

        # Load constants: thresholds, mappings, scores
        self.vis_keyword_map = constants.vis_keyword_map
        self.task_keyword_map = constants.task_keyword_map
        self.match_scores = constants.match_scores
        self.match_thresholds = constants.match_thresholds
        if self.language=="cn":
            self.match_thresholds['string_similarity']=80

        # Initialize intermediate/output variables
        self.execution_durations = dict()
        self.query_raw = None
        self.query_processed = ""
        self.query_for_task_inference = ""
        self.query_tokens = list()
        self.query_ngrams = dict()
        self.extracted_vis_type = None
        self.extracted_vis_token = None
        self.extracted_tasks = OrderedDict()
        self.extracted_attributes = OrderedDict()
        self.vis_list = None
        self.dependencies = list()
        self.dependency_parser = None
        self.dependency_parser_instance = None

        # Others
        self.dialog = False

        # initialize porter stemmer instance
        self.porter_stemmer_instance = PorterStemmer()

        # Initialize internal Class Instances
        self.data_genie_instance = DataGenie(self)  # initialize a DataGenie instance.
        self.query_genie_instance = QueryGenie(self)  # initialize a QueryGenie instance.
        self.attribute_genie_instance = AttributeGenie(self)   # initialize a AttributeGenie instance.
        # self.task_genie_instance = TaskGenie(self)  # initialize a TaskGenie instance.
        # self.vis_genie_instance = VisGenie(self)   # initialize a VisGenie instance.

        # Set the dependency parser if config is not None
        if self.dependency_parser_config is not None:
            self.set_dependency_parser(dependency_parser_config)
        # Set the thresholds, e.g., string matching
        if thresholds is not None:
            self.set_thresholds(thresholds=thresholds)
        # Set the importance scores, i.e., weights assigned to different ways in which attributes, tasks, and vis are detected/inferred.
        if importance_scores is not None:
            self.set_importance_scores(scores=importance_scores)
        # Override the attribute datatypes
        if attribute_datatype is not None:
            self.set_attribute_datatype(attr_type_obj=attribute_datatype)

    # ToDo:- Utilities to perform unit conversion (eg. seconds > minutes). Problem: Tedious to infer base unit from data. - LATER
    def analyze_query(self, query=None, dialog=None, debug=None, verbose=None,attributemap=None):
        # type: (str) -> dict
        self.execution_durations = dict()
        self.extracted_vis_type = None
        self.extracted_vis_token = None
        self.extracted_tasks = OrderedDict()
        self.extracted_attributes = OrderedDict()

        # CLEAN AND PROCESS QUERY
        self.query_raw = query
        st = time.time()
        if self.language=="cn":
            self.query_raw=self.query_genie_instance.process_chinese(self.query_raw)
        self.query_processed = self.query_genie_instance.process_query(self.query_raw)
        # print("after processed:",self.query_processed)
        self.query_tokens = self.query_genie_instance.clean_query_and_get_query_tokens(self.query_processed, self.reserve_words, self.ignore_words)
        # print("query_tokens:",self.query_tokens)
        self.query_ngrams = self.query_genie_instance.get_query_ngrams(' '.join(self.query_tokens))
        # print("n-grams:",self.query_ngrams)
        self.execution_durations['clean_query'] = time.time() - st

        # DETECT EXPLICIT AND IMPLICIT ATTRIBUTES
        st = time.time()
        self.extracted_attributes = self.attribute_genie_instance.extract_attributes(self.query_ngrams,attributemap)
        querys=list(self.query_ngrams.keys())
        attributes=list(set(attributemap.keys()).difference(set(self.extracted_attributes))) 
        attribute_concept= word2column(querys,attributes)
        print("attribute_concept",attribute_concept)
        # print("query_ngrams",self.query_ngrams)
        # print("attributemap",attributemap)
        self.execution_durations['extract_attributes'] = time.time() - st

        # DETECT IMPLICIT AND EXPLICIT TASKS
        st = time.time()
        task_type=None
        task_type = DecideTask(self.query_processed)
        self.execution_durations['extract_tasks'] = time.time() - st

        """
        # DETECT IMPLICIT AND EXPLICIT TASKS
        st = time.time()
        self.query_for_task_inference = self.task_genie_instance.prepare_query_for_task_inference(self.query_processed)
        self.dependencies = self.task_genie_instance.create_dependency_tree(self.query_for_task_inference)
        task_map = self.task_genie_instance.extract_explicit_tasks_from_dependencies(self.dependencies)

        # Filters from Domain Values
        task_map = self.task_genie_instance.extract_explicit_tasks_from_domain_value(task_map)

        # At this stage, which attributes are encodeable?
        encodeable_attributes = self.attribute_genie_instance.get_encodeable_attributes()

        # INFER tasks based on (encodeable) attribute Datatypes
        task_map = self.task_genie_instance.extract_implicit_tasks_from_attributes(task_map, encodeable_attributes)

        # From the generated TaskMap, ensure that the task "keys" are NOT EMPTY LISTS
        self.extracted_tasks = self.task_genie_instance.filter_empty_tasks(task_map)
        """

        # Prepare output
        output = {
            # 'query_raw': self.query_raw,
            # 'query_processed': self.query_processed,
            'attribute': list(self.extracted_attributes),
            'task': task_type,
        }
        # print("meta_data:",self.get_metadata())
        # print(self.execution_durations)
        return output

    # Update the attribute datatypes that were not correctly detected by NL4DV
    def set_attribute_datatype(self, attr_type_obj):
        return self.data_genie_instance.set_attribute_datatype(attr_type_obj=attr_type_obj)

    # Set Label attribute for the dataset, i.e. one that defines what the dataset is about.
    # e.g. "Correlate horsepower and MPG for sports car models" should NOT apply an explicit attribute for models since there are two explicit attributes already present.
    def set_label_attribute(self, label_attribute):
        return self.data_genie_instance.set_label_attribute(label_attribute=label_attribute)

    # WORDS that should be IGNORED in the query, i.e. NOT lead to the detection of attributes and tasks
    # `Movie` in movies dataset
    # `Car` in cars dataset
    def set_ignore_words(self, ignore_words):
        return self.data_genie_instance.set_ignore_words(ignore_words=ignore_words)

    # Custom STOPWORDS that should NOT removed from the query, as they might be present in the domain.
    # e.g. `A` in grades dataset
    def set_reserve_words(self, reserve_words):
        return self.data_genie_instance.set_reserve_words(reserve_words=reserve_words)

    # Sets the AliasMap
    def set_alias_map(self, alias_value=None, alias_url=None):
        return self.data_genie_instance.set_alias_map(alias_value=alias_value, alias_url=alias_url)

    # Sets the Dataset
    def set_data(self, data_url=None, data_value=None):
        return self.data_genie_instance.set_data(data_url=data_url, data_value=data_value)

    # Sets the String Matching, Domain Word Limit, ... Thresholds
    def set_thresholds(self, thresholds):
        for t in thresholds:
            if t in self.match_thresholds and (isinstance(thresholds[t], float) or isinstance(thresholds[t], int)):
                self.match_thresholds[t] = thresholds[t]

    # Sets the Scoring Weights for the way attributes / tasks and visualizations are detected.
    def set_importance_scores(self, scores):
        # domain = {'attribute', 'task', 'vis'}
        for domain in scores.keys():
            if domain in self.match_scores and isinstance(scores[domain], dict):
                # setting = {'attribute_exact_match', 'attribute_similarity_match', 'attribute_alias_exact_match', ... so on}
                for setting in scores[domain].keys():
                    if setting in self.match_scores[domain] and isinstance(scores[domain][setting], float):
                        self.match_scores[domain][setting] = scores[domain][setting]

    # Get the dataset metadata
    def get_metadata(self):
        return json.loads(json.dumps(self.data_genie_instance.data_attribute_map, cls=helpers.CustomJSONEncoder))

    # Create a dependency parser instance
    def set_dependency_parser(self, config):
        if isinstance(config, dict):
            self.dependency_parser = config["name"]
            if config["name"] == "spacy":
                """
                    Sets the model and returns the Spacy NLP instance. Example ways from the Spacy docs:
                    spacy.load("en") # shortcut link
                    spacy.load("en_core_web_sm") # package
                    spacy.load("/path/to/en") # unicode path
                    spacy.load(Path("/path/to/en")) # pathlib Path
                """
                self.dependency_parser_instance = spacy.load(config["model"])

            elif config["name"] == "corenlp":
                if 'CLASSPATH' not in os.environ:
                    os.environ['CLASSPATH'] = ""

                cpath = config["model"] + os.pathsep + config["parser"]
                if cpath not in os.environ['CLASSPATH']:
                    os.environ['CLASSPATH'] = cpath + os.pathsep + os.environ['CLASSPATH']

                # TODO:- DEPRECATED
                self.dependency_parser_instance = StanfordDependencyParser(path_to_models_jar=config["model"],encoding='utf8')
            elif config["name"] == "corenlp-server":
                # Requires the CoreNLPServer running in the background at the below URL (generally https://localhost:9000)
                # Start server by running the following command in the JARs directory.
                # `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000`
                self.dependency_parser_instance = CoreNLPDependencyParser(url=config["url"])
