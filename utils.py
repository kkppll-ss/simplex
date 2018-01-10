import numpy as np

def receiveInput():
    # receive input
    str_in=input("Input number n for number of decision variables\t")

    n,m =[int(k) for k in str_in.split()]
    A=np.zeros([m,n])
    C=np.zeros([1,n])
    B=np.zeros([m,1])
    add_n=np.array([]) #varibale number after standard
    e=np.array([],dtype=np.int32) #varibale number after standard

    #first line of cn
    counter_slack=0 #number of slack variable
    str_in=input("Input C\t").split()
    # print(str_in[0])
    # print(str_in[1])

    for i in range(n):
        C[0][i]=-int(str_in[i]) #input c
    for i in range(m): #m line of constrains
        str_in=input("Input Phrase\t").split()
        for j in range(n): #n decision variable coffecient
            A[i][j]=int(str_in[j])
        B[i][0]=int(str_in[n])
        d=int(str_in[n+1])
        add_n=np.append(add_n,d) #m
        if d!=0:
            counter_slack=counter_slack+1

    counter_double=0
    str_in=input("Input E\t").split()

    for i in range(n):
        this=int(str_in[i])
        e=np.append(e,this)
        if this==0: #no constraint
            counter_double=counter_double+1
    print("Input finished")

    total_length=n+counter_double+counter_slack
    IndexStore=np.zeros([n,2],dtype=np.int32) # double index * 2(real index)
    realA=np.zeros([m,total_length])
    realC=np.zeros([1,total_length])
    pointerA=0
    for i in range(n):
        #first we handle double
            if e[i] ==0:
                realA[:,i]=A[:,pointerA]
                realA[:,i+1]=-A[:,pointerA]
                realC[0][i]=C[0][pointerA]
                realC[0][i+1]=-C[0][pointerA]
                IndexStore[pointerA][0]=i
                IndexStore[pointerA][1]=i+1
                pointerA=pointerA+1
            elif e[i]==-1:
                realA[:,i]=-A[:,pointerA]
                realC[0][i]=-C[0][pointerA]
                pointerA=pointerA+1
            else:
                realA[:,i]=A[:,pointerA]
                realC[0][i]=C[0][pointerA]
                pointerA=pointerA+1

    for i in range(m):
            if add_n[i]==-1:
                temp=np.zeros([m])
                temp[i]=temp[i]+1
                realC[0][pointerA]=0
                realA[:,pointerA]=temp
                pointerA=pointerA+1

            elif add_n[i]==1:
                temp=np.zeros([m])
                temp[i]=temp[i]+1
                realC[0][pointerA]=0
                B[i]=-B[i]
                realA[i,:]=-realA[i,:]
                realA[:,pointerA]=temp
                pointerA=pointerA+1

    realA=np.mat(realA) # m * totallength(n) matrix
    realC=np.mat(realC)# 1* totallength matrix
    B=np.mat(B) # m* 1 matrix
    return  realA,B,realC,IndexStore,e,counter_slack,add_n
