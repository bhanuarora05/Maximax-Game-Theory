import time
start = time.clock()
with open('input2.txt') as fin:
    b = int(fin.readline().strip())
    p = int(fin.readline().strip())
    L = int(fin.readline().strip())
    LAHSA = {}
    for i in range(0,L):
        LAHSA[fin.readline().strip()] = 1
    
    S = int(fin.readline().strip())
    SPLA = {}
    for i in range(0,S):
        SPLA[fin.readline().strip()] = 1
    
    A = int(fin.readline().strip())
    Applicants = {}
    for data in fin:
        data = data.strip()
        Applicants[data[:5]] = [data[5],int(data[6:9]),data[9],data[10],data[11],data[12],[int(d) for d in list(data[13:])]]
        
def max_applicant_allotment(current_capacity,list_Applicants,index):
    if index<0:
        return (0,'',[])
    global Applicants
    possible_capacity = [x - y for x, y in zip(current_capacity,Applicants[list_Applicants[index]][6])]
    if min(possible_capacity)<0:
        return max_applicant_allotment(current_capacity,list_Applicants,index-1)
    ret,next_app,path = max_applicant_allotment(possible_capacity,list_Applicants,index-1)
    if next_app=='' or int(list_Applicants[index])<int(next_app):
        return max(max_applicant_allotment(current_capacity,list_Applicants,index-1),(sum(Applicants[list_Applicants[index]][6])+ret,list_Applicants[index],path+[list_Applicants[index]]))
    else:
        return max(max_applicant_allotment(current_capacity,list_Applicants,index-1),(sum(Applicants[list_Applicants[index]][6])+ret,next_app,path+[list_Applicants[index]]))

def find_optimum(turn,SPLA_layout,LAHSA_layout,SPLA_Applicants,LAHSA_Applicants,common_Applicants,depth):
    global b,p,Applicants
    flag = 1
    Max = None
    for applicant in common_Applicants.keys():
        if turn==0:
            SPLA_layout_copy = [x + y for x, y in zip(SPLA_layout,Applicants[applicant][6])]
            if max(SPLA_layout_copy)>p:
                common_Applicants.pop(applicant)
                LAHSA_Applicants[applicant] = 1
        else:
            LAHSA_layout_copy = [x + y for x, y in zip(LAHSA_layout,Applicants[applicant][6])]
            if max(LAHSA_layout_copy)>b:
                common_Applicants.pop(applicant)
                SPLA_Applicants[applicant] = 1
                
    if turn==0:
        for applicant in SPLA_Applicants.keys():
            SPLA_layout_copy = [x + y for x, y in zip(SPLA_layout,Applicants[applicant][6])]
            if max(SPLA_layout_copy)>p:
                SPLA_Applicants.pop(applicant)
    else:
        for applicant in LAHSA_Applicants.keys():
            LAHSA_layout_copy = [x + y for x, y in zip(LAHSA_layout,Applicants[applicant][6])]
            if max(LAHSA_layout_copy)>b:
                LAHSA_Applicants.pop(applicant)
            
        
    if len(common_Applicants)==0:
        b_flag = 1
        SPLA_layout_copy = list(SPLA_layout)
        next_app = ['','']
        for applicant in SPLA_Applicants.keys():
            SPLA_layout_copy = [x + y for x, y in zip(SPLA_layout_copy,Applicants[applicant][6])]
            if max(SPLA_layout_copy)>p:
                b_flag = 0
                break
            if next_app[0]=='' or int(next_app[0])>int(applicant):
                next_app[0] = applicant
        if b_flag:
            ret_1 = sum(SPLA_layout_copy)
            path = SPLA_Applicants.keys()
        else:
            ret,next_app[0],path = max_applicant_allotment([p - x for x in SPLA_layout],SPLA_Applicants.keys(),len(SPLA_Applicants)-1)
            ret_1 = sum(SPLA_layout) + ret
        
        b_flag = 1
        LAHSA_layout_copy = list(LAHSA_layout)
        for applicant in LAHSA_Applicants.keys():
            LAHSA_layout_copy = [x + y for x, y in zip(LAHSA_layout_copy,Applicants[applicant][6])]
            if max(LAHSA_layout_copy)>b:
                b_flag = 0
                break
            if next_app[1]=='' or int(next_app[1])>int(applicant):
                next_app[1] = applicant
        if b_flag:
            ret_2 = sum(LAHSA_layout_copy)
            path2 = LAHSA_Applicants.keys()
        else:
            ret,next_app[1],path2 = max_applicant_allotment([b - x for x in LAHSA_layout],LAHSA_Applicants.keys(),len(LAHSA_Applicants)-1)                
            ret_2 = sum(LAHSA_layout) + ret
        
        return [ret_1,ret_2,next_app[turn],path2+[-2]+path+[-1]]
    
    if turn==0:
        for applicant in common_Applicants.keys():
            SPLA_layout_copy = [x + y for x, y in zip(SPLA_layout,Applicants[applicant][6])]
            flag = 0
            common_Applicants_copy = common_Applicants.copy()
            common_Applicants_copy.pop(applicant)
            SPLA_Applicants_copy = SPLA_Applicants.copy()
            LAHSA_Applicants_copy = LAHSA_Applicants.copy()
            ret_1,ret_2,_,path = find_optimum(1,SPLA_layout_copy,LAHSA_layout,SPLA_Applicants_copy,LAHSA_Applicants_copy,common_Applicants_copy,depth+1)
            if depth==0:
                print applicant,(ret_1,ret_2),path
            #print ret_1+ret_2
            if Max is None or Max[0]<=ret_1:
                if Max is None or Max[0]<ret_1:
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
                elif Max[0]==ret_1 and int(Max[2])>int(applicant):
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
            
        for applicant in SPLA_Applicants.keys():
            SPLA_layout_copy = [x + y for x, y in zip(SPLA_layout,Applicants[applicant][6])]    
            flag = 0
            SPLA_Applicants_copy = SPLA_Applicants.copy()
            SPLA_Applicants_copy.pop(applicant)
            common_Applicants_copy = common_Applicants.copy()
            LAHSA_Applicants_copy = LAHSA_Applicants.copy()
            ret_1,ret_2,_,path = find_optimum(1,SPLA_layout_copy,LAHSA_layout,SPLA_Applicants_copy,LAHSA_Applicants_copy,common_Applicants_copy,depth+1)
            if depth==0:
                print applicant,(ret_1,ret_2),path
            #print ret_1+ret_2
            if Max is None or Max[0]<=ret_1:
                if Max is None or Max[0]<ret_1:
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
                elif Max[0]==ret_1 and int(Max[2])>int(applicant):
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
                
        if flag:
            ret_1,ret_2,next_app,path = find_optimum(0,SPLA_layout,LAHSA_layout,SPLA_Applicants,LAHSA_Applicants,common_Applicants,depth+1)
            return [ret_1,ret_2,next_app,path+['']]
        
    else:
        for applicant in common_Applicants.keys():
            LAHSA_layout_copy = [x + y for x, y in zip(LAHSA_layout,Applicants[applicant][6])]
            flag = 0
            common_Applicants_copy = common_Applicants.copy()
            common_Applicants_copy.pop(applicant)
            SPLA_Applicants_copy = SPLA_Applicants.copy()
            LAHSA_Applicants_copy = LAHSA_Applicants.copy()
            ret_1,ret_2,_,path = find_optimum(0,SPLA_layout,LAHSA_layout_copy,SPLA_Applicants_copy,LAHSA_Applicants_copy,common_Applicants_copy,depth+1)
            #print ret_1+ret_2
            if Max is None or Max[1]<=ret_2:
                if Max is None or Max[1]<ret_2:
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
                elif Max[1]==ret_2 and int(Max[2])>int(applicant):
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
                
        for applicant in LAHSA_Applicants.keys():
            LAHSA_layout_copy = [x + y for x, y in zip(LAHSA_layout,Applicants[applicant][6])]
            flag = 0
            LAHSA_Applicants_copy = LAHSA_Applicants.copy()
            LAHSA_Applicants_copy.pop(applicant)
            common_Applicants_copy = common_Applicants.copy()
            SPLA_Applicants_copy = SPLA_Applicants.copy()
            ret_1,ret_2,_,path = find_optimum(0,SPLA_layout,LAHSA_layout_copy,SPLA_Applicants_copy,LAHSA_Applicants_copy,common_Applicants_copy,depth+1)
            #print ret_1+ret_2
            if Max is None or Max[1]<=ret_2:
                if Max is None or Max[1]<ret_2:
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
                elif Max[1]==ret_2 and int(Max[2])>int(applicant):
                    Max = [ret_1,ret_2,applicant,path+[applicant]]
        
        if flag:
            ret_1,ret_2,next_app,path = find_optimum(0,SPLA_layout,LAHSA_layout,SPLA_Applicants,LAHSA_Applicants,common_Applicants,depth+1)
            return [ret_1,ret_2,next_app,path+['']]

    return Max

SPLA_layout = [0 for i in range(7)]
LAHSA_layout = [0 for i in range(7)]


for applicant in SPLA:
    SPLA_layout = [x + y for x, y in zip(SPLA_layout,Applicants[applicant][6])]

for applicant in LAHSA:
    LAHSA_layout = [x + y for x, y in zip(LAHSA_layout,Applicants[applicant][6])]

#print SPLA,LAHSA
SPLA_Applicants = {}
LAHSA_Applicants = {}
common_Applicants = {}
for applicant in Applicants:
    if applicant in SPLA or applicant in LAHSA:
        continue
    if Applicants[applicant][3]=='N' and Applicants[applicant][4]=='Y' and Applicants[applicant][5]=='Y' and (applicant not in SPLA):
        if Applicants[applicant][0]=='F' and Applicants[applicant][1]>17 and Applicants[applicant][2]=='N' and (applicant not in LAHSA):
            common_Applicants[applicant] = 1
        else:
            SPLA_Applicants[applicant] = 1
    elif Applicants[applicant][0]=='F' and Applicants[applicant][1]>17 and Applicants[applicant][2]=='N' and (applicant not in LAHSA):
        LAHSA_Applicants[applicant] = 1
print Applicants
print common_Applicants,SPLA_Applicants,LAHSA_Applicants
eff,eff2,next_applicant,path = find_optimum(0,SPLA_layout,LAHSA_layout,SPLA_Applicants,LAHSA_Applicants,common_Applicants,0)
print next_applicant,eff,eff2,path
with open('output.txt','w') as fout:
    fout.write(next_applicant)
print "Time Taken: ",time.clock() - start