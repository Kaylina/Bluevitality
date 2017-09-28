git执行流程：
> **工作区** ---> **暂存区** ---> **版本库** ---> **远程仓库**

生成公私钥：
`ssh-keygen -t rsa -C "youremail@example.com"`  

全局设置：  
设置默认的编辑器：  
`git config --system core.editor vim`
设置差异分析工具：
`git config --system merge.tool vimdiff`
命令别名"st"代替status：
`git config --global alias.st status`
设置用户信息：（位于 ~/.gitconfig 下，若使用 --system 则位于 /etc/gitconfig，工作目录的 .git/config 仅对当前项目生效）
`git config --global user.name "bluevitality"`
`git config --global user.email "inmoonlight@163.com"`
查看配置信息：
`git config --list`

初始化当前项目目录：（生成 .git）
`git init .`
克隆远程仓库到本地：（如需指定本地的项目根目录名称则在后面添加目录名即可：git clone Url Path ）
`git clone git@github.com/bluevitality/xxxxx.git`
在git服务器端创建一个没有工作区的裸仓库：
`git init --bare workspace.git`
隐藏当前现场处理其他任务：（即保存当前工作区与暂存区的状态）
`git stash`
查看隐藏的现场列表：
`git stash --list`
回到隐藏现场的分支后恢复现场继续处理未完成任务：
`git stash pop`

将工作区改变的文件数据添加到暂存区：（在对文件完成修改操作后执行）
`git add filename`
`git add .`
`git add *`

对文件改名：（相当于执行了 *mv .. .. ; git rm .. ; git add ..*）
`git mv oldname newname`
删除文件：（若要删除已修改并提交到暂存区的文件则去添加参数-f）
`git rm filename`
删除暂存区的文件，停止对其跟踪：
`git rm --cached filename`
恢复误删的文件：（一键还原，从版本库中恢复）
`git checkout -- filename`

将工作区改变的文件数据添加到暂存区：（包括删除对象的操作，默认仅添加修改或新增的对象）
`git add --all` 或： `git add -A`
与git add命令合并为一条命令并提交到本地仓库：
`git commit -a -m "commit info.."`
将本暂存区要要提交的信息与最后一次的提交并为一个提交（若暂存区未发生改变也相当于重写了提交信息）
`git commit --amend -m "add fix ...."`
添加远程仓库设置别名为"origin"：（删除远程仓库使用：**git remote rm xxx**）
`git remote add origin git@github.com/bluevitality/xxxxx.git`
提交到远程仓库origin的master分支：（参数**-u**可将本地的分支与远程分支关联）
`git push -u origin master`
将本地other分支的内容推送到远程的master分支：
`git push origin other:master`
查看远程仓库信息：
`git remote show origin`
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
合并特定分支到当前分支：（建议增加 **--no-ff** 参数，使得执行快速合并时历史记录中仍保留此分支的信息）
`git merge --no-ff Name`
用户A在本地创建和远程分支对应的分支：
`git checkout -b other origin/other`
用户B设置本地分支与远程分支的对应关系：
`git branch --set-upstram othser osrigin/other`
查看本地及远程仓库的分支信息：（参数-v附加显示各分支的最后一次提交信息，若仅查看远程仓库信息则使用**-v**参数）
`git branch -av`
删除分支：（未进行合并时需要使用强制删除参数**-D**）
`git branch -d Name`
在本地创建一个分支后推送到远程仓库：
`git checkout -b BName  ;  git push BName origin:BName`
删除远程仓库分支：(下面的命令是推送空分支到远程，即为删除操作，严格来说应该执行：**git push origin --delete Bname**)
`git push origin :Bname`
查看哪些分支已经并入了当前的分支中：（若不需要保留可用**git branch -d Name**进行删除）
`git branch --merged`
查看尚未进行合并的分支：（删除未合并的分支时应使用branch的大写**-D**参数）
`git branch --no-merged`
查看暂存区与工作区间的状态：
`git status`

*默认情况下创建的标签仅存在于 **本地仓库***
若需要推送到远程需设置：（即：将平时提交时需指定的分支改为标签名称）
`git push origin TagName` 或一次性推送所有标签： `git push origin --tags`
若标签已推到远程，要删除远程标签则麻烦一点，首先先从本地删除：
`git tag -d v1.0` 再从远程删除： `git push origin :refs/tags/v1.0`
针对当前分支的最新commit提交创建一个标签：
`git tag v1.0`
查看标签信息：（仅查看v1系列的标签：**git tag -l "v1.*"**）
`git tag`
查看提交历史：（-n 使用**数字**作为参数则仅显示最近的几次提交信息）
`git log  --pretty=oneline --pretty=format:"%h %ad :%s" --graph`
针对提交历史中特定提交打标签：
`git tag v2.0 6723TUYG`
查看标签的指定的commit的提交信息：
`git show v2.0`
对标签详细设置其名字及说明以便区分：
`git tag -a v3.0 -m "tag info..." 3a1f237`
删除特定标签：
`git tah -d v1.0`
回退到之前的第二个版本：
`git reset --hard HEAD^`
回退到指定的提交：（工作区会跟着回退）
`git reser --hard 578IF734F`
查看版本库中最新的文件与工作区的文件的区别：（HEAD指针永远指向当前分支的最后一次提交）
`git diff HEAD -- filename`
查看尚未暂存的文件更新了哪些部分：（即尚未暂存的改动）
`git diff`
查看已暂存的文件与上次提交的差异：
`git diff --cached`
撤销暂存区中的修改，回退到工作区：
`git reset HEAD filename`
