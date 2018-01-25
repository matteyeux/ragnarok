#include <stdio.h>
#include <signal.h>

/* local headers */
#include <include/server.h>
#include <include/server_tool.h>
#include <include/common.h>

int main(void){
	signal(SIGINT, INThandler);
	run_python("src/python/test.py");
	debug("starting server...\n");
	tcp_server("12345");
	return 0;
}
