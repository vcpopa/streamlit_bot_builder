import graphviz as graphviz

class FlowChart():
    def __init__(self,steps:list,scraper_name):
        self.steps=steps
        self.scraper_name=scraper_name

    def make_flowchart(self):
        dot = graphviz.Digraph(f'{self.scraper_name}Flow',graph_attr={'rankdir':'LR'},node_attr={'color': 'palegreen3',"shape":"box","style":"rounded,filled"},edge_attr={"style":""},format='png') 
        for step,i in zip(self.steps,range(len(self.steps))):
            if len(self.steps)<=1:
                dot.node(f"{i+1}",step)
            else:
                if i==0:
                    dot.node(f"{i+1}",step)
                else:
                    dot.node(f"{i+1}",step)
                    dot.edge(f"{i}",f"{i+1}")

        return dot.render(self.scraper_name)