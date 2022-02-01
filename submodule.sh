#!/usr/bin/env bash

echo "Please enter your name: "
read name

echo "would you like to update your submodule [1] , add a new one [2] , or push your changes [3]? "
read answer

if [ $answer = 1 ] || [ $answer = 2 ] || [ $answer = 3 ]
then
    if [ $answer = 1 ]
    then

        git submodule update --remote $link

        git add .

        git commit -m "Updated by $name"

        git push
    fi


    if [ $answer = 2 ]
    then
        echo "PLease enter the link to the git submodule you would like to add: "
        read sub_link


        DATE=$(date)

        git submodule add $sub_link

        git commit -m "Submodule added by $name on $DATE"

        git push
    fi

    if [ $answer = 3 ]
    then
        git add .

        git commit -m "commited by $name"

        git push

        cd ./

        git add .

        git commit -m "commited by $name"

        git push
    fi
else
    echo "Invalid entry $answer"
fi