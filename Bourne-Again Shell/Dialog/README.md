```bash
#!/bin/bash
yesno() {
 dialog --title "First screen" --backtitle "Test Program" --clear --yesno \
 "Start this test program or not ? \nThis decesion have to make by you. " 16 51
 # yes is 0, no is 1 , esc is 255
 result=$?
 if [ $result -eq 1 ] ; then
 exit 1;
 elif [ $result -eq 255 ]; then
 exit 255;
 fi
 username
}
username() {
 cat /dev/null >/tmp/test.username
 dialog --title "Second screen" --backtitle "Test Program" --clear --inputbox \
 "Please input your username (default: hello) " 16 51 "hello" 2>/tmp/test.username
 result=$?
 if [ $result -eq 1 ] ; then
 yesno
 elif [ $result -eq 255 ]; then
 exit 255;
 fi
 password
}
password() {
 cat /dev/null >/tmp/test.password
 dialog --insecure --title "Third screen" --backtitle "Test Program" --clear --passwordbox \
 "Please input your password (default: 123456) " 16 51 "123456" 2>/tmp/test.password
 result=$?
 if [ $result -eq 1 ] ; then
 username
 elif [ $result -eq 255 ]; then
 exit 255;
 fi
 occupation
}
occupation() {
 cat /dev/null >/tmp/test.occupation
 dialog --title "Forth screen" --backtitle "Test Program" --clear --menu \
 "Please choose your occupation: (default: IT)" 16 51 3 \
 IT "The worst occupation" \
 CEO "The best occupation" \
 Teacher "Not the best or worst" 2>/tmp/test.occupation
 result=$?
 if [ $result -eq 1 ] ; then
 password
 elif [ $result -eq 255 ]; then
 exit 255;
 fi
 finish
}
finish() {
 dialog --title "Fifth screen" --backtitle "Test Program" --clear --msgbox \
 "Congratulations! The test program has finished!\n Username: $(cat /tmp/test.username)\n Password: $(cat /tmp/test.password)\n Occupation: $(cat /tmp/test.occupation)" 16 51
 result=$?
 if [ $result -eq 1 ] ; then
 occupation
 elif [ $result -eq 255 ]; then
 exit 255;
 fi
}
yesno
```
