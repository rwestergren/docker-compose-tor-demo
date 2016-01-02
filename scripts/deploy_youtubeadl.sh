#!/bin/bash

cd ../ansible

ansible-playbook -i ../ansible/production ../ansible/site.yml --tags="deploy" --ask-vault-pass
