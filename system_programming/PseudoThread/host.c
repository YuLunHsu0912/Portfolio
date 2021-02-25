#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<unistd.h>
#include<fcntl.h>
#include<stdlib.h>
#include<string.h>
#include<sys/wait.h>
#define DEBUG 1

void err_sys(char *x)//error occur, exit
{
	perror(x);
	exit(1);
}
int main(int argc,char *argv[])
{
	if(argc !=4)
		err_sys("Usage:./host [host_id] [key] [depth]\n");
	int host_id=atoi(argv[1]);
	int key=atoi(argv[2]);
	int depth=atoi(argv[3]);

	int fd_left1[2],fd_left2[2];
	//left_1 for parent write on child left_2 for child write on parent
	int fd_right1[2],fd_right2[2];
	pid_t pid;	
	//fork child//
	if(depth<0||depth>2){
		err_sys("depth error");
	}
	if(depth<=1){
		if(pipe(fd_left1)<0||pipe(fd_left2)<0)
			err_sys("pipe error");
		pid=fork();
		if(pid<0)
			err_sys("fork error");
		else if(pid==0)//left child
		{
			close(fd_left1[1]);
			close(fd_left2[0]);
			if(dup2(fd_left1[0],STDIN_FILENO)!=STDIN_FILENO||dup2(fd_left2[1],STDOUT_FILENO)!=STDOUT_FILENO)
			{
				err_sys("dup error");
			}
			close(fd_left1[0]);
			close(fd_left2[1]);
			//pipe and redirect down
			if(depth<=1)//need to run host again
			{
				char dep[3];
				//itoa(depth+1,dep,10);
				if (depth==0)
				
			//	sprintf(dep,"%d\0",depth+1);
					execl("./host","./host",argv[1],argv[2],"1",(char*)0);
				else
					execl("./host","./host",argv[1],argv[2],"2",(char*)0);
				

			}
		}
		//parent of left child
		close(fd_left1[0]);
		close(fd_left2[1]);
		//right child
		if(pipe(fd_right1)<0||pipe(fd_right2)<0)
				err_sys("pipe error");
		pid_t pid2=fork();
		if(pid2<0)
			err_sys("pipe error");
		else if(pid2==0)
		{
			close(fd_right1[1]);
			close(fd_right2[0]);
			if(dup2(fd_right1[0],STDIN_FILENO)!=STDIN_FILENO||dup2(fd_right2[1],STDOUT_FILENO)!=STDOUT_FILENO)
			{
				err_sys("dup error");
			}
			close(fd_right1[0]);
			close(fd_right2[1]);
			//pipe and redirect down
			if(depth<=1)//need to run host again
			{
				char dep[3];
				//itoa(depth+1,dep,10);
				sprintf(dep,"%d",depth+1);
				execl("./host","./host",argv[1],argv[2],dep,(char*)0);
			}

		}
		//parent of right child and left child
		close(fd_right1[0]);
		close(fd_right2[1]);
		
	}

	if(depth==0)//root
	{
#ifdef DEBUG
//	for(int a=0;a<argc;a++)
//		printf("argc[%d]=%s\n",a,argv[a]);
#endif
	//prepare to read and write FIFO file
	//read from fifo_[host id].tmp write on fifo_0.tmp
		char read_fifo_name[20];
		sprintf(read_fifo_name,"fifo_%d.tmp",host_id);
		FILE *read_fifo=fopen(read_fifo_name,"r");
		if(read_fifo==NULL)
		{	
			printf("error");
		}
		FILE *write_fifo=fopen("fifo_0.tmp","w");
		FILE *left1=fdopen(fd_left1[1],"w");
		FILE *left2=fdopen(fd_left2[0],"r");
		FILE *right1=fdopen(fd_right1[1],"w");
		FILE *right2=fdopen(fd_right2[0],"r");

		int players[8];
		fscanf(read_fifo,"%d %d %d %d %d %d %d %d",&players[0],&players[1],&players[2],&players[3],&players[4],&players[5],&players[6],&players[7]);

		while(players[0]!=-1)
		{
			fprintf(right1,"%d %d %d %d\n",players[4],players[5],players[6],players[7]);
			fprintf(left1,"%d %d %d %d\n",players[0],players[1],players[2],players[3]);
			fflush(left1);
			fsync(fd_left1[1]);
			fflush(right1);
			fsync(fd_right1[1]);
	
			//total 10 rounds
			int data[8][2];
			for(int a=0;a<8;a++)
			{
				data[a][0]=players[a];
				data[a][1]=0;
			}
			for(int a=0;a<10;a++)
			{
				int win1,bid1,win2,bid2;
				fscanf(left2,"%d %d",&win1,&bid1);
				fscanf(right2,"%d %d",&win2,&bid2);
				int win;
				if(bid1>bid2)
					win=win1;
				else
					win=win2;
				
				for(int b=0;b<8;b++)
				{
					if(win==data[b][0])
					{

						data[b][1]++;
						break;
					}
				}
			}
			int other[8];
			for(int a=0;a<8;a++)
				other[a]=data[a][1];
			for(int a=0;a<8;a++)
				for(int b=0;b<7;b++)
					if(other[b]<other[b+1])
					{
						int temp=other[b];
						other[b]=other[b+1];
						other[b+1]=temp;
					}
			int ranktable[8][2];
			ranktable[0][0]=other[0];
			ranktable[0][1]=1;
			int count=1;
			for(int a=1;a<8;a++)
			{
				if(other[a]!=ranktable[a-1][0])
				{
					ranktable[a][0]=other[a];
					ranktable[a][1]=count+1;
					count++;
				}else{
					ranktable[a][0]=other[a];
					ranktable[a][1]=ranktable[a-1][1];
					count++;
				}
			}
			for(int a=0;a<8;a++)
			{
				for(int b=0;b<8;b++){
					if(data[a][1]==ranktable[b][0])
					{
						data[a][1]=ranktable[b][1];
						break;
					}
				}
			}

			
			fprintf(write_fifo,"%s\n",argv[2]);
			for(int a=0;a<8;a++)
			{
				fprintf(write_fifo,"%d %d\n",data[a][0],data[a][1]);
			}
			fflush(write_fifo);
			fsync(fileno(write_fifo));
			fscanf(read_fifo,"%d %d %d %d %d %d %d %d",&players[0],&players[1],&players[2],&players[3],&players[4],&players[5],&players[6],&players[7]);
		}

		
		fprintf(right1,"-1 -1 -1 -1\n");
		fprintf(left1,"-1 -1 -1 -1\n");
		
		fflush(left1);
		fsync(fd_left1[1]);
		fflush(right1);
		fsync(fd_right1[1]);
		
		//wait for two children end
		wait(NULL);
		wait(NULL);
		fclose(left1);
		fclose(left2);
		fclose(right1);
		fclose(right2);
		close(fd_left1[1]);
		close(fd_left2[0]);
		close(fd_right1[1]);
		close(fd_right2[0]);
		exit(0);	

	}else if(depth==1){
		FILE *left1=fdopen(fd_left1[1],"w");
		FILE *left2=fdopen(fd_left2[0],"r");
		FILE *right1=fdopen(fd_right1[1],"w");
		FILE *right2=fdopen(fd_right2[0],"r");
		int players[4];
		scanf("%d %d %d %d",&players[0],&players[1],&players[2],&players[3]);
		while(players[0]!=-1){
			fprintf(right1,"%d %d\n",players[2],players[3]);
			fprintf(left1,"%d %d\n",players[0],players[1]);
			
			fflush(left1);
			fsync(fd_left1[1]);
			fflush(right1);
			fsync(fd_right1[1]);
			for(int a=0;a<10;a++)
			{
				int win1,bid1,win2,bid2;
				fscanf(left2,"%d %d",&win1,&bid1);
				fscanf(right2,"%d %d",&win2,&bid2);
				int win;
				if(bid1>bid2)
					printf("%d %d\n",win1,bid1);
				else
					printf("%d %d\n",win2,bid2);
				fflush(stdout);
				fsync(STDOUT_FILENO);
				
			}
			scanf("%d %d %d %d",&players[0],&players[1],&players[2],&players[3]);
		}

		fprintf(left1,"-1 -1\n");
		fprintf(right1,"-1 -1\n");

		fflush(left1);
		fsync(fd_left1[1]);
		fflush(right1);
		fsync(fd_right1[1]);
		
		//wait for two children end
		wait(NULL);
		wait(NULL);
		fclose(left1);
		fclose(left2);
		fclose(right1);
		fclose(right2);
		close(fd_left1[1]);
		close(fd_left2[0]);
		close(fd_right1[1]);
		close(fd_right2[0]);
		exit(0);	
	}else if(depth==2){
		int players[2];
		scanf("%d %d",&players[0],&players[1]);

		while(players[0]!=-1&&players[1]!=-1){
			if(pipe(fd_left1)<0||pipe(fd_left2)<0)
				err_sys("pipe error");
			pid=fork();
			if(pid<0)
				err_sys("fork error");
			else if(pid==0)//left player
			{
				close(fd_left1[1]);
				close(fd_left2[0]);
				if(dup2(fd_left1[0],STDIN_FILENO)!=STDIN_FILENO||dup2(fd_left2[1],STDOUT_FILENO)!=STDOUT_FILENO)
				{
					err_sys("dup error");
				}
				close(fd_left1[0]);
				close(fd_left2[1]);
			//pipe and redirect down
				
				//exec player 
				char player1_id[10];
				sprintf(player1_id,"%d",players[0]);
				execl("./player","./player",player1_id,(char*)0);
			}//end fork of left player
			//parent of left child
			close(fd_left1[0]);
			close(fd_left2[1]);
			//right player
			if(pipe(fd_right1)<0||pipe(fd_right2)<0)
					err_sys("pipe error");
			pid_t pid2=fork();
			if(pid2<0)
				err_sys("pipe error");
			else if(pid2==0){
				close(fd_right1[1]);
				close(fd_right2[0]);
				if(dup2(fd_right1[0],STDIN_FILENO)!=STDIN_FILENO||dup2(fd_right2[1],STDOUT_FILENO)!=STDOUT_FILENO){
				err_sys("dup error");
				}
				close(fd_right1[0]);
				close(fd_right2[1]);
			//pipe and redirect down
				char player2_id[10];
				sprintf(player2_id,"%d",players[1]);
				execl("./player","./player",player2_id,(char*)0);
			}//end fork of right player
			close(fd_right1[0]);
			close(fd_right2[1]);

			//parent of players
			FILE *left2=fdopen(fd_left2[0],"r");
			FILE *right2=fdopen(fd_right2[0],"r");
			for(int a=0;a<10;a++)
			{
				int win1,bid1,win2,bid2;
				fscanf(left2,"%d %d",&win1,&bid1);
				fscanf(right2,"%d %d",&win2,&bid2);
				int win;
				if(bid1>bid2)
					printf("%d %d\n",players[0],bid1);
				else
					printf("%d %d\n",players[1],bid2);
				fflush(stdout);
				fsync(STDOUT_FILENO);
				
			}	
			
			wait(NULL);
			wait(NULL);
			fclose(left2);
			fclose(right2);
			close(fd_left2[0]);
			close(fd_right2[0]);
			scanf("%d %d",&players[0],&players[1]);
		}//end while	
		exit(0);
	}
}
