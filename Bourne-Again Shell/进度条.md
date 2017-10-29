#### eg1
```bash
#!/bin/bash

sleepa(){
	b=''
	for ((i=100;$i>=0;i-=2))
	do
	    printf "等待中:[%-50s]\r" $b 
	    sleep 0.1
	    b==$b
	done
	echo
}
sleepa
# 效果：     等待中:[==================                           ]
```

#### eg2
```bash
#!/bin/bash

function Loading()
{
        b=''
        for ((i=100;$i>=0;i-=2))
        do
            #左对齐宽度五十，每次执行一个空格
            printf "Loading:[%-${1}s]\r" $b

            #暂停
            sleep 0.06

            #任务完成时在原来基础上加"="
            b==$b


        done
        echo
}

Loading 50 #传参，50是指进度条宽度
```
#### eg3
```bash
#!/bin/bash

b=''
num=0
while [ $num -le  100 ]
do
    printf "process:[%-50s] %d%% \r" $b $num
    sleep 0.1
    num=`expr $num + 2`
    b=#$b
done
echo
```
#### 转动效果
```bash
#!/bin/bash
i=0
while [ $i -lt 20 ]
do
  for j in '-' '\' '|' '/'
    do
      printf "intel testing : %s\r" $j
      sleep 0.1
      ((i++))
    done
done

```
