# %%
from youtubesearchpython import VideosSearch


'''
    get URL of the specific song from youtube 
    return title and URL of the song 
'''
def getUrl(query):
    search = VideosSearch(query, limit = 1)
    top_result = search.result()['result'][0]

    title = top_result['title']
    link = top_result['link']

    return title, link
