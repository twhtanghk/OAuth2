#!/bin/sh

url='https://abc.com/auth/oauth2/token/'

client='id:secret'

data='grant_type=password&username=user&password=password&scope=read'

curl --user ${client} --data ${data} ${url}
