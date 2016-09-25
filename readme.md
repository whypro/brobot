
	start java -jar selenium-server-standalone-2.53.1.jar -role hub
	
	start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5555 -hub http://localhost:4444/grid/register
	start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5556
	start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5557
	start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5558


