# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import markdownAndENML
from evernoteapi import EvernoteAPI
from xml.dom import minidom


class EvervimPref(object):
    """ This object has pref of vim """
    _instance = None

    def __init__(self):
        if EvervimPref._instance is not None:
            raise RuntimeError("EvervimPref must be one object!!!")

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
        self.encoding             = None

    @classmethod
    def getInstance(self):
        if EvervimPref._instance is None:
            EvervimPref._instance = EvervimPref()

        return EvervimPref._instance


class EvervimEditor(object):
    """ editing buffertext """
    _instance = None

    def __init__(self):
        if EvervimEditor._instance is not None:
            raise RuntimeError("EvervimPref must be one object!!!")
        self.api = None

    @classmethod
    def getInstance(self):
        if EvervimEditor._instance is None:
            EvervimEditor._instance = EvervimEditor()

        return EvervimEditor._instance

    def setAPI(self):
        pref = EvervimPref.getInstance()
        if EvervimPref.getInstance().username is None:
            raise AttributeError("username must be set!!")
        if EvervimPref.getInstance().password is None:
            raise AttributeError("password must be set!!")

        self.api = EvernoteAPI(pref.username, pref.password)

