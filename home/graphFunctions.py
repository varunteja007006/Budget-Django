from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcdefaults()

def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])

class GraphFunctions:

    def get_graph_bar(self, x, y, xlabel, ylabel, graph_title):
        fig = plt.figure()
        plt.bar(x, y)
        addlabels(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(graph_title)
        plt.tight_layout()
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data


    def get_graph_barh(self, y_pos, exp, ylabel, xlabel, graph_title):
        fig = plt.figure()
        colours = ['#0d6efd', '#6610f2', '#0dcaf0', '#d63384',
                   '#dc3545', '#fd7e14', '#ffc107', '#198754']
        plt.barh(y_pos, exp, align='center', alpha=0.8, color=colours)
        plt.yticks(y_pos, ylabel)
        plt.xlabel(xlabel)
        plt.title(graph_title)
        plt.tight_layout()
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data


    def get_graph_plot(self, x, y, xlabel, ylabel, graph_title, colour):
        fig = plt.figure()
        plt.plot(x, y, color=colour, label=graph_title,
                 marker='o', linestyle='--', linewidth=0.9)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(graph_title)
        plt.tight_layout()
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data


    def get_graph_pie(self,overall_exp, types, graph_title):
        fig = plt.figure()
        colours = ['#0d6efd', '#fd7e14','#6610f2', '#33ff66', '#74acfc', '#ff8791','#a8fff9',
                     '#ffc107']
        explode = [0, 0, 0, 0, 0, 0,0, 0]
        plt.pie(overall_exp, labels=types, explode=explode[:len(types)], colors=colours, wedgeprops={
                'edgecolor': 'black', }, autopct="%1.1f%%")
        plt.title(graph_title)
        plt.tight_layout()
        # plt.legend()
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data
