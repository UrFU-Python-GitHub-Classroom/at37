# 2.2.1

```
git add README.md
git commit -m '2.2.1'
```

<<<<<<< HEAD
# 2.2.2

```
# из ветки 2.2 создали ветку 2.2-develop
git checkout -b 2.2-develop
git add .
git commit -m '2.2.2'

# после этого вернулись и с мержили изменения
git checkout 2.2
git merge 2.2-develop
=======
# 2.2.3

```
# создадим ветку от определенного коммита
git checkout -b 2.2-develop-2 6d3284
>>>>>>> 2.2-develop-2
```