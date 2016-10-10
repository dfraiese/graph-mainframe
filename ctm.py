#!/usr/bin/env python
# -*- coding: utf-8
#!/usr/bin/python

__author__ = 'Diego Fraiese'
__copyright__ = "Copyright 2016, Diego Fraiese"
__license__ = "MIT"
__email__ = "dfraiese@gmail.com"
__version__ = "0.1 Beta"

################################################################################
# Python 2,7.1
################################################################################
try:
    import datetime
    import sys
    import os
    from dateutil import parser
    from networkx.readwrite import json_graph
    import networkx as nx
    import json
    import pydot
except Exception, e:
    print str(datetime.datetime.now()) + "-" + "ERROR " + "-" + str(e)
    sys.exit()

def open_file(path, modo):
    try:
        file = open(path, modo)
    except Exception, e:
        print str(datetime.datetime.now()) + "-" + "ERROR " + "-" + str(e)
        sys.exit()
    else:
        return file

def close_file(file):
    try:
        file.close()
    except Exception, e:
        print str(datetime.datetime.now()) + "-" + "ERROR " + "-" + str(e)
        sys.exit()
        
#CADENA = "LEADIA"
s_job = "" 
i = 1

if __name__ == "__main__":
    print "--------------------------------------------------------------------"
    print "Autor       ",  __author__  
    print "Copýright   ", __copyright__  
    print "Licencia    ", __license__ 
    print "Email       ", __email__
    print "Version     ", __version__
    print "--------------------------------------------------------------------"
    
    if len(sys.argv) != 4:
        print "Número de parámetros erroneo: ", len(sys.argv) - 1
        print "Debe informar CADENA odate Path_CADENA"
        print "por ejemplo IC 160801 /home/user/CTM/"
        
        sys.exit()
    else:
        CADENA = sys.argv[1]
        ODATE = sys.argv[2]
        PATH = sys.argv[3]
    
    ###########################################################################
    # Crea dos diccionarios desde la bajada del CTM
    # d_jobs contiene la lista ordenada de jobs
    #        en formato {job: ['predecesor1', 'predecesorn']}
    # d_schema contiene los predecesores
    #        en formato {1: 'job', 2: 'job', n: 'jobn'}
    ###########################################################################
    d_estructura_CTM = {
        "jobname": {"start": 6, "end": 14},
        "predecesor": {"start": 15, "end": 23},
    }

    d_schema = {}
    d_jobs = {}
    s_predecesor = ""
    pathCTM = PATH + CADENA + ".txt"
    
    f = open_file(pathCTM, "r")
    
    for l in f:
        s_job = l[d_estructura_CTM["jobname"]["start"]:
                  d_estructura_CTM["jobname"]["end"]]

        s_predecesor = l[d_estructura_CTM["predecesor"]["start"]:
                         d_estructura_CTM["predecesor"]["end"]]

        if s_job != "" and s_job != "        ": 
            d_jobs.setdefault(s_job, i)
        
            i = i + 1

            l_predecesor = []
            d_schema.setdefault(s_job, l_predecesor)
            
            if s_predecesor != "" and s_predecesor != "        ":
                l_predecesor.append(s_predecesor)
        elif s_predecesor != "" and s_predecesor != "        ":
            l_predecesor.append(s_predecesor)
        
    close_file(f)
    
    ###########################################################################
    # Obtiene la lista de cputime's completa
    # l_cputime contiene la lista ordenada de archivos
    ###########################################################################
    #pathCputime = "/home/diego/CTM/"
    pathCputime = PATH
    l_cputime = []
    l_files = []
    l_dirs = os.walk(pathCputime)
        
    for root, dirs, files in l_dirs:
        for f in files:
            if os.path.splitext(f)[0].find("cputime" + ODATE) != -1:
                filepath = os.path.join(root, f)
                l_files.append(filepath)  
        
        l_cputime = sorted(l_files)

    ###########################################################################
    # Por cada cputime lo aparea con el diccionario d_jobs y crea un diccionario
    # por fecha con formato 
    #     d_runner = {jobname: [startdate hhmmstart, enddate hhmmend, 
    #                 elapsed, jobid]}
    ###########################################################################
    s_groupname = "" 
    s_startdate = ""
    s_starttime = ""
    s_enddate   = ""
    s_endtime   = ""
    s_elapsed   = ""
    s_jobid     = ""
    
    d_runner = {}
    
    d_estructura_cputime = {
        "groupname": {"start": 68, "end": 88},
        "jobname": {"start": 11, "end": 19},
        "startdate": {"start": 28, "end": 36},
        "starttime": {"start": 37, "end": 42},
        "enddate": {"start": 44, "end": 52},
        "endtime": {"start": 53, "end": 62},
        "elapsed": {"start": 63, "end": 69},
        "jobid"  : {"start": 20, "end": 28}
    }
    
    for j in l_cputime:
        f = open_file(j, "r")
        for k in f:
            s_groupname = k[d_estructura_cputime["groupname"]["start"]:
                            d_estructura_cputime["groupname"]["end"]]
                            
            if CADENA in s_groupname:
                s_job = k[d_estructura_cputime["jobname"]["start"]:
                          d_estructura_cputime["jobname"]["end"]]

                s_startdate = k[d_estructura_cputime["startdate"]["start"]:
                                d_estructura_cputime["startdate"]["end"]]

                s_starttime = k[d_estructura_cputime["starttime"]["start"]:
                                d_estructura_cputime["starttime"]["end"]]

                s_enddate = k[d_estructura_cputime["enddate"]["start"]:
                              d_estructura_cputime["enddate"]["end"]]

                s_endtime = k[d_estructura_cputime["endtime"]["start"]:
                              d_estructura_cputime["endtime"]["end"]]

                s_elapsed = k[d_estructura_cputime["elapsed"]["start"]:
                              d_estructura_cputime["elapsed"]["end"]]

                s_jobid = k[d_estructura_cputime["jobid"]["start"]:
                            d_estructura_cputime["jobid"]["end"]]

                dtini = str(parser.parse(s_startdate + " " + s_starttime))
                
                (m, s) = s_elapsed.split(':')
                masElapsed = datetime.timedelta(minutes=int(m), seconds=int(s))
                endMasElapsed = str(parser.parse(s_endtime) + masElapsed)

                dtend = str(parser.parse(s_enddate + " " + endMasElapsed[10:19]))
                
                d_runner[s_job] = [dtini, dtend, s_elapsed, s_jobid]

        close_file(f)
        
    ###########################################################################
    # Por cada job en el diccionario d_runner genera un diccionario final
    # con los jobs y predecesores que ejecutaron ese dia, usando d_schema  
    # con formato
    #     d_jobOdate = {jobname: startdate hhmmstart, startend hhmmend, 
    #                   elapsed, jobid, [nPredecesores]}
    #
    # si no hay predecesor se completa el diccionario con una lista de un
    # elemento conteniendo ["-"]
    ###########################################################################
    d_aux = {}
    
    for j in d_runner:
        if d_schema.has_key(j):
            n = len(d_schema[j])
            
            if n > 0:
                l = []
                
                for k in range(n):
                    if d_runner.has_key(d_schema[j][k]):
                        l.append(d_schema[j][k])
                
                d_aux[j] = [d_runner[j], l]
            else:
                d_aux[j] = [d_runner[j], ["-"]]
    
    ###########################################################################
    # Se genera un archivo .cvs con la salida final de job por orden de 
    # ejecucion de job haciendo ordenamiento por seleccion (starttime + jobid)
    ###########################################################################
    d_jobOdate = {}
    l_aux = []
    l_tmp = []
        
    for i in d_aux:
        l_aux.append(i + d_aux[i][0][0] + d_aux[i][0][3])
                
    n = len(l_aux)
    
    for i in range(0, n - 1):
        n_min = i
        
        for j in range(i + 1, n):
            if l_aux[n_min][8:34] > l_aux[j][8:34]:
                n_min = j
        
        
        l_tmp = l_aux[n_min]
        l_aux[n_min] = l_aux[i]
        l_aux[i] = l_tmp
        
    
    f = open_file(PATH + CADENA + "_" + ODATE + ".cvs", "w+")
    
    for i in l_aux:
        s = i[0:8] + " " + str(d_aux[i[0:8]][0][0]) + " " + \
            str(d_aux[i[0:8]][0][1]) + " " + \
            str(d_aux[i[0:8]][1]) + "\n"
        
        f.write(s)
    
    close_file(f)
    
    ###########################################################################
    # Se genera un .png en el path definido y json para la libreria 
    # javascript D3
    ###########################################################################
    s_jobNode = ""
    n_cant = 0
    
    G = nx.Graph()
    graph = pydot.Dot(graph_type='digraph')
    
    for i in l_aux:
        s_jobNode = i[0:8]
        graph.add_node(pydot.Node(s_jobNode))
        G.add_node(s_jobNode)

        n_cant = n_cant + 1
        
        for j in d_aux[i[0:8]][1]:
            if j != None and j != "-":
                graph.add_edge(pydot.Edge(j, i[0:8]))
                G.add_edge(j, i[0:8])
                
    
    nx.draw_spring(G, with_labels =False, node_size=30)
    d = json_graph.node_link_data(G)
    json.dump(d, open(PATH + CADENA + "_" + ODATE + ".json", "w"))

    graph.write_png(PATH + CADENA + "_" + ODATE + ".png")
    
    print "Nodos       ", n_cant
    print "--------------------------------------------------------------------"

    
