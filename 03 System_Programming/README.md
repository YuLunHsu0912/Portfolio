# System Programming
In this part, three systems are implemented with the aid of pipe, fifo, signals, multiplexing. Details are discussed in each project.

The work is coupled with the course System programming in NTU csie.
## Auction system
We have  implemented an auction system which handles a number of auctions simultaneously.

## Mak pre-order system
The csieMask system is composed of read and write servers, both can access a file preorderRecord that records infomation of consumer's order. When a server gets a request from clients, it will response according to the content of the file. A read server can tell the client how many masks can be ordered. A write server can modify the file to record the orders.
## Pseudothread
In this part, we simulate a user-thread library by using longjmp(), setjmp(), etc. For simplicity, we use a function to represent a thread. In other words, "context switch" happens between functions. To do this, we use non-local jumps between functions, which is arranged by a scheduler(): each time a function needs to "context switch" to another, it needs to jump back to scheduler(), and scheduler() will schedule next function to be executed, thus jump to it. Since non-local jump won't store local variables, we define a data structure for each function to store data needed for computing, which is called TCB_NODE. All the TCB_NODEs will formulate a circular linked-list. As scheduler() schedules functions, it also needs to make sure Current pointer points to correct TCB_NODE for functions to output correct result.
