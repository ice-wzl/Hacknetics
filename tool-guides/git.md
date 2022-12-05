# Git

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

\
