# -*- coding: utf-8 -*-

import mastodonpost
import shutil
import os
import datetime
with open("keys/index.txt") as fp:
    for line in fp:
            mastod = mastodonpost.mastodonserver("keys/"+line.split()[0]+"_user.txt","keys/"+line.split()[0]+"_cid.txt","keys/"+line.split()[0]+"_tkn.txt",line.split("_")[0]);
if os.path.exists('./src/'):
    shutil.rmtree('src/')
print('finish, OJBK '+str(datetime.datetime.now()))
