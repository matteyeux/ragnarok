CC = gcc

python3v = $(shell python3 --version | cut -d . -f 2 | tr -d '\n')
python3m = $(shell python3 --version | cut -d . -f 2 | tr -d '\n ' && echo "m")

all : run_python send_xml sql_db

run_python : run_python.c
	$(CC) $< -I/usr/include/python3.$(python3v) -Wall -g -o $@ -lpython3.$(python3m)

send_xml : send_xml.c
	$(CC) $< -o $@

sql_db : sql_db.c
	$(CC) $< -I/usr/include/mysql -o $@ -lmysqlclient -lpthread -lz -lrt -ldl 
clean :
	rm -rf run_python send_xml sql_db
