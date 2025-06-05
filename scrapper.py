import re
import matplotlib.pyplot as plt # type: ignore
import matplotlib as mpl # type: ignore
import emoji # type: ignore
from collections import Counter
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

plt.rcParams.update({'text.color': "white", 'axes.labelcolor': "white"})


file = open("_chat.txt", "r", encoding="utf8")
lines = file.readlines()
file.close()
file = open("_chat.txt", "r", encoding="utf8")
line = file.read().replace('\n',' ')
file.close()




message_pattern = r'^(?:\S+\s+){2}([^:]*):'
heart_pattern = '🩷|🩵|🤍|❤|💙|🤎|🧡|💜|💛|🖤|❤‍🔥|💚|🩶|❤‍🩹|💖|💗|💓|💞|💕|💘|💝|❣'
time_pattern = '([0-1]?[0-9]|2[0-3]):'
laugh_pattern = '(jaja$|JAJA$)+'


laugh_counter = 0
heart_counter = 0
message_count = {}
image_counter = 0
sticker_counter = 0
video_counter = 0
audio_counter = 0
gif_counter = 0

start_date = (re.search('\d{1,2}\/\d{1,2}\/\d{2,4}',lines[0])).group(0)
end_date = (re.search('\d{1,2}\/\d{1,2}\/\d{2,4}',lines[len(lines) - 1])).group(0)
hour_counter = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in lines:
    server_sided = re.search(r'‎', i)
    if(server_sided):
        if(re.search(r'‎audio omitted', i)):
            audio_counter += 1
            continue

        if( re.search(r'‎video omitted', i)):
            video_counter += 1
            continue

        if( re.search(r'‎image omitted', i)):
            image_counter += 1
            continue

        if( re.search(r'‎sticker omitted', i)):
            sticker_counter += 1
            continue

        if(re.search(r'‎GIF omitted', i)):
            gif_counter += 1
            continue
    else:
        hasname = re.search(message_pattern , i)
        hasheart = re.search(heart_pattern, i)
        hastime = (re.search(time_pattern, i))
        haslaugh = (re.search(laugh_pattern, i))
        if(hastime):
            hour_counter[int((hastime.group(0)).replace(':',''))] += 1
        if(hasname):
            username = hasname.group(1)  
            if(username in message_count):
                message_count[username] += 1
            else:
                message_count[username] = 1
        if(haslaugh):
            laugh_counter += 1
        hasheart = re.findall(heart_pattern, i)
        heart_counter += len(hasheart)

    



emojis = [char for char in line if char in emoji.EMOJI_DATA]
    
emoji_counts = Counter(emojis)
    
top_5_emojis = emoji_counts.most_common(5)
for i in range(5):
    top_5_emojis[i] = top_5_emojis[i][0]



prevalues = list(message_count.values())
prekeys = list(message_count.keys())
postvalues = []
postkeys = []
for i in range(2):
    fstmax = max(prevalues)
    postvalues.append(fstmax)
    postkeys.append(prekeys[prevalues.index(fstmax)])
    prevalues.remove(fstmax) 
plt.pie(postvalues, labels = postkeys, labeldistance=1.05, colors=['#5752D1','#B2B0EA'], shadow= True, autopct='%1.1f%%', wedgeprops = {"edgecolor" : "black", 
                      'linewidth': 0, 
                      'antialiased': True}, radius= 2.0, textprops={'size': 'xx-large'})
plt.savefig('pie.png', bbox_inches='tight', pad_inches = 0,  transparent = True)


norm = plt.Normalize(min(hour_counter), max(hour_counter))
colors = plt.cm.plasma(norm(hour_counter))

plt.figure(figsize=(10, 6))
plt.bar(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'], hour_counter, color=colors, edgecolor='black', width=1)
plt.xlabel('Hora del Dia')
plt.ylabel('Cantidad de Mensajes')
plt.title('Mensajes Por Hora')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('bar.png', bbox_inches='tight', pad_inches = 0,  transparent = True)

print(hour_counter)
print("start: ",start_date)
print("end: ",end_date)
print("contador de corazones: ",heart_counter)
print("top emojis: ",top_5_emojis)
print("laugh counter: ", laugh_counter)
print('contador de imagenes: ', image_counter)
print('contador de videos: ', video_counter)
print('contador de audios: ', audio_counter)
print('contador de stickers: ', sticker_counter)
print('contador de gif: ', gif_counter)




