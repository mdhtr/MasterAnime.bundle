import Shortcuts, Objects, Constants, Log, MediaXML, XML
######################################################################################

######################################################################################
@handler('/video/masteranime', 'MasterAnime')
def Main(): # this is the landing page of the plugin because of the prefix handler.
    return ObjectContainer()
