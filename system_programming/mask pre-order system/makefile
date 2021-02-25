all:write_server read_server
write_server : server.c 
	gcc -o write_server server.c
read_server : server.c
	gcc -o read_server server.c -D READ_SERVER

