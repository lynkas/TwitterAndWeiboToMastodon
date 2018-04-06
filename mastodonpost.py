# -*- coding: utf-8 -*-

from mastodon import Mastodon
import main,weibomain

class mastodonserver():

    def __init__(self,userfile,cidfile,atkfile,tw,url='https://cap.moe'):
        mastodon = Mastodon(
            client_id = cidfile,
            access_token = atkfile,
            api_base_url = url
        )
        with open(userfile) as ulist:
            for uline in ulist:
                if tw=="t":
                    ewone = main.getxml(uline.replace("\n",""))
                else:
                    ewone = weibomain.getxml(uline.replace("\n","").split("#")[0])

                for tws in ewone.retlist:

                    imglist=[]

                    for i in tws.imgname:
                        imglist.append(mastodon.media_post('src/'+i))

                    mastodon.status_post(tws.finalcontent,media_ids=imglist)
            ulist.close()