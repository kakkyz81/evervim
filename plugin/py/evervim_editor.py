# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import markdownAndENML
from evernoteapi import EvernoteAPI
from xml.dom import minidom

class EvervimSetting(object):
	""" This object has setting of vim """
    def __init__(self):
        self.workdir              = None
        self.username             = None
        self.password             = None
        self.sortnotes            = None
        self.sortnotebooks        = None
        self.sorttags             = None
        self.hidexmlheader        = None
        self.removeemptylineonxml = None
        self.xmlindent            = None
        self.usemarkdown          = None


class EvervimEditor(object):
    """ editing buffertext """
    def __init__(self):
        pass
