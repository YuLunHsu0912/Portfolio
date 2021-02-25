#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<fcntl.h>
int bid_list[21]={20,18,5,21,8,7,2,19,14,13,9,1,6,10,16,11,4,12,15,17,3};

int main(int argc, char*argv[])
{
	int player_id=atoi(argv[1]);//one arqument for id of player


#ifdef DEBUG
	printf("player id =%d\n",player_id);
#endif
	for(int a=1;a<=10;a++)
	{
		int bid=bid_list[player_id+a-2]*100;
		printf("%d %d\n",player_id,bid);
		fflush(stdout);
		fsync(STDOUT_FILENO);;
	}
	exit(0);
}
