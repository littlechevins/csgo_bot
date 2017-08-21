import sys
import requests
# get_response = requests.get(url='https://csgostats.gg/match/upload')
for line in sys.stdin:
    post_data = {'sharecode':line} #'CSGO-Sxeyi-Htw35-HB7Po-SAe5U-XF95Q'
    # POST some form-encoded data:
    post_response = requests.post(url='https://csgostats.gg/match/upload', data=post_data)
    print ("Sent ", line)
    print(post_response.status_code, post_response.reason)

# print ('END')
