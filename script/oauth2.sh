#!/bin/sh

url='https://ttsoon.com/org/oauth2/token/'

client='id:secret'

data='grant_type=password&username=user&password=password&scope=read'

curl --user ${client} --data ${data} ${url}