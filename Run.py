import time,os,Show_Results
from Simulator import *
from Result_Extractor import *
def generate_coordinates(filename, num_points,xc,yc,zc,nsenders):
        coordinates = []
        #sender nodes
        for i in range(nsenders):
            x = random.randint(0, xc)
            y = random.randint(0, yc)
            z = zc  
            coordinates.append(f"{x},{y},{z}\n")
        #sink node
        coordinates.append(f"{xc//2},{yc//2},{0}\n")            
        # other nodes
        for i in range(num_points-1-nsenders):
            x = random.randint(0, xc)
            y = random.randint(0, yc)
            z = random.randint(0, zc)
            coordinates.append(f"{x},{y},{z}\n")
        with open(filename, 'w') as file:
            file.writelines(coordinates)
current_time=time.time()
Period_Length=10 # interval that SDN controller anounces new paths
log_file="log.txt"
total_results_file="Total_Results.txt"
result_file="Results.txt"
cor_file="coordinates.txt"
tr_file="Throughput\\Throughput" 
f=open(result_file, "w")   
f.close()
total_nodes=100
#generate_coordinates(cor_file,total_nodes,1000,1000,500,int(total_nodes*0.1))#nn,x,y,z,nsenders
src_dst_pairs=[]
sink=int(total_nodes*0.1)+1 #sink ID
for i in range(1,int(total_nodes*0.1)+1):
    #src_dst_pairs=[[1,10],[3,15],[9,25],[7,19],[8,29]] #first index is src and the second is dst
    src_dst_pairs.append([i,sink])
methods=["Energybased","SDNHopCountShortestPath","NONSDNHopCountShortestPath"]
rates=[2,4,6]#,8,10]
sizes=[50,100,150,200]
for j in range(len(rates)):
    for q in range(len(sizes)):
        for k in range(len(methods)):
            m=Main()
            current_time=time.time()
            m.set_SimTime(300)
            m.set_PacketSize(sizes[q])
            m.Create_Topology(cor_file,sink)
            m.set_PacketRate(rates[j])
            m.set_Method(methods[k])
            m.set_Srcdest_pairs(src_dst_pairs)
            m.set_Sink(sink)
            log_file="log_"+methods[k]+"_"+str(rates[j])+"_"+str(sizes[q])+".txt"
            stringlabel=methods[k]+"_"+str(rates[j])+"_"+str(sizes[q])
            f=open((tr_file+stringlabel+".txt"), "w")   
            f.close()
            f=open(log_file, "w")  
            f.close()
            m.set_LogFile(log_file)
            if methods[k]!="NONSDNHopCountShortestPath":#for non-SDN solutions there is no need to install path periodically
                pthread = PathThread(m,current_time,Period_Length)
                pthread.start()
            else:
                m.Calculate_Paths() # this is called only once for Non-SDN solutiins (To prohibit null paths at the beginning of simulation)
                
            for i in range(len(src_dst_pairs)):
                thread = SenderThread(m,src_dst_pairs[i][0],src_dst_pairs[i][1])
                thread.start()
            thread.join()
            if methods[k]!="NON-SDNHopCountShortestPath":#for non-SDN solutions
                pthread.join()
            m.WriteLog_ToFile()
            #Plot(Topology)
            print("\nSim Time=",time.time()-current_time)
            Extract_Results(log_file,result_file,(tr_file+stringlabel+".txt"),stringlabel,total_nodes)
            os.remove(log_file)
    Show_Results.extract_data(result_file,str(sizes[q]))
    with open(total_results_file, 'a') as f2:
        with open(result_file, 'r') as f1:
            f2.write(f1.read())
    f=open(result_file, "w")  # reset file and clean it 
    f.close()