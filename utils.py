import numpy as np

def receiveInput():
    # receive input
    str_in=input("Input number n and m for number of decision variables\t")

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
        C[0][i]=-float(str_in[i]) #input c
    for i in range(m): #m line of constrains
        str_in=input("Input Phrase\t").split()
        for j in range(n): #n decision variable coffecient
            A[i][j]=float(str_in[j])
        B[i][0]=float(str_in[n])
        d=int(str_in[n+1])
        add_n=np.append(add_n,d) #m
        if d!=0:
            counter_slack=counter_slack+1
    counter_double=0
    str_in=input("Input E\t").split()

    for i in range(n):
        this=float(str_in[i])
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
                realA[:,pointerA]=A[:,i]
                realA[:,pointerA+1]=-A[:,i]
                realC[0][pointerA]=C[0][i]
                realC[0][pointerA+1]=-C[0][i]
                IndexStore[i][0]=i
                IndexStore[i][1]=i+1
                pointerA=pointerA+2
            elif e[i]==-1:
                realA[:,pointerA]=-A[:,i]
                realC[0][pointerA]=-C[0][i]
                pointerA=pointerA+1
            else:
                realA[:,pointerA]=A[:,i]
                realC[0][pointerA]=C[0][i]
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
