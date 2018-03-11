#include <stdio.h>
#include <stdarg.h>
#include <Python.h>
#include <stdbool.h>
#include <libxml/parser.h>
#include <libxml/tree.h>

#include <include/common.h>

#ifdef DEBUG
static FILE* dbg = NULL;
#endif

void version(){
	#ifdef DEBUG
		fprintf(stdout, "%s, version %s-DEBUG\nCompiled on %s at %s\nCopyright 2018 - White Wolf Team\n", TOOLNAME, VERSION, __DATE__, __TIME__);
	#else
		fprintf(stdout, "%s, version %s\nCompiled on %s at %s\nCopyright 2018 - White Wolf Team\n", TOOLNAME, VERSION, __DATE__, __TIME__);
	#endif
}

/*
*	We call this function almost everywhere
*	But it prints to stdout/stderr only
*	when you build the project in DEBUG mode
*	for the moment
*/
void debug(const char* format, ...) {
	#ifdef DEBUG
	va_list vargs;
	va_start(vargs, format);
	vfprintf((dbg) ? dbg : stderr,format, vargs);
	va_end(vargs);
	#endif
}

/*
*	This functions checks if a file exists
*	returns TRUE if exists
*	in the other case it returns FALSE.
*	param is the name of the file
*/
bool file_exists(const char* file){
	if(access(file, F_OK ) != -1) {
		return true;
	} else {
		return false;
	}
}

/*
*	Call a Python script with this function
*	param is the python script you want to run
*	We use Python3
*/
int run_python(const char *pyscript){
	Py_Initialize();
	FILE* file = fopen(pyscript, "r");
	if (!file_exists(pyscript))
	{
		fprintf(stderr, "%s: %s\n", pyscript, strerror(errno));
		return -2;
	}
	PyRun_SimpleFile(file, pyscript);
	Py_Finalize();
	return 0;
}


/*
*	function to get date and time
*	type is char * it returns a pointer:
*	curr_time
*	TODO : find a better to print use date
*	and time for server
*/

char *get_date_and_time(void)
{
	time_t local_time;
	struct tm * tm;
	char *curr_time;
	curr_time = malloc(sizeof(char) *30);
	time(& local_time);
	tm = localtime(& local_time);
	sprintf(curr_time, "%02d/%02d/%02d-%02d:%02d:%02d", tm->tm_mday, tm->tm_mon + 1, tm->tm_year % 100, tm->tm_hour, tm->tm_min, tm->tm_sec);
	return (char *)curr_time;
}
/*
*	function to find text between 2 strings
*	returns found text
*	str = default string
* 	p1 = first pattern
*	p2 = scnd pattern to search between
*	https://stackoverflow.com/a/24696896/9299410
*/
char *get_txt(const char *str, const char *p1, const char *p2){
	char *target = NULL;
	char *start, *end;

	if ((start = strstr(str, p1))) {
		start += strlen(p1);
		if ((end = strstr(start, p2)))
		{
			target = (char *)malloc(end - start + 1);
			memcpy(target, start, end - start);
			target[end - start] = '\0';
		}
	}

	if (target)
		return (char *)target;
	else 
		return NULL;
}

xmlDocPtr doc = NULL;
xmlNodePtr root = NULL, device_AP_name = NULL, info_ap = NULL, info_ap_nb = NULL;
xmlNodePtr device_AP_name_child = NULL, info_ap_child = NULL;

void init_xml(char *docname){
	doc = xmlNewDoc(BAD_CAST "1.0");
	root = xmlNewNode(NULL, BAD_CAST docname);
	xmlDocSetRootElement(doc, root);
	/* create two childs we will deal with */
	device_AP_name = xmlNewChild(root, NULL, BAD_CAST "rpi_info", NULL);
	info_ap = xmlNewChild(root, NULL, BAD_CAST "info_AP", NULL);
}

void end_xml(char *docname){
	/* 	this commented line can output the XML file to stdout
	* 	I keep it for debugging purposes
	*/
	// xmlSaveFormatFileEnc("-", doc, "UTF-8", 1);
	xmlSaveFormatFileEnc(docname, doc, "UTF-8", 1);
	xmlFreeDoc(doc);
}