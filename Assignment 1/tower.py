'''
*************************************************************************
            @author Yifei Ge, Ke Wang, Tianyu Zhao
**************************************************************************

'''
import copy
print("Hanoi Tower V2.0, Py 3.5\n Yifei Ge  Ke Wang  Tianyu Zhao")
n = int(input("Input the number of Disk:\n"))
print("The number of Disk is ",n )
m = int(input("Input the number of Peg:\n"))
print("The number of Pegs is ",m)
peg = [[]] #The []*m array stores the current peg
for kkk in range(1, m):
    peg.append([])
peg[0] = list(range(1, n + 1))
total = sum(peg[0])
print("total",total)
print(peg)
dict = {}  #Dictionary, usd to check if one occation occurs before
temp =''  #transfer the code to the peg.
for p in [peg]:
    temp += ''.join(str(i) for i in p)
    temp += ';'
print(temp)
dict[temp]=0
#build a stack to store all the process to jump back
runlog = [[]]
top = -1
#push stack
def stackpush(elem):
    global top
    global runlog
    runlog.append(copy.deepcopy(elem))
    top += 1
#popStack
def stackpop():
    global top
    global runlog
    if top == -1:
        print("empty stack")
    else:
        top -= 1
        return runlog.pop()
stackpush(peg)


def checkdict(mov,target):  #Check if one situation in the dictionary or not
    global dict
    tpeg = copy.deepcopy(peg)
    movetemp = tpeg[mov][0]
    tpeg[mov] = tpeg[mov][1:]
    tpeg[target].insert(0, movetemp)
    tempkey = ''  # transfer the code to the peg.
    for p in [tpeg]:
        tempkey += ''.join(str(i) for i in p)
        tempkey += ';'
    if not tempkey in dict:
        return True
    else:
        return False

def move(mov,target):  #move the target
    global peg
    global dict
    global runlog
    global top
    movtemp=peg[mov][0]
    peg[mov]=peg[mov][1:]
    peg[target].insert(0, movtemp)
    stackpush(peg)
    tempkey=''
    for p in [peg]:
        tempkey += ''.join(str(i) for i in p)
        tempkey += ';'
    dict[tempkey] = 0
    print("current",peg)
    
def checkfinish():
    global peg
    global dict
    global total
    if sum(peg[m-1]) == total:
        return True
    else:
        return False
    
while((not checkfinish()) and (top != -1)):
    keeprun = True
    tempkey = ''
    for i in range (0, m):
        if(keeprun == False):
            break
        for j in range(0, m):
            if j == i:
                if j < m - 1:
                    j = j + 1
                else:
                    break
            if len(peg[i]) == 0:
                break
            else:
                if len(peg[j]) == 0:
                    if checkdict(i, j):
                        move(i, j)
                        keeprun = False
                        break
                elif peg[i][0] < peg[j][0]:
                    if checkdict(i, j):
                        move(i, j)
                        keeprun = False
                        break
                else:
                    if checkdict(j, i):
                        move(j, i)
                        keeprun = False
                        break
    if keeprun == True:
        print("Jump Back to", peg)
        peg = stackpop()
        print("Current Top", top, peg)
print("Finished Successfully the answer should be:", peg)
