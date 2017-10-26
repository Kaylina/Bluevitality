[root@localhost ~]# cat test.sh 
#!/bin/bash

exec ${@}
[root@localhost ~]# bash test.sh ls -lh
总用量 4.0K
-rw-r--r-- 1 root root 23 8月  15 10:47 test.sh
