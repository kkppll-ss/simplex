

import numpy as np

import utils as user

def Solve(A,b,C,op):
    #A m*n martxi
    #b m*1 matrix
    #C 1*n matrix
    #op valid initial value  n nparry ,0 1 number, 1 for basic list, 0 for otherwise
    # max standard
    n=np.shape(A)[1]
    m=np.shape(A)[0]


    while 1:

        B=np.zeros([m,m])
        B=np.mat(B) # m* m matrix
        N=np.zeros([m,n-m])
        N=np.mat(N)
        Cn=np.zeros([1,n-m])
        Cn=np.mat(Cn)
        Cb=np.zeros([1,m])
        Cb=np.mat(Cb)
        pointerN=0
        pointerB=0
        for i in range(n):
            if op[i]==1: # is a basic
                B[:,pointerB]=A[:,i]
                Cb[:,pointerB]=C[:,i]
                pointerB=pointerB+1
            else:  # is not a basic
                N[:,pointerN]=A[:,i]
                Cn[:,pointerN]=C[:,i]
                pointerN=pointerN+1
        B_inv=B.I #m*m matrix
        Gettrue=True
        constantValue=B_inv*b #m*1 matrix
        MinValue=0
        IndexOut=0
        for i in range(m):
            tempSum=constantValue[i].sum()
            if tempSum<MinValue:
                MinValue=tempSum
                Gettrue=False
                IndexOut=i
                #print(IndexOut)
        if Gettrue==True: #we find our final result
            X_out=B_inv*b
            Z=Cb*B_inv*b
            return X_out,op,Z,1 #final 1 means we get a solid result
        #  doesn't find result
        coF=B_inv[IndexOut,:]*N #1*n-m matrix
        coFLine=Cn-Cb*B_inv*N # 1*n-m matrix
        MinRatio=100000000
        InIndex=0
        NoResult=True
        for i in range(n-m):
            temp=coF[0,i].sum()
            if(temp<0):
                NoResult=False
                tempA=coFLine[0,i].sum()/temp
                if tempA<MinRatio:
                    MinRatio=tempA
                    InIndex=i
        #enter new one
        if NoResult==True:
            return 0,0,0,-1  #final 0 means we get a wrong result


        counter_out=0
        counter_in=0
        for i in range(n):
            if op[i]==1:
                if(counter_out==IndexOut):
                    op[i]=0
                counter_out=counter_out+1
            else:
                if(counter_in==InIndex):
                    op[i]=1
                counter_in=counter_in+1

        #print(op)

if __name__ == "__main__":
    # n=5
    # m=3
    # A=np.array([[1,1,1,0,0],[0,2,1,1,0],[0,-4,-6,0,1]])
    # A=np.mat(A)
    # C=np.array([2,1,0,0,0])
    # C=np.mat(C)
    # b=np.array([5,5,-9])
    # b=np.mat(b)
    # b=b.T
    # Solve(A,b,C,op):
    A,b,C,whatever,e_index,counter_slack,add_n=user.receiveInput()

    totalLength=np.shape(A)[1]
    op=np.zeros([totalLength],dtype=np.int32)

    for i in range(np.shape(C)[1]):
        if C[0,i]>0:
            print("Cannot be solved by dual simplex, Because in a standard form, all C should be non-negative")
            exit(0)
    for i in range(np.shape(add_n)[0]):
        if add_n[i] ==0:
            print("Cannot be solved by dual simplex, Because a equal constraint")
            exit(0)
    op[totalLength-counter_slack:]=1
    #op=np.array([1,0,0,1,1])



    X_out,op,Z,type=Solve(A,b,C,op)
    #        return X_out,op,Z,1 #final 1 means we get a solid result

    if type==-1:
        print(-1)
        exit(0)
    else:
        print(type)
    X_out=np.array(X_out)
    Real_length=np.shape(whatever)[0]
    n_after=np.shape(op)[0]
    X_out_before=np.zeros([n_after])
    pointerToXout=0



    for i in range(n_after):
        if op[i]==1:
            X_out_before[i]=X_out[pointerToXout][0]
            pointerToXout=pointerToXout+1

    X_output=np.zeros([Real_length])


    pointerToop=0
    for i in range(Real_length):
        if e_index[i]==0: #no constraint
            X_output[i]=X_out_before[pointerToop]-X_out_before[pointerToop+1]
            pointerToop=pointerToop+2
        elif e_index[i]==-1:
            X_output[i]=-X_out_before[pointerToop]
            pointerToop=pointerToop+1
        else:
            X_output[i]=X_out_before[pointerToop]
            pointerToop=pointerToop+1


    print(Z[0,0])
    for i in range(Real_length):
        print(X_output[i],end=" ")

    # print("X_output")
    # print(X_output)
    # print("Z")
    #
    # print(Z)
    # print("Op")
    # print(op)
    #
    # print("type")
    # print(type)
