from typing import Dict, List, Optional
import clyngor
from clyngor.answers import Answers
from visrec.src.Transform import Asp2Vl
import logging
import subprocess
import os
import tempfile
import json
from time import time
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_cache: Dict[str, bytes] = {}

DRACO_LP_DIR = './visrec/asps'
DRACO_LP = [
    "define.lp",
    "generate.lp",
    "rules.lp",
    "output.lp",
    "task.lp"
]

# Answer Class
class Result:
    props: List[str]
    cost: Optional[int]
    Ops: List[str]
    fields:List[str]
    count:int
    task:set()
    svg:List

    def __init__(self, answers: Answers, cost: Optional[int] = None):
        props: List[str] = []
        Ops: List[str] = []
        for ((head, body),) in answers:
            if head == "cost":
                cost = int(body[0])
            else:
                b = ",".join(map(str, body))
                props.append(f"{head}({b}).")

        self.props = props
        self.cost = cost
        self.Ops = []
        self.fields=[]
        self.count=0
        self.task=set()
        self.svg=[]

    def __lt__(self, other):  # override <操作符
        if self.count>other.count:
            return True
        elif self.count<other.count:
            return False
        elif self.cost < other.cost:
            return True
        return False
    
    def __eq__(self, other):
        return self.props == other.props

    def as_vl(self) -> Dict:
        return Asp2Vl(self.props)


def load_file(path: str):
    content = file_cache.get(path)
    if content is not None:
        return content
    with open(path,'r',encoding='UTF-8') as f:
        content = f.read().encode("utf8")
        file_cache[path] = content
        return content


def run_clingo(
        draco_query: List[str],
        constants: Dict[str, str] = None,
        files: List[str] = None,
        relax_hard=False,
        silence_warnings=False,
        debug=False):
    """Run CLingo and return stderr and stdout"""
    files = files or DRACO_LP

    if relax_hard and "hard-integrity.lp" in files:
        files.remove("hard-integrity.lp")

    constants = constants or {}

    #     options = ["--outf=2", "--quiet=1,2,2"]
    # options = ["--outf=2"]
    options = ["--outf=2", "-n 0", "--project"]
    if silence_warnings:
        options.append("--warn=no-atom-undefined")
    for name, value in constants.items():
        options.append(f"-c {name}={value}")

    cmd = ["clingo"] + options
    logger.debug("Command: %s", " ".join(cmd))
    proc = subprocess.Popen(
        args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env={'PATH': os.environ['PATH']}
    )
    program = u"\n".join(draco_query)
    file_names = [os.path.join(DRACO_LP_DIR, f) for f in files]
    asp_program = b"\n".join(map(load_file, file_names)) + program.encode("utf8")
    # print("asp_program:", asp_program)
    if debug:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fd:
            fd.write(program)

            logger.info('Debug ASP with "clingo %s %s"',
                        " ".join(file_names), fd.name)
    stdout, stderr = proc.communicate(asp_program)
    return (stderr, stdout)


lock = threading.Lock()
def run(
        draco_query: List[str],
        constants: Dict[str, str] = None,
        files: List[str] = None,
        relax_hard=False,
        silence_warnings=False,
        debug=False,
        clear_cache=False,
        num=10):
    """ Run clingo to compute a completion of a partial spec or violations. """

    # Clear file cache. useful during development in notebooks.
    if clear_cache and file_cache:
        logger.warning("Cleared file cache")
        file_cache.clear()
    # Call CLingo
    # time_s = time()
    stderr, stdout = run_clingo(
        draco_query, constants, files, relax_hard, silence_warnings, debug
    )
    # time_e = time()
    # print("Clingo time last %f " % (time_e - time_s))
    try:
        json_result = json.loads(stdout)
    except json.JSONDecodeError:
        logger.error("stdout: %s", stdout)
        logger.error("stderr: %s", stderr)
        raise
    # Analysis CLingo stdout
    result = json_result["Result"]
    if result == "OPTIMUM FOUND" or "SATISFIABLE":
        StdoutNumber = json_result["Models"]["Number"]
        if num == 0:
            AnsNumber = StdoutNumber
        else:
            AnsNumber = StdoutNumber if StdoutNumber < num else num
        if "Witnesses" in json_result["Call"][0]:
            answers = json_result["Call"][0]["Witnesses"][StdoutNumber - AnsNumber:]
            answers.reverse()
        else:
            return None
        AnswerList=[]
        for i in range(AnsNumber):
        #     # if 'Cost' in answers[i]:
        #     #     AnswerList.append(Result(clyngor.Answers(answers[i]["Value"]).sorted, cost=answers[i]["Costs"]))
        #     # else:
            AnswerList.append(Result(clyngor.Answers(answers[i]["Value"]).sorted, cost=0))
        # print("Find %d answers, select top%d" % (StdoutNumber, len(AnswerList)))
        return AnswerList
    else:
        logger.error("Unsupported result: %s", result)
        return None
