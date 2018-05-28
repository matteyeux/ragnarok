#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# @file xmlparser.py
# @brief Parse XML file to put info in the ragnarok database
#

import mysql.connector
import xml.etree.ElementTree 
import sys

## Function : insert_info_ap
# Function used to insert Wifi access point information in the database
# @param db_conn
# @param mac
# @param essid
# @param time
# @param id_encryption
# @param channel
# @param beacon
# @param signal
# @param frequency
# @param id_quality
# @param MAC_Rasb
def insert_info_ap(db_conn, mac, essid, time, encryption, channel, beacon, signal, frequency, quality, MAC_Rasb): 
	curs = db_conn.cursor() 
	sql = "INSERT INTO Info_AP VALUES (NULL,'%s', '%s', '%s', (SELECT Id_encryption FROM Encryption WHERE Encryption.Encryption_name = '%s'), '%s', '%s', '%s', '%s', '%s', '%s');" % \
		(mac, essid, time, encryption, channel, beacon, signal, frequency, quality, MAC_Rasb)
	curs.execute(sql)

## Function : insert_device_info
# Function used to insert client information in the database
# @param db_conn
# @param time
# @param mac
# @param ip
def insert_device_info(db_conn, time, mac, ip):
	curs = db_conn.cursor()
	sql = "INSERT INTO Device_info VALUES ('%s', '%s', '%s');" % \
		(time, mac_rasb, ip)  
	curs.execute(sql)

## Function : insert_encryption
# Function used to insert encryption information in the database
# @param db_conn
# @param Encryption_name
def insert_encryption(db_conn, Encryption_name):
	curs = db_conn.cursor()
	sql1 = "INSERT INTO Encryption VALUES (NULL,'%s');" % (Encryption_name)
	sql2 = "SELECT COUNT(Encryption_name) FROM Encryption WHERE Encryption_name='%s';" % (Encryption_name)
	curs.execute(sql2)
	rows = curs.fetchone()
	nbligne = rows[0]
	print (nbligne)
	if nbligne == 0:
		curs.execute(sql1)
	else:
		pass


## Function : ap_data_from_element
# Parse data in the XML file
# @param info_AP
# @param info_rasb
def ap_data_from_element(info_AP, info_rasb):
	mac = info_AP.find("mac").text
	essid = info_AP.find("essid").text
	channel = info_AP.find("channel").text
	beacon = info_AP.find("last_beacon").text
	quality = info_AP.find("quality").text
	signal = info_AP.find("signal").text
	frequency = info_AP.find("frequency").text
	time = info_rasb.find("time").text
	mac_rasb = info_rasb.find("mac").text
<<<<<<< HEAD
	encryption = info_AP.find("encryption").text
	ip = info_rasb.find("IP").text
=======

	if info_AP.find("encryption") == None:
		encryption = "None"
	else :
		encryption = info_AP.find("encryption").text
>>>>>>> upstream/master


	return mac, channel, frequency, quality, signal, essid, beacon, encryption, time, mac_rasb,ip

def parse(xmlfile):
	conn = mysql.connector.connect(host="localhost", user="root", password="root", database="ragnarok_bdd")
	ragnarok = xml.etree.ElementTree.parse(xmlfile)
	APs = ragnarok.findall("info_AP")
	RASBs = ragnarok.find("rpi_info")

	return APs, RASBs, conn


## Function : usage
# usage function
def usage():
	print("usage : %s <file>" % sys.argv[0])


if __name__ == '__main__':
	if len(sys.argv) != 4 :
		usage()
		sys.exit(1)
	else :
<<<<<<< HEAD
		xmlfile1 = sys.argv[1]
		xmlfile2 = sys.argv[2]
		xmlfile3 = sys.argv[3]

	APs, RASBs, conn = parse(xmlfile1)


	for AP in APs:
		mac, channel, frequency, quality, signal, essid, beacon, encryption, time, mac_rasb, ip = ap_data_from_element(AP,RASBs)
		insert_encryption(conn, encryption)
		conn.commit()
		insert_info_ap(conn, mac, essid, time, encryption, channel, beacon, signal, frequency, quality, mac_rasb)
		conn.commit()

	insert_device_info(conn, time, mac_rasb, ip)
	conn.commit()


	APs, RASBs, conn = parse(xmlfile2)
	for AP in APs:
		mac, channel, frequency, quality, signal, essid, beacon, encryption, time, mac_rasb = ap_data_from_element(AP,RASBs)
		insert_encryption(conn, encryption)
		conn.commit()
		insert_info_ap(conn, mac, essid, time, encryption, channel, beacon, signal, frequency, quality, mac_rasb)
		conn.commit()
	insert_device_info(conn, time, mac_rasb, ip)
	conn.commit()


	APs, RASBs, conn = parse(xmlfile3)
	for AP in APs:
		mac, channel, frequency, quality, signal, essid, beacon, encryption, time, mac_rasb = ap_data_from_element(AP,RASBs)
		insert_encryption(conn, encryption)
		conn.commit()
		insert_info_ap(conn, mac, essid, time, encryption, channel, beacon, signal, frequency, quality, mac_rasb)
		conn.commit()
	insert_device_info(conn, time, mac_rasb, ip)
	conn.commit()
=======
		xmlfiles = sys.argv

	for i in range(1, len(xmlfiles)):
		APs, RASBs, conn = parse(xmlfiles[i])

		# foreignkey(conn)
		# conn.commit()

		for AP in APs:
			mac, channel, frequency, quality, signal, essid, beacon, encryption, time, mac_rasb = ap_data_from_element(AP,RASBs)
			insert_encryption(conn, encryption)
			conn.commit()
			insert_info_ap(conn, mac, essid, time, encryption, channel, beacon, signal, frequency, quality, mac_rasb)
			conn.commit()
			# defqual1(conn,mac_rasb,mac,quality)
			# conn.commit()
		insert_device_info(conn, time, mac_rasb, 0)
		conn.commit()

		# qual1,qual2,qual3 = 1,2,3
		# insert_quality(conn,qual1,qual2,qual3)
		# conn.commit()
>>>>>>> upstream/master
