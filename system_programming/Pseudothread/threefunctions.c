#include "threadutils.h"

void BinarySearch(int thread_id, int init, int maxiter)
{
    ThreadInit(thread_id, init, maxiter);
    /*
    Some initilization if needed.
    */
    Current->y=0;
    Current->z=100;
    for (Current->i = 0; Current->i < Current->N; ++Current->i)
    {
        sleep(1);
        /*
        Do the computation, then output result.
        Call ThreadExit() if the work is done.
        */
	int temp=(Current->y+Current->z)/2;
	printf("BinarySearch: %d\n",temp);
	if(temp==Current->x){
		ThreadExit();
	}else if(temp < Current->x){
		Current->y=temp+1;
	}else{
		Current->z=temp-1;
	}
        ThreadYield();
    }
    ThreadExit()
}

void BlackholeNumber(int thread_id, int init, int maxiter)
{
    ThreadInit(thread_id, init, maxiter);
    /*
    Some initilization if needed.
    */
    for (Current->i = 0; Current->i < Current->N; ++Current->i)
    {
        sleep(1);
        /*
        Do the computation, then output result.
        Call ThreadExit() if the work is done.
        */  
	int a[3];
	a[0]=Current->x/100;
	a[1]=Current->x/10%10;
	a[2]=Current->x%10;
	for(int n=0;n<3;n++)
		for(int m=0;m<2;m++)
			if(a[m]<a[m+1]){
				int temp=a[m+1];
				a[m+1]=a[m];
				a[m]=temp;
			}
	Current->x=(a[0]-a[2])*100+a[2]-a[0];
	printf("BlackholeNumber: %d\n",Current->x);
	if(Current->x==495){
		ThreadExit();
	}
	ThreadYield();
    }
    ThreadExit()
}

void FibonacciSequence(int thread_id, int init, int maxiter)
{
    ThreadInit(thread_id, init, maxiter);
    /*
    Some initilization if needed.
    */
    Current->x=0;
    Current->y=1;
    for (Current->i = 0; Current->i < Current->N; ++Current->i)
    {
        sleep(1);
        /*
        Do the computation, then output result.
        */  
	Current->z=Current->x+Current->y;
	printf("FibonacciSequence: %d\n",Current->z);
	Current->x=Current->y;
	Current->y=Current->z;
        ThreadYield();
    }
    ThreadExit()
}
