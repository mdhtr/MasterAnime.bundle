# import Shortcuts, Objects, Constants, Log, MediaXML, XML
# from Constants import *
# from Shortcuts import *
# from MediaXML import *
# from XML import *
######################################################################################
TITLE = 'MasterAnime'
PREFIX = '/video/masteranime'
ART = "art-default.jpg"
ICON = "icon-default.png"
VIDEO_THUMB = "default_video_thumbnail.png"
BASE_URL = "http://www.masterani.me"

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    PopupDirectoryObject.thumb = R(ICON)
    PopupDirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(VIDEO_THUMB)
    VideoClipObject.art = R(ART)
    HTTP.CacheTime = CACHE_1HOUR

######################################################################################
@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu(): # this is the landing page of the plugin because of the prefix handler.
    oc = ObjectContainer()

    oc.add(
        DirectoryObject(
            key = Callback(RecentAnimeSubMenu, category_title='Recent Anime'),
            title = 'Recent Anime'
        )
    )
    oc.add(
        DirectoryObject(
            key = Callback(AnimeOfTheWeekSubMenu, category_title='Anime of the Week'),
            title = 'Anime of the Week'
        )
    )
    oc.add(
        DirectoryObject(
            key = Callback(CategorySubMenu, category_title='Spotlight: Being Watched', category_url=BASE_URL + '/anime/being-watched'),
            title = 'Spotlight: Being Watched'
        )
    )
    oc.add(
        DirectoryObject(
            key = Callback(CategorySubMenu, category_title='Spotlight: Popular Today', category_url=BASE_URL + '/anime/popular-today'),
            title = 'Spotlight: Popular Today'
        )
    )
    return oc

######################################################################################
# Recent Anime class="latest-anime", multipage
# 1 element:
# title array: '//*/div[@class="ui latest card"]//a[@class="title"]/text()'
# link href array: '//*/div[@class="ui latest card"]//a[@class="title"]/@href'
# thumb src array: '//*/div[@class="ui latest card"]/div[@class="image"]/img/@src'
# could be a Next page item for triggering the next page in a new directory.
@route(PREFIX + "/categoryrecent")
def RecentAnimeSubMenu(category_title):
    oc = ObjectContainer(title1=category_title)

    page_element = HTML.ElementFromURL(BASE_URL)
    serie_count = len(page_element.xpath('//*/div[@class="ui latest card"]'))
    for card in range(0, serie_count):
        serie_title = page_element.xpath('//*/div[@class="ui latest card"]//a[@class="title"]/text()')[card]
        serie_url = ValidateUrl(page_element.xpath('//*/div[@class="ui latest card"]//a[@class="title"]/@href')[card])
        serie_img = ValidateUrl(page_element.xpath('//*/div[@class="ui latest card"]/div[@class="image"]/img/@src')[card])

        oc.add(DirectoryObject(
            key = Callback(SerieSubMenu, serie_title = serie_title, serie_url = serie_url),
            title = serie_title,
            thumb = Resource.ContentsOfURLWithFallback(url = serie_img, fallback='icon-default.png'),
            summary = 'Watch ' + serie_title + ' from MasterAni.me!'
        ))
    return oc
######################################################################################
# Anime of the week:
# title (array): '//*/h1[span[text()="ANIME OF THE WEEK"]]//a/text()'
# href (array): '//*/h1[span[text()="ANIME OF THE WEEK"]]//a/@href'
# thumb (array): should be this but it might not work at all:
# '//*/h1[span[text()="ANIME OF THE WEEK"]]//a/img/@src'
@route(PREFIX + "/categoryweek")
def AnimeOfTheWeekSubMenu(category_title):
    oc = ObjectContainer(title1=category_title)

    page_element = HTML.ElementFromURL(BASE_URL)
    serie_title = page_element.xpath('//*/h1[span[text()="ANIME OF THE WEEK"]]//a/text()')[0]
    serie_url = ValidateUrl(page_element.xpath('//*/h1[span[text()="ANIME OF THE WEEK"]]//a/@href')[0])
    serie_img = ValidateUrl(page_element.xpath('//*/h1[span[text()="ANIME OF THE WEEK"]]//a/img/@src')[0])
    Log.Debug(serie_title + " " + serie_url + " " + serie_img)

    oc.add(DirectoryObject(
        key=Callback(SerieSubMenu, serie_title=serie_title, serie_url=serie_url),
        title=serie_title,
        thumb=Resource.ContentsOfURLWithFallback(url=serie_img, fallback='icon-default.png'),
        summary='Watch ' + serie_title + ' from MasterAni.me!'
    ))
    return oc
######################################################################################
# Spotlight: Popular Today
# http://www.masterani.me/anime/popular-today
# Spotlight: Being Watched
# http://www.masterani.me/anime/being-watched
@route(PREFIX + "/category")
def CategorySubMenu(category_title, category_url):
    oc = ObjectContainer(title1=category_title)

    page_element = HTML.ElementFromURL(category_url)
    serie_count = len(page_element.xpath('//*/div[@class="ui linked fluid card"]'))

    for card in range(0, serie_count):
        serie_title = page_element.xpath('//*/div[@class="ui linked fluid card"]/a[@class="ui bottom black attached button"]/text()')[card]
        serie_url = ValidateUrl(page_element.xpath('//*/div[@class="ui linked fluid card"]/a[@class="image"]/@href')[card])
        serie_img = ValidateUrl(page_element.xpath('//*/div[@class="ui linked fluid card"]/a[@class="image"]/img/@src')[card])
        Log.Debug(serie_title + " " + serie_url + " " + serie_img)

        oc.add(DirectoryObject(
            key = Callback(SerieSubMenu, serie_title = serie_title, serie_url = serie_url),
            title = serie_title,
            thumb = Resource.ContentsOfURLWithFallback(url = serie_img, fallback='icon-default.png'),
            summary = 'Watch ' + serie_title + ' from MasterAni.me!'
        ))
    return oc
######################################################################################
@route(PREFIX + "/serie")
def SerieSubMenu(serie_title, serie_url):
    oc = ObjectContainer(title1=serie_title)
    page_element = HTML.ElementFromURL(serie_url)
    # div class ui episode list
    episode_count_list = len(page_element.xpath('//*/div[@class="ui episode list"]/div'))

    # div class ui episode thumbnail
    episode_count_thumb = len(page_element.xpath('//*/div[@class="ui episode thumbnail"]/div'))

    for episode in range(0, episode_count_list):
        ep_number = page_element.xpath('//*/div[@class="ui episode list"]//div[@class="number"]/text()')[episode]
        ep_title = page_element.xpath('//*/div[@class="ui episode list"]//div[@class="title"]/text()')[episode]
        ep_url = ValidateUrl(page_element.xpath('//*/div[@class="ui episode list"]//a[@class="play"]/@href')[episode])
        episode_title = 'EP ' + ep_number + ': ' + ep_title
        #ep_img = page_element.xpath('')[episode]

        oc.add(PopupDirectoryObject(
            key = Callback(EpisodeSubMenu, episode_title = episode_title, episode_url = ep_url),
            title = episode_title,
            summary = 'Watch ' + episode_title + ' from MasterAni.me!'
        ))

    return oc
######################################################################################
@route(PREFIX + "/episode")
def EpisodeSubMenu(episode_title, episode_url):
    oc = ObjectContainer(title1=episode_title)
    page_element = HTML.ElementFromURL(episode_url)

    #TODO: list all mirrors
    # grab the actual mirror from page:
    iframes_on_page = page_element.xpath('//*/iframe/@src')
    known_hosts = [ "mp4upload", "arkvid" ]
    for iframe_src in iframes_on_page:
        for known_host in known_hosts:
            if iframe_src.find(known_host):
                host_url = iframe_src
                break
    mirror_url = episode_url + "??" + host_url

    oc.add(PopupDirectoryObject(
            key = Callback(MirrorSubMenu, episode_title = episode_title, mirror_url = mirror_url),
            title = episode_title,
            summary = 'Watch ' + episode_title + ' from MasterAni.me!'
        ))
    return oc
######################################################################################
@route(PREFIX + "/mirrors")
def MirrorSubMenu(episode_title, mirror_url):
    oc = ObjectContainer()

    # TODO: play video
    oc.add(VideoClipObject(
            url = mirror_url,
            title = episode_title
            )
        )
    return oc
######################################################################################

######################################################################################
### UTILS
######################################################################################
def ValidateUrl(url):
    if url.startswith('//'):
        correct_url = 'http:' + url
        return correct_url
    elif url.startswith('/'):
        correct_url = BASE_URL + url
        return correct_url
    elif url.startswith('https://'):
        correct_url = url.replace('https://', 'http://')
        return correct_url
    else:
        return url
