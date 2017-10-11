git执行流程：
> **工作区** ---> **暂存区** ---> **版本库** ---> **远程仓库**  
> Git中文件的三种状态：已修改（还未add到Index）---> 已暂存（所有的修改还未提交）---> 已提交（存在版本库中）  
> HEAD：这是当前分支版本顶端的别名，即在当前分支最近的一个提交  
> Index：暂存区是指一套将被提交的文件集合。他也是将成为HEAD的的那个commit  

   
生成SSH密钥对：   
`ssh-keygen -t rsa -C "youremail@example.com"`   
   
环境设置：    
选项 --global：用户全局，--system：系统全局，--local：仅针对当前项目   
针对特定作用范围的conf文件直接进行编辑：   
`git config -e [--global | --system | --local]`   
   
设置用户信息：（用户信息位于 ~/.gitconfig ，若 --system 则位于 /etc/gitconfig，工作目录的 .git/conf 仅当前项目生效）  
`git config --global user.name "bluevitality"`  
`git config --global user.email "inmoonlight@163.com"`  
设置默认的编辑器：  
`git config --system core.editor vim`  
设置差异分析工具：  
`git config --system merge.tool vimdiff`  
别名代替常用命令：  
`git config --global alias.st status`  
查看配置信息：  
`git config --list`  
  
初始化当前项目目录：（生成版本库 ---> .git）  
`git init .`  
在git服务端创建无工作区的裸仓库：  
`git init --bare workspace.git`  
克隆远程仓库到本地：（如需指定本地的项目根目录名称则在后面添加目录名即可：git clone Url Path ）  
`git clone git@github.com/bluevitality/xxxxx.git`  

隐藏当前现场处理其他任务：（即保存当前工作区与暂存区的状态）  
`git stash`  
查看隐藏的现场列表：  
`git stash --list`  
恢复or删除现场：  
`git stash [apply | drop]`  
回到隐藏现场的分支后恢复并删除保存的现场并继续处理：  
`git stash pop`  
  
将工作区改变的文件数据添加到暂存区：（在对文件完成修改操作后执行）  
`git add filename`  
`git add .` 或：`git add *`   
将工作区改变的文件数据添加到暂存区：（包括删除对象的操作，默认仅添加修改或新增的对象）  
`git add --all` 或： `git add -A`   
对文件改名：（相当于执行 mv .. .. ; git rm .. ; git add ..）  
`git mv oldname newname`  
删除文件：（若要删除已修改并提交到暂存区的文件则去添加参数 -f）  
`git rm filename`  
删除暂存区的文件用于停止对其跟踪：  
`git rm --cached filename`  
恢复误删的文件：（若修改后还未执行add则将指定文件返回至版本库的最新状态，若已添加至暂存区后又进行了   则将其回退至add时最初的暂存区保存的状态，即让文件回退至最近的一次commit或add后的状态）  
`git checkout -- filename`  
用HEAD所指向的分支的全部或部分文件来替换暂存区和工作区：  
`git checkout HEAD [. | filename]`  
与git add命令合并为一条命令并提交到本地仓库：    
`git commit -a -m "commit info.."`    
将当前本暂存区要提交的信息与上一次的提交并为**1**个提交（若暂存区未发生改变则相当于重写了提交信息）     
`git commit --amend -m "add fix ...."`    
添加远程仓库设置别名为"origin"：（删除远程仓库使用：**git remote rm xxx**）    
`git remote add origin git@github.com/bluevitality/xxxxx.git`  
查看远程仓库"origin"的信息：    
`git remote show origin`  

将本地的master分支提交到origin远程仓库：  
`git push origin master`  
将本地other分支的内容推送到远程仓库origin的master分支：  
`git push origin other:master`  
建立本地分支和远程分支的关联：  
`git branch --set-upstream 本地分支名 origin/远程分支名`  

修改远程仓库名称：  
`git remote rename Oldname Newname`  
从远程仓库拉取本地仓库还没有的数据：（fetch仅拉取远端数据到本地而不合并，需手工进行合并）  
`git fetch origin`  
将从远程仓库fetch下来的数据与当前分支进行合并操作：  
`git merge origin/master`  
从远程仓库拉取本地仓库还没有的数据并且进行合并操作！  
`git pull origin master`  
新建并切换到一个分支：（相当于两条命令：**git branch Name ; git checkout Name**）  
`git checkout -b Name`   
合并特定分支到当前分支：（建议增加 ** --no-ff** 参数，使得执行快速合并时历史记录中仍保留此分支的信   
`git merge --no-ff Name`  
用户A在本地创建和远程分支对应的分支：  
`git checkout -b other origin/other`  
用户B设置本地分支与远程分支的对应关系：  
`git branch --set-upstram othser osrigin/other`  
查看本地及远程仓库的分支信息：（参数-v附加显示各分支的最后一次提交信息，若仅查看远程仓库信息则使用-r参数）  
`git branch -av`  
删除分支：（未进行合并时需要使用强制删除参数-D）  
`git branch -d Name`  
在本地创建一个分支后推送到远程仓库：  
`git checkout -b BName  ;  git push BName origin:BName`  
删除远程仓库分支：(下面的命令是推送空分支到远程，即为删除操作，严格来说应该执行：**git push origin    ete   Bname**)     
`git push origin :Bname`     
查看哪些分支已经并入了当前的分支中：（若不需要保留可用**git branch -d Name**进行删除）     
`git branch --merged`     
查看尚未进行合并的分支：（删除未合并的分支时应使用branch的大写 -D 参数）     
`git branch --no-merged`     
查看暂存区与工作区间的状态：     
`git status`     
   
查看提交历史：（-n 使用**数字**作为参数则仅显示最近的几次提交信息）     
`git log  --pretty=oneline --pretty=format:"%h %ad :%s" --graph`     
查看最近三次的提交记录：   
`git log --prrety=oneline -3`   
   
*默认情况下创建的标签仅存在于 **本地仓库***     
若需要推送到远程需设置：（即：将平时提交时需指定的分支改为标签名称）     
`git push origin TagName` 或一次性推送所有标签： `git push origin --tags`     
若标签已推到远程，要删除远程标签则麻烦一点，首先先从本地删除：     
`git tag -d v1.0` 再从远程删除： `git push origin :refs/tags/v1.0`     
针对当前分支的最新commit提交创建一个标签：     
`git tag v1.0`     
查看标签信息：（仅查看v1系列的标签：git tag -l "v1."）     
`git tag`     
针对提交历史中特定提交打标签：     
`git tag v2.0 6723TUYG`     
查看标签的指定的commit的提交信息：     
`git show v2.0`     
对标签详细设置其名字及说明以便区分：     
`git tag -a v3.0 -m "tag info..." 3a1f237`     
删除特定标签：     
`git tag -d v1.0`    
   
用版本库中的文件替换暂存区中的文件：   
`git reset HEAD -- filename`   
版本库，暂存区，工作区全部一致，撤回到某个提交点：   
`git reset --hard 578IF734F`   
清空添加到暂存区的内容：   
`git reset .`或：`git reset HEAD`   
撤出暂存区中指定的文件：（相当于git add的反操作）   
`git reset filename`或：`git reset HEAD filename`   
撤销暂存区中的修改，回退到工作区：     
`git reset HEAD filename`   
回退到最新的提交版本：   
`git reset --hard HEAD`   
回退到之前的第二个版本：     
`git reset --hard HEAD^`   
回退到之前的第100个版本：   
`git reset --hard HEAD~100`   
回退到指定的提交：   
`git reset --hard 578IF734F`     
撤销刚才的提交：   
`git reset --soft HEAD^`   
模拟amend提交（覆盖上一次的提交）：   
`git reset --soft HEAD^ ; git -a -m "amend...."`   
   
查看版本库中最新的文件与工作区的文件的区别：（HEAD指针永远指向当前分支的最后一次提交）     
`git diff HEAD -- filename`     
查看尚未暂存文件的改变：（即尚未暂存的改动）     
`git diff`     
查看已暂存的文件与上次提交的差异：     
`git diff --cached`   
   
查看哪些文件/目录将被删除：   
`git clean -nd`   
清除工作区中未加入版本库的文件/目录：   
`git clean -fd`   
   
   
