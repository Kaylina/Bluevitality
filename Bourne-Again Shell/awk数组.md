#### 数组
```bash
# awk是按行处理文本数据的，将1行为1个记录；1个记录还可依分隔符变量"FS"来分隔为若干字段
# awk数组叫做关联数组，因为下标可是数也可是串。awk中数组不必提前声明，也不必声明大小...
# awk多维数组在本质上是一维数组，更确切的说，它在存储上并不支持多维数组。但其提供了逻辑上模拟2维数组的方式
# 例如：array[2,4]=1 这样的访问是允许的（多维数组成员测试可使用 if( (i,j) in array ) 的形式）


#Example：
#取数组长度(length返回值为串的数组长度，split分割字串为数组，格式：length(string,arry,"fs"))
[root@localhost ~]# awk 'BEGIN{info="it is a test";lens=split(info,tA," ");print length(tA),lens;}'
4 4

#asort对数组进行排序并且返回数组长度，格式：asort(arry)
[root@localhost ~]# awk 'BEGIN{info="it is a test";split(info,tA," ");print asort(tA);}'
4

#无序输出数组内容
[root@localhost ~]# awk 'BEGIN{info="it is a test";split(info,A," ");for(i in A){print i,A[i]}}'      
4 test
1 it
2 is
3 a

#有序输出数组内容（数组下标从1开始，与c不同）
[root@localhost ~]# awk 'BEGIN{info="it is a test";len=split(info,A," ");for(i=1;i<=len;i++){print i,A[i]}}'            
1 it
2 is
3 a
4 test


[root@localhost ~]# awk 'BEGIN{
>     for(i=1;i<=3;i++)
>     {
>         for(j=1;j<=3;j++)  
>         {
>             tarr[i,j]=i*j;
>             print i,"*",j,"=",tarr[i,j];
>         }
>     }
> }'
1 * 1 = 1
1 * 2 = 2
1 * 3 = 3
2 * 1 = 2
2 * 2 = 4
2 * 3 = 6
......

#判断关联数组中是否存在指定的下标元素（删除下标时，要使用 "delete Arry["index"]" 的形式）
[root@localhost ~]#  awk 'BEGIN{tB["a"]="a1";tB["b"]="b1";if( "a" in tB){print "have"}}'
have

[root@localhost ~]# cat 1
111 abc  def abc 
222 ddd  sss klm 
333 efg  xyz ddd 
abc ddd  sss klm
[root@localhost ~]#  awk '{ w[$2]+=1 } END { for (a in w) print a,w[a]}' 1  #统计第二个字段的重复次数
abc 1
efg 1
ddd 2
[root@localhost ~]# < 1 awk '$2=="ddd" {i=i+1} END {print i}'       #统计"ddd"出现的次数
[root@localhost ~]# < 1 awk '{if($2=="ddd") i=i+1} END {print i}'   #统计"ddd"出现的次数
[root@localhost ~]# < 1 awk '$2 ~ /ddd/{++i}END{print i}'           #统计"ddd"出现的次数

```
