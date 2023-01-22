# Git

### Basic Workflow&#x20;

* Git clone the repo you are interested in:

```
git clone https://github.com/jtaubs1/OSCP-Prep.git
```

* Now move into the directory that the reposity or now located in and initialize the repo

```
git init
```

* For any site that is going to be hosted on GitHub pages, ensure you check out the `gh-pages` branch

```
git checkout -b gh-pages
```

* Now make all the chages you want to make on the repo.
* To see the status of the files changed before pushing the new commits.

```
git status
```

* If these are the changes you want to make:

```
git add .
```

* Now commit the changes locally

```
git commit -m "initial commit"
```

* You only have to do the below command once, but this will instruct git where to push the changes to:

```
git remote add origin https://github.com/jtaubs1/jtaubs1.github.io.git
```

* Now make the commit official and push to your branch:

```
git push origin gh-pages
```

### Observing a Repository&#x20;

* List new or modified files not yet commited&#x20;

```
git status
```

* Show the changes to files not yet staged&#x20;

```
git diff    
```

* Show the changes to staged files&#x20;

```
git diff --cached
```

* Show all staged and unstaged file changes&#x20;

```
git diff HEAD 
```

* Show the changes between two commit ids&#x20;

```
git diff <commit1> <commit2>
```

* List the change dates and authoris for a file&#x20;

```
git blame <file>
```

* Show the file changes for a commit id and/or file&#x20;

```
git show <commit>:<file>
```

* Show full change history&#x20;

```
git log
```

* Show change history for file/directory including diffs

```
git log -p [file/directory]
```

### Working with Branches

* List all local branches&#x20;

```
git branch
```

* List all branches local and remote&#x20;

```
git branch -av 
```

* Switch to a branch, my\_branch, and update working directory&#x20;

```
git checkout my_branch
```

* Create a new branch called my\_branch

```
git branch my_branch
```

* Delete the branch called my\_branch

```
git branch -d my_branch
```

* Merge branch\_a into branch\_b

```
git checkout branch_b
git merge branch_a
```

* Tage the current commit&#x20;

```
git tag my_tag
```

### Make a Change&#x20;

* Stages the file, ready for commit&#x20;

```
git add [file]
```

* Stage all changed files, ready for commit

```
git add .
```

* Commit all staged files to versioned history&#x20;

```
git commit -m "commit message"
```

* Commit all your tracked files to versioned history

```
git commit -am "commit message"
```

* Unstages file, keeping the file changes&#x20;

```
git reset [file]
```

* Revert everything to the last commit&#x20;

```
git reset --hard 
```

### Synchronize&#x20;

* Get the latest changes from origin (no merge)

```
git fetch
```

* Fetch the latest changes from origin and merge&#x20;

```
git pull
```

* Fetch the latest changes from origin and rebase

```
git pull --rebase
```

* Push local changes to the origin&#x20;

```
git push
```
