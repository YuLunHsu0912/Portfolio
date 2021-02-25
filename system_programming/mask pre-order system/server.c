#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#define ERR_EXIT(a) do { perror(a); exit(1); } while(0)

typedef struct {
    char hostname[512];  // server's hostname
    unsigned short port;  // port to listen
    int listen_fd;  // fd to wait for a new connection
} server;

typedef struct {
    int id; //customer id
    int adultMask;
    int childrenMask;
} Order;

typedef struct {
    char host[512];  // client's host
    int conn_fd;  // fd to talk with client
    char buf[512];  // data sent by/to client
    size_t buf_len;  // bytes used by buf
    // you don't need to change this.
    int id;
    int wait_for_write;  // used by handle_read to know if the header is read or not.
} request;
typedef struct{
	short l_type;
	off_t l_start;
	short l_whence;
	off_t l_len;
	pid_t l_pid;
}flock;

int lock_reg(int fd,int cmd, int type, off_t offset)
{
	struct flock lock;
	lock.l_type=type;
	lock.l_start=offset*sizeof(Order);
	lock.l_whence=SEEK_SET;
	lock.l_len=sizeof(Order);
	return fcntl(fd,cmd,&lock);

}
#define read_lock(fd,offset,type)\
	lock_reg((fd),F_SETLK,F_RDLCK,(offset))
#define write_lock(fd,offset,type)\
	lock_reg((fd),F_SETLK,F_WRLCK,(offset))
#define unlock(fd,offset)\
	lock_reg((fd),F_SETLK,F_UNLCK,(offset))
server svr;  // server
request* requestP = NULL;  // point to a list of requests
int maxfd;  // size of open file descriptor table, size of request list

const char* accept_read_header = "ACCEPT_FROM_READ";
const char* accept_write_header = "ACCEPT_FROM_WRITE";

static void init_server(unsigned short port);
// initailize a server, exit for error

static void init_request(request* reqP);
// initailize a request instance

static void free_request(request* reqP);
// free resources used by a request instance

int handle_read(request* reqP) {
    char buf[512];
    read(reqP->conn_fd, buf, sizeof(buf));
    memcpy(reqP->buf, buf, strlen(buf));
    return 0;

}

int main(int argc, char** argv) {

    // Parse args.
    if (argc != 2) {
        fprintf(stderr, "usage: %s [port]\n", argv[0]);
        exit(1);
    }

    struct sockaddr_in cliaddr;  // used by accept()
    int clilen;

    int conn_fd;  // fd for a new connection with client
    int file_fd;  // fd for file that we open for reading
    char buf[512];
    int buf_len;

    char error[]="Operation failed.\n";
	
    char read_notation[]="Please enter the id (to check how many masks can be ordered):\n";
    char lock_notation[]="Locked.\n";
    // Initialize server
    init_server((unsigned short) atoi(argv[1]));
    
    // Loop for handling connections
    fprintf(stderr, "\nstarting on %.80s, port %d, fd %d, maxconn %d...\n", svr.hostname, svr.port, svr.listen_fd, maxfd);
    int ok=0;
    fd_set master_set,  working_set;
    FD_ZERO(&master_set);
    FD_SET(svr.listen_fd,&master_set);
#ifdef READ_SERVER
    file_fd=openat(AT_FDCWD,"preorderRecord",O_RDONLY);
#else
    file_fd=openat(AT_FDCWD,"preorderRecord",O_RDWR);
#endif

    while (1) {
        // TODO: Add IO multiplexing
//	memcpy(&working_set,&master_set,sizeof(master_set));
	FD_ZERO(&working_set);
	FD_SET(svr.listen_fd,&working_set);
	for(int a=0;a<maxfd;a++)
	{
		if(requestP[a].conn_fd!=-1)
		{
			FD_SET(requestP[a].conn_fd,&working_set);
		}
	}
	ok=select(maxfd,&working_set,NULL,NULL,NULL);
	if(ok>0)
	{
		if(FD_ISSET(svr.listen_fd,&working_set)){//ready for connect	
        	// Check new connection
        		clilen = sizeof(cliaddr);
        		conn_fd = accept(svr.listen_fd, (struct sockaddr*)&cliaddr, (socklen_t*)&clilen);
        		if (conn_fd < 0) {
           	 		if (errno == EINTR || errno == EAGAIN) continue;  // try again
           			if (errno == ENFILE) {
                			(void) fprintf(stderr, "out of file descriptor table ... (maxconn %d)\n", maxfd);
               			 	continue;
         			}
            			ERR_EXIT("accept");
        		}
        		requestP[conn_fd].conn_fd = conn_fd;
        		strcpy(requestP[conn_fd].host, inet_ntoa(cliaddr.sin_addr));
        		fprintf(stderr, "getting a new request... fd %d from %s\n", conn_fd, requestP[conn_fd].host);
			write(requestP[conn_fd].conn_fd,read_notation,strlen(read_notation));
			continue;
		}//end of connect
		
		//reading and writing
	#ifdef READ_SERVER
		for(int a=0;a<maxfd;a++)
		{
			if(FD_ISSET(requestP[a].conn_fd,&working_set)>0){
				int ret=handle_read(&requestP[a]);
				if(ret<0)
				{
					fprintf(stderr, "bad request from %s\n", requestP[conn_fd].host);
		       			continue;	
				}
				if(atoi(requestP[conn_fd].buf)>902020 || atoi(requestP[conn_fd].buf)<902001)
				{
					write(requestP[conn_fd].conn_fd,error,strlen(error));
					close(requestP[conn_fd].conn_fd);
        				free_request(&requestP[conn_fd]);;
					continue;
				}
						if(read_lock(file_fd,atoi(requestP[a].buf)-902001,F_RDLCK)>0)
						{
							write(requestP[a].conn_fd,lock_notation,strlen(lock_notation));
						}else
						{
							lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
							Order temp[1];
							read(file_fd,temp,sizeof(Order));
							sprintf(buf,"You can order %d adult mask(s) and %d children mask(s).\n",temp[0].adultMask,temp[0].childrenMask);
							write(requestP[conn_fd].conn_fd, buf, strlen(buf));
						}
				unlock(file_fd,atoi(requestP[a].buf)-902001);			
				close(requestP[a].conn_fd);
				free_request(&requestP[a]);
			}


		}
	#else
		for(int a=0;a<maxfd;a++)
		{
			if(FD_ISSET(requestP[a].conn_fd,&working_set)){
				int ret=handle_read(&requestP[a]);
				if(ret<0)
				{
					fprintf(stderr, "bad request from %s\n", requestP[conn_fd].host);
		       			continue;	
				}			
				if(requestP[a].id==0)//buf鋆⊿?疳d
				{
					if(atoi(requestP[conn_fd].buf)>902020 || atoi(requestP[conn_fd].buf)<902001)
					{
						write(requestP[conn_fd].conn_fd,error,strlen(error));
						close(requestP[conn_fd].conn_fd);
        					free_request(&requestP[conn_fd]);;
						continue;
					}

					int status=0;
					for(int j=0;j<maxfd;j++)
					{
						if(requestP[j].id==atoi(requestP[a].buf))
						{
							status=2;
							break;
						}
					}
					if(write_lock(file_fd,atoi(requestP[a].buf)-902001,F_WRLCK)<0)
						status=2;
					if(status==2)
					{
						write(requestP[a].conn_fd,lock_notation,strlen(lock_notation));
						close(requestP[a].conn_fd);
						free_request(&requestP[a]);
						continue;
					}else
					{
						requestP[a].id=atoi(requestP[a].buf);
						lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
						Order temp[1];
						read(file_fd,temp,sizeof(Order));
						sprintf(buf,"You can order %d adult mask(s) and %d children mask(s).\n",temp[0].adultMask,temp[0].childrenMask);
						write(requestP[conn_fd].conn_fd, buf, strlen(buf));
						char write_notation[]="Please enter the mask type (adult or children) and number of mask you would like to order:\n";
						write(requestP[conn_fd].conn_fd,write_notation,strlen(write_notation));				
					}
				}else{//buf鋆⊿?暹?隞?
					if(strncmp(requestP[conn_fd].buf,"adult",5)==0){
					int number=atoi(requestP[conn_fd].buf+6);
					lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
					Order temp[1];
					read(file_fd,temp,sizeof(Order));
					if(number<=temp[0].adultMask && number >0){	
						lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
						temp[0].adultMask-=number;
						write(file_fd,temp,sizeof(Order));
						sprintf(buf,"Pre-order for %d successed, %d adult mask(s) ordered.\n",temp[0].id,number);
						write(requestP[conn_fd].conn_fd, buf, strlen(buf));			
					}else{
						write(requestP[conn_fd].conn_fd,error,strlen(error));
		        			close(requestP[conn_fd].conn_fd);
        					free_request(&requestP[conn_fd]);
 					}

				}else if(strncmp(requestP[conn_fd].buf,"children",8)==0){//children mask
					int number=atoi(requestP[conn_fd].buf+9);
					lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
					Order temp[1];
					read(file_fd,temp,sizeof(Order));
					if(number<=temp[0].adultMask && number >0){	
						lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
						temp[0].childrenMask-=number;
						write(file_fd,temp,sizeof(Order));
						sprintf(buf,"Pre-order for %d successed, %d children mask(s) ordered.\n",temp[0].id,number);
						write(requestP[conn_fd].conn_fd, buf, strlen(buf));
					}else{
						write(requestP[conn_fd].conn_fd,error,strlen(error));
	        				close(requestP[conn_fd].conn_fd);
        					free_request(&requestP[conn_fd]);
 					}

				}else
				{
					write(requestP[conn_fd].conn_fd,error,strlen(error));
	        			close(requestP[conn_fd].conn_fd);
        				free_request(&requestP[conn_fd]);
 					
				}
				unlock(file_fd,requestP[a].id-902001);

					close(requestP[a].conn_fd);
					free_request(&requestP[a]);
				}	
			}
		}//end for



	#endif


		//problems!!!
	//
/*int set_lock(int fd,int offset,int type){
	struct	flock lock;
	lock.l_type=type;
	lock.l_whence=SEEK_SET;
	lock.l_start=offset*sizeof(Order);
	lock.l_len=sizeof(Order);
	return fcntl(fd,F_SETLK,&lock);
}
int un_lock(int fd, int offset)
{
	struct flock lock;
	lock.l_type=F_UNLCK;
	lock.l_whence=SEEK_SET;
	lock.l_start=offset*sizeof(Order);
	lock.l_len=sizeof(Order);
	return fcntl(fd,F_SETLK,&lock);
}
		int a;
		for(a=0;a<maxfd;a++)
		{
		       if(FD_ISSET(requestP[a].conn_fd,&working_set)&requestP[a].conn_fd>=0){
		       
	
			conn_fd=a;
			int ret = handle_read(&requestP[conn_fd]); // parse data from client to requestP[conn_fd].buf
		       

			if (ret < 0) {
           			fprintf(stderr, "bad request from %s\n", requestP[conn_fd].host);
		       	continue;
       			}
		       
			if(atoi(requestP[conn_fd].buf)>902020 || atoi(requestP[conn_fd].buf)<902001)
			{
				write(requestP[conn_fd].conn_fd,error,strlen(error));
				close(requestP[conn_fd].conn_fd);
        			free_request(&requestP[conn_fd]);;
				continue;
			}
			int lock=0;
			for(int i=0;i<maxfd && i!=conn_fd;i++){
				if(requestP[i].id==atoi(requestP[conn_fd].buf))
				{
					FD_CLR(conn_fd,&master_set);
					write(requestP[conn_fd].conn_fd,lock_notation,strlen(lock_notation));
					close(requestP[conn_fd].conn_fd);
        				free_request(&requestP[conn_fd]);
					lock=1;
					break;
				}
			}
		       	if(lock==1)//no read or write since the same id
				continue;
// TODO: handle requests from clients
#ifdef READ_SERVER      

			requestP[a].id=atoi(requestP[a].buf);	
			for(int now=902001;now<=902020;now++)
			{
				if(now==requestP[a].id)
				{
					int status=set_lock(file_fd,requestP[conn_fd].id-902001,F_RDLCK);
					if(status<0)
					{
						FD_CLR(conn_fd,&master_set);
						write(requestP[conn_fd].conn_fd,lock_notation,strlen(lock_notation));
						close(requestP[conn_fd].conn_fd);
        					free_request(&requestP[conn_fd]);
						break;
					}else{
		
						lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
						Order temp[1];
						read(file_fd,temp,sizeof(Order));
						sprintf(buf,"You can order %d adult mask(s) and %d children mask(s).\n",temp[0].adultMask,temp[0].childrenMask);
						write(requestP[conn_fd].conn_fd, buf, strlen(buf));
						unlock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order));

							
					}
				}
			}
			
	
		/*	if(read_lock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order))>=0){
				lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
				Order temp[1];
				read(file_fd,temp,sizeof(Order));
				sprintf(buf,"You can order %d adult mask(s) and %d children mask(s).\n",temp[0].adultMask,temp[0].childrenMask);
				write(requestP[conn_fd].conn_fd, buf, strlen(buf));
				unlock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order));
			}else{
				FD_CLR(conn_fd,&master_set);
				write(requestP[conn_fd].conn_fd,lock_notation,strlen(lock_notation));
				close(requestP[conn_fd].conn_fd);
        			free_request(&requestP[conn_fd]);
				continue;
			}
#else 	
			

			if(requestP[conn_fd].id==0)//撠頛詨??蔗?賊?
			{
				requestP[conn_fd].id=atoi(requestP[a].buf);
				int lock=0;
				if(write_lock(file_fd,sizeof(Order)*(requestP[conn_fd].id-902001),SEEK_SET,sizeof(Order)<0)){
							lock=1;
				}
				if(lock==1)
				{
					FD_CLR(conn_fd,&master_set);
					write(requestP[conn_fd].conn_fd,lock_notation,strlen(lock_notation));
					close(requestP[conn_fd].conn_fd);
        				free_request(&requestP[conn_fd]);
					continue;
				}
				else
				{
					lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
					Order temp[1];
					read(file_fd,temp,sizeof(Order));
					sprintf(buf,"You can order %d adult mask(s) and %d children mask(s).\n",temp[0].adultMask,temp[0].childrenMask);
					write(requestP[conn_fd].conn_fd, buf, strlen(buf));
					char write_notation[]="Please enter the mask type (adult or children) and number of mask you would like to order:\n";
					write(requestP[conn_fd].conn_fd,write_notation,strlen(write_notation));
				}
			}else{
				ret = handle_read(&requestP[conn_fd]); // parse data from client to requestP[conn_fd].buf
				if (ret < 0) {
				    fprintf(stderr, "bad request from %s\n", requestP[conn_fd].host);
				    continue;
				}
				if(strncmp(requestP[conn_fd].buf,"adult",5)==0){
					int number=atoi(requestP[conn_fd].buf+6);
					lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
					Order temp[1];
					read(file_fd,temp,sizeof(Order));
					if(number<=temp[0].adultMask && number >0){	
						lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
						temp[0].adultMask-=number;
						write(file_fd,temp,sizeof(Order));
						sprintf(buf,"Pre-order for %d successed, %d adult mask(s) ordered.\n",temp[0].id,number);
						write(requestP[conn_fd].conn_fd, buf, strlen(buf));			
						unlock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order));
					}else{
						write(requestP[conn_fd].conn_fd,error,strlen(error));
		        			close(requestP[conn_fd].conn_fd);
        					free_request(&requestP[conn_fd]);
						unlock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order));
 					}

				}else{//children mask
					int number=atoi(requestP[conn_fd].buf+9);
					lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
					Order temp[1];
					read(file_fd,temp,sizeof(Order));
					if(number<=temp[0].adultMask && number >0){	
						lseek(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET);
						temp[0].childrenMask-=number;
						write(file_fd,temp,sizeof(Order));
						sprintf(buf,"Pre-order for %d successed, %d children mask(s) ordered.\n",temp[0].id,number);
						write(requestP[conn_fd].conn_fd, buf, strlen(buf));
						unlock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order));
					}else{
						write(requestP[conn_fd].conn_fd,error,strlen(error));
	        				close(requestP[conn_fd].conn_fd);
        					free_request(&requestP[conn_fd]);
						unlock(file_fd,(requestP[conn_fd].id-902001)*sizeof(Order),SEEK_SET,sizeof(Order));
 					}

				}


			}
	#endif
        				close(requestP[conn_fd].conn_fd);
        				free_request(&requestP[conn_fd]);
					FD_CLR(conn_fd,&master_set);
			
		       }//end FD_ISSET
		}//end of for
*/
	}else if(ok<=0)
		continue;
    }
    close(file_fd);
    free(requestP);
    return 0;
}

// ======================================================================================================
// You don't need to know how the following codes are working
#include <fcntl.h>

static void init_request(request* reqP) {
    reqP->conn_fd = -1;
    reqP->buf_len = 0;
    reqP->id = 0;
}

static void free_request(request* reqP) {
    /*if (reqP->filename != NULL) {
        free(reqP->filename);
        reqP->filename = NULL;
    }*/
    init_request(reqP);
}

static void init_server(unsigned short port) {
    struct sockaddr_in servaddr;
    int tmp;

    gethostname(svr.hostname, sizeof(svr.hostname));
    svr.port = port;

    svr.listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (svr.listen_fd < 0) ERR_EXIT("socket");

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(port);
    tmp = 1;
    if (setsockopt(svr.listen_fd, SOL_SOCKET, SO_REUSEADDR, (void*)&tmp, sizeof(tmp)) < 0) {
        ERR_EXIT("setsockopt");
    }
    if (bind(svr.listen_fd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0) {
        ERR_EXIT("bind");
    }
    if (listen(svr.listen_fd, 1024) < 0) {
        ERR_EXIT("listen");
    }

    // Get file descripter table size and initize request table
    maxfd = getdtablesize();
    requestP = (request*) malloc(sizeof(request) * maxfd);
    if (requestP == NULL) {
        ERR_EXIT("out of memory allocating all requests");
    }
    for (int i = 0; i < maxfd; i++) {
        init_request(&requestP[i]);
    }
    requestP[svr.listen_fd].conn_fd = svr.listen_fd;
    strcpy(requestP[svr.listen_fd].host, svr.hostname);

    return;
}
