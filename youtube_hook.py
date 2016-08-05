# from __future__ import unicode_literals
# import youtube_dl

# ydl = youtube_dl.YoutubeDL()

# with ydl:
#     result = ydl.extract_info(
#         'http://www.youtube.com/watch?v=BaW_jenozKc',
#         download=False # We just want to extract the info
#     )

# if 'entries' in result:
#     # Can be a playlist or a li-st of videos
#     video = result['entries'][0]
# else:
#     # Just a video
#     video = result

# print(video)
# video_url = video['url']
# print(video_url)

import youtube_dl
import json
import pickle


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done extracting information, Do you want to download all the remaining videos now?')

sample_result = { "id" : "xyz",
				  "upload_date":  20150990,
					 "title" : "Sample Video",
					 "url" : "http://satwikkansal.xyz",
					 "playlist": "abc",
					 "playlist_title": "Motivators of the century"			 
					 }
	

def fetch_channel_info(channel_url='https://www.youtube.com/channel/UC1jfB50_OhJhDeoMaX_3WDw'):
	ydl_opts = {
	    'format': 'best',
	    'logger': MyLogger(),
	    'progress_hooks': [my_hook],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	#    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
		info_dic = ydl.extract_info(
	        channel_url,
	        download=False # We just want to extract the info
	    )
	results = []
	#print info_dic
	for vid in info_dic['entries']:
		meta_dic = { "id" : vid["id"],
					 "upload_date":  vid["upload_date"],
					 "title" : vid["title"],
					 "url" : vid["url"]				 
					 }
		try:
			meta_dic["playlist"] = vid["playlist"]
			meta_dic["playlist_titile"] = vid["playlist_title"]
		except:
			pass
		results.append(meta_dic)
	results = sorted(results, key=lambda k: k['upload_date'], reverse=True)
	update_pickle(results)
	return results

def update_meta(channel_url):
	fileObject = open('summarized_data.p','r')  
	old_data = pickle.load(fileObject)
	new_data = fetch_channel_info(channel_url)
	new_data.append(sample_result)
	new_data = sorted(new_data, key=lambda k: k['upload_date'], reverse=True)
	len_diff = len(new_data) - len(old_data)
	if(len_diff==0):
		print "Already up to date"
	else:
		i = 0
		delta = [] #List of dictionaries of to be downloaded videos
		for i in range(len_diff):
			delta.append(new_data[-i])
		print "Videos to be downloaded :",len_diff
		for i in range(len(delta)):
			print delta[i]['title']
		#update the pickle after downloading
		update_pickle(new_data)



def update_pickle(results=[]):
	file_name = "summarized_data.p"
	fileObject = open(file_name,'wb') 
	pickle.dump(results,fileObject)
	fileObject.close()

channel_url='https://www.youtube.com/channel/UC1jfB50_OhJhDeoMaX_3WDw'

fetch_channel_info(channel_url)
update_meta(channel_url)