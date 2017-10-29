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
