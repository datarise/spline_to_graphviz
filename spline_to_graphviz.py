import json
from graphviz import Digraph

class PlotLinage:
    def __init__(self, path_to_json):
        with open(path_to_json) as json_file:
            self.linage = json.load(json_file)
        self.data = {}
        self.data["reads"] = self.linage["operations"]["reads"]
        self.data["write"] = self.linage["operations"]["write"]
        self.data["other"] = self.linage["operations"]["other"]

    def plot(self, output_path):
        def plot_reads(read):
            id_num = read["id"]
            name = read["extra"]["name"]
            sourceType = read["extra"]["sourceType"]
            inputSources = read["inputSources"][0]
            plot_string = f"Read \n ID: {id_num} \n Name: {name} \n SourceType: {sourceType} \n InputSources: \n {inputSources}"
            return plot_string

        def plot_writes(write):
            id_num = write["id"]
            name = write["extra"]["name"]
            destinationType = write["extra"]["destinationType"]
            outputSource =  write["outputSource"]
            plot_string = f"Write \n ID: {id_num} \n Name: {name} \n DestinationType: {destinationType} \n OutputSource: \n {outputSource}"

            pairs = [[str(child), str(write["id"])] for child in write["childIds"]]

            return plot_string, pairs

        def plot_other(other):
            id_num = other["id"]
            name = other["extra"]["name"]

            if "aggregateExpressions" in str(other["params"]):
                agg_type = other["params"]["aggregateExpressions"][1]["child"]["children"][0]["name"]
                plot_string = f"Name: {name} \n ID: {id_num} \n Type: {agg_type}"
            else: 
                plot_string = f"Name: {name} \n ID: {id_num}"
            
            pairs = [[str(child), str(other["id"])] for child in other["childIds"]]

            return plot_string, pairs


        dot = Digraph()
        for read in self.data["reads"]:
            plot_string = plot_reads(read)
            dot.node(str(read["id"]), plot_string)
        
        pairs = []

        for other in self.data["other"]:
            plot_string, pair = plot_other(other)
            pairs = pairs + pair
            dot.node(str(other["id"]), plot_string)

        plot_string, pair = plot_writes(self.data["write"])
        pairs = pairs + pair
        
        dot.node(str(self.data["write"]["id"]), plot_string)

        for pair in pairs:
            dot.edge(pair[0], pair[1])

        dot.format = 'png'
        dot.render(output_path)  

# Select input file
linage = PlotLinage("splineoutput.json")
# Select output file
linage.plot("linage_test")