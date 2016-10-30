start java -jar selenium-server-standalone-2.53.1.jar -role hub
start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5555 -browser browserName=phantomjs,platform=WINDOWS
start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5556 -browser browserName=phantomjs,platform=WINDOWS
start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5557 -browser browserName=phantomjs,platform=WINDOWS
start java -jar selenium-server-standalone-2.53.1.jar -role node -port 5558 -browser browserName=phantomjs,platform=WINDOWS

