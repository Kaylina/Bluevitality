#### 说明
```txt
JSON是一种取代XML的数据结构,和xml相比,它更小巧,由于它的小巧所以网络传输数据将减少更多流量从而加快速度。 
JSON就是一串字符串 只不过元素会使用特定的符号标注。 
  {} 双括号表示对象 
  [] 中括号表示数组 
  
""  双引号内是属性或值 
:   冒号表示后者是前者的值(这个值可以是字符串、数字、也可以是另一个数组或对象) 

所以 {"name": "beck"} 可以理解为是一个包含name为beck的对象 
而[{"name": "beck"},{"name": "rooney"}]就表示包含两个对象的数组 

当然了,你也可以使用{"name":["beck","rooney"]}来简化上面一部,这是一个拥有一个name数组的对象。 
为什么{name:'json'}在检验时通过不了? ---> JSON官网最新规范规定“键”或者“值”都需要用双引号来表示。 
```
#### Example
```json
{  
    "root": [  
        {  
            "workDay": "1",  
            "productType": "ZT4",  
            "customBatch": "",  
            "destination": "020"  
        },  
        {  
             "workDay": "7",  
             "productType": "ZT4",  
             "customBatch": "",  
             "destination": "020"  
         }]  
}  
```
#### jq
```bash
# 对于JSON格式而言，jq就像sed/awk/grep这些神器一样的方便，而也，jq没有乱七八糟的依赖，只需要一个binary文件jq，就足矣。

[root@localhost ~]# cat txt
{"name":"Google","location":{"street":"1600 Amphitheatre Parkway","city":"Mountain View","state":"California","country":"US"},"employees":[{"name":"Michael","division":"Engineering"},{"name":"Laura","division":"HR"},{"name":"Elise","division":"Marketing"}]}
[root@localhost ~]# cat txt | jq .      #解析JSON并格式化
{
  "name": "Google",
  "location": {
    "street": "1600 Amphitheatre Parkway",
    "city": "Mountain View",
    "state": "California",
    "country": "US"
  },
  "employees": [
    {
      "name": "Michael",
      "division": "Engineering"
    },
    {
      "name": "Laura",
      "division": "HR"
    },
    {
      "name": "Elise",
      "division": "Marketing"
    }
  ]
}
[root@localhost ~]# cat txt | jq '.employees[1].name'     #根据Key解析Value
"Laura"
[root@localhost ~]# echo '{"foo": 42, "bar": "less interesting data"}' | jq .nofoo  #解析不存在的元素会返回空
null
cat json_raw.txt | jq 'keys'  #使用内建函数"keys"来解析并列出所有KEY
[
  "employees",
  "location",
  "name"
]
[root@localhost ~]# cat txt | jq 'has("name")'    #查询是否存在指定的key，注意格式不要写错！....
true

#使用Python自带模块"json.tool"进行解析
[root@localhost ~]# python -m json.tool txt
{
    "employees": [
        {
            "division": "Engineering",
            "name": "Michael"
        },
        {
            "division": "HR",
            "name": "Laura"
        },
        {
            "division": "Marketing",
            "name": "Elise"
        }
    ],
    "location": {
        "city": "Mountain View",
        "country": "US",
        "state": "California",
        "street": "1600 Amphitheatre Parkway"
    },
    "name": "Google"
}
```
