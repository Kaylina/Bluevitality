GRANT ALL ON *.* TO 'root'@'192.168.1.%' IDENTIFIED BY 'pass123';
GRANT USAGE ON *.* to 'user'@'192.168.1.%' IDENTIFIED BY 'pass123';
GRANT ALL PRIVILEGES on *.* to 'user'@'192.168.1.%';
FLUSH PRIVILEGES;
GRANT ALL ON *.* TO 'root'@'192.168.2.1' IDENTIFIED BY 'pass123';
GRANT USAGE ON *.* to 'user'@'192.168.2.1' IDENTIFIED BY 'pass123';
GRANT ALL PRIVILEGES on *.* to 'user'@'192.168.2.1';
FLUSH PRIVILEGES;
#for haproxy
INSERT INTO mysql.user (Host,User) values ('192.168.1.%','cluster_check');
FLUSH PRIVILEGES;
