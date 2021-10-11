import webbrowser
import json

def HTML_Out2(Data, Recos_task,ColumnTypes,Times):
    if len(Recos_task)==0:
        return
    c = d = 0
    for col in ColumnTypes:
        if col["type"] == "quantitative" or col["type"] == "temporal":
            c += 1
        else:
            d += 1
    # FileName = "../html/%dc_%dd_Deduplication.html" % (c, d)
    FileName = "../html/%dc_%dd.html" % (c, d)
    # FileName = "test.html"
    f = open(FileName, 'w')
    message = """
<!DOCTYPE html>
<html>
<head>
<style>
    .error {
        color: red;
    }
</style>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@5"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@4"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@6"></script>
<title>VisRec</title>
</head>
<body> \n"""
    for col in ColumnTypes:
        message += "<a>%s</a></br>\n" % (str(col))
    tasks = Recos_task.keys()
    for task in tasks:
        message += "<br><br><br><b><a>%s</a></b><br><br>\n" % (task)
        if Recos_task[task] is None:
            continue
        message += "<a>Generate <b>%d</b> vis, time last <b>%f</b> s.</a><br>\n" % (len(Recos_task[task]),Times[task])
        for i in range(len(Recos_task[task])):
            message +="<div id='v_%s%d'></div>\n<a>Cost:%.3f</a>" % (task, i, Recos_task[task][i].cost)
                
    message += """
</body></br><script>
(function(vegaEmbed) {
var embedOpt = {"mode": "vega-lite"};
var data = % s;\n""" % (json.dumps({'values': json.dumps(Data)}))

    for task in tasks:
        if Recos_task[task] is None:
            continue
        for i in range(len(Recos_task[task])):
            message = message + \
                "var spec%s%d =%s;\n" % (task, i, json.dumps(Recos_task[task][i].props))
            message = message + "vegaEmbed('#v_%s%d', spec%s%d, embedOpt);\n" % (task, i, task, i)

    message += """
})(vegaEmbed);
</script>
</br>
</html> """
    message = message.replace("True", "true")
    message = message.replace("False", "false")
    message = message.replace("\"vegalitedata\"", "data")
    f.write(message)
    f.close()
    # webbrowser.open(FileName, new=1)


def HTML_Out(Data, Recos, task=None, ColumnTypes=None,time=0):
    if Recos is None:
        return
    # c = d = 0
    # if not ColumnTypes is None:
    #     for col in ColumnTypes:
    #         if col["type"] == "quantitative" or col["type"] == "temporal":
    #             c += 1
    #         else:
    #             d += 1
    # FileName = "../html/%dc_%dd.html" % (c, d)

    # FileName = "../html/individual_recommendation/movies/movies_%s.html" % (task)
    FileName = "test.html"
    f = open(FileName, 'w')
    message = """
<!DOCTYPE html>
<html>
<head>
<style>
    .error {
        color: red;
    }
</style>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@5"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@4"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@6"></script>
<title>VisRec</title>
</head>
<body>\n"""
    if not ColumnTypes is None:
        for col in ColumnTypes:
            message += "<a>%s</a></br>\n" % (str(col))
    message += "<a>Generate <b>%d</b> vis, time last <b>%.3f</b> s.</a><br>\n" % (len(Recos),time)
    for i in range(len(Recos)):
        # message = message + "<div id='vis%d'></div>\n<a>Cost:%.3f</a>" % (i,Recos[i].cost)
        message = message + "<div id='vis%d'></div>" % (i)
    message += """
<script>
(function(vegaEmbed) {
var embedOpt = {"mode": "vega-lite"};
var data=%s;\n""" % (json.dumps({'values': json.dumps(Data)}))

    for i in range(len(Recos)):
        message = message + "var spec%d =%s;\n" % (i, json.dumps(Recos[i].props))
        message = message + "vegaEmbed('#vis%d', spec%d, embedOpt);\n" % (i, i)
    message += """
})(vegaEmbed);
</script>
</body>
</html> """
    message = message.replace("True", "true")
    message = message.replace("False", "false")
    message = message.replace("\"vegalitedata\"", "data")
    f.write(message)
    f.close()
    webbrowser.open(FileName, new=1)