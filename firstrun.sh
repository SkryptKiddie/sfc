#!/bin/bash
# update the system, install the requirements and create the databases
echo "SFC first-run configurator"
pwd
sudo apt update -y
sudo apt upgrade -y
pip3 install -r requirements.txt
rm -rf requirements.txt
touch ./db/users.db
echo """
{
    "_default": {
        "1": {
            "username": "Owner",
            "userid": "lfE2-YpX1Y",
            "token": "admin_token"
        }
    }
}
""" > ./db/users.db
touch ./db/log.db
echo """
{
    "_default": {}
}
""" > ./db/log.db