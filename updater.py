from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup as bs
import os, requests

load_dotenv(find_dotenv())
YT_API_KEY = os.getenv("YT_API_KEY")
YT_CHANNEL_ID = os.getenv("YT_CHANNEL_ID")
DISCORD_INVITE_ID = os.getenv("DISCORD_INVITE_ID")

vidURL = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + YT_CHANNEL_ID + "&maxResults=3&order=date&type=video&key=" + YT_API_KEY
subsURL = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + YT_CHANNEL_ID + "&key=" + YT_API_KEY
discordURL = "https://discord.com/api/v9/invites/"+ DISCORD_INVITE_ID +"?with_counts=true"

response1 = requests.get(vidURL)
data_json1 = response1.json()
res1 = data_json1["items"]
response2 = requests.get(subsURL)
data_json2 = response2.json()
res2 = ((data_json2["items"])[0])["statistics"]

response3 = requests.get(discordURL)
data_json3 = response3.json()

videos = []
for i in res1:
    vID = (i["id"])["videoId"]
    videos.append(vID)

subsCount = res2["subscriberCount"]
videoCount = res2["videoCount"]
viewCount = res2["viewCount"]
discordCount = data_json3["approximate_member_count"]
stats = {"subscribers": subsCount, "videos": videoCount, "views": viewCount, "discordMembers": discordCount}

base = os.path.dirname(os.path.abspath(__file__))
html = open('index.html')
soup = bs(html, 'html.parser')

print("HTML has been updated with the following details- ")
print("Video IDs- ")
for i in range(0,3):
    idNo = i + 1
    idName = "update" + str(idNo)
    new_tag = soup.find("lite-youtube", {"id": idName})
    print("• "+ videos[i])
    new_tag['videoid'] = videos[i]
    replacer = soup.find("lite-youtube", {"id": idName}).replace_with(new_tag)

print()

for k,v in stats.items():
    vint = int(v)
    vstr = str(v)
    if (vint < 10000) and (vint > 999):
        val = vstr[0:1] + "." + vstr[1:2] + "K+"
    elif (vint < 100000) and (vint > 9999):
        val = vstr[0:2] + "." + vstr[2:3] + "K+"
    elif (vint < 1000000) and (vint > 99999):
        val = vstr[0:3] + "." + vstr[3:4] + "K+"
    elif (vint < 10000000) and (vint > 999999):
        val = vstr[0:1] + "." + vstr[1:2] + "M+"
    elif (vint < 100000000) and (vint > 9999999):
        val = vstr[0:1] + "." + vstr[1:2] + "B+"
    elif (vint < 1000000000) and (vint > 99999999):
        val = vstr[0:1] + "." + vstr[1:2] + "T+"
    else:
        val = vstr + "+"
    new_tag = soup.find("span", {"id": k})
    new_tag.string = val
    print(k + ": " + val)

with open("index.html", "wb") as f_output:
    f_output.write(soup.prettify("utf-8"))
