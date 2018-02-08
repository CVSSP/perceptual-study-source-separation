# git remote add listen https://github.com/deeuu/listen.git

# Update listen
git checkout master
git fetch listen
git checkout listen/master site/assets site/_layouts site/_includes site/staticman.yml
git commit -a -m "Merge listen"
