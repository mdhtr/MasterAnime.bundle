import Shortcuts, Objects, Constants, Log, MediaXML, XML
from Constants import *
from Shortcuts import *
######################################################################################
TITLE = 'MasterAnime'
PREFIX = '/video/masteranime'
ART = "art-default.jpg"
ICON = "icon-default.png"

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    PopupDirectoryObject.thumb = R(ICON)
    PopupDirectoryObject.art = R(ART)
    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)
    HTTP.CacheTime = CACHE_1HOUR

######################################################################################
@handler(PREFIX, TITLE)
def MainMenu(): # this is the landing page of the plugin because of the prefix handler.
    # Recent Anime class="latest-anime", multipage
    # 1 element:
    # title array: '//*/div[@class="ui latest card"]//a[@class="title"]/text()'
    # link href array: '//*/div[@class="ui latest card"]//a[@class="title"]/@href'
    # thumb src array: '//*/div[@class="ui latest card"]/div[@class="image"]/img/@src'
    # could be a Next page item for triggering the next page in a new directory.

    # Anime of the week:
    # title (array): '//*/h1[span[text()="ANIME OF THE WEEK"]]//a/text()'
    # href (array): '//*/h1[span[text()="ANIME OF THE WEEK"]]//a/@href'
    # thumb (array): should be this but it might not work at all:
    # '//*/h1[span[text()="ANIME OF THE WEEK"]]//a/img/@src'

    # Spotlight: Being Watched / Popular Today




    oc = ObjectContainer()

    return ObjectContainer()

