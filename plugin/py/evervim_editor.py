# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import markdownAndENML
import re
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
        self.sortnotebooks        = None
        self.sorttags             = None
        self.xmlindent            = None
        self.usemarkdown          = None
        self.encoding             = None
        self.asyncupdate          = None
        self.enscriptpath         = None

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

    def note2buffer(self, note):
        """ return strings array for buffer from note. """
        """ note has attribute title, tagNames, content """
        bufStrings = []
        pref = EvervimPref.getInstance()
        doc = minidom.parseString(note.content)
        ennote = doc.getElementsByTagName("en-note")[0]

        if pref.usemarkdown == '0':
            bufStrings.append(note.title)
            bufStrings.append("Tags:" + ",".join(note.tagNames))
            contentxml = ennote.toprettyxml(indent=pref.xmlindent, encoding='utf-8')
            contentxml = re.sub('^' + pref.xmlindent, '', contentxml, flags=re.MULTILINE)
            bufStrings.extend([line for line in contentxml.splitlines()[1:-1] if line.strip()])
        else:
            bufStrings.append('# ' + note.title)
            bufStrings.append("Tags:" + ",".join(note.tagNames))
            content = markdownAndENML.parseENML(ennote).encode('utf-8')
            bufStrings.extend(content.splitlines())
        return bufStrings

    def buffer2note(self, note, buflines):
        """ return note that set title, tags, content from buftext """
        pref = EvervimPref.getInstance()
        if pref.usemarkdown == '0':
            note.title = buflines[0]
            note = self.api.editTag(note, buflines[1].replace('Tags:', ''))
            note.content  = EvernoteAPI.NOTECONTENT_HEADER + "\n".join(buflines[2:]) + EvernoteAPI.NOTECONTENT_FOOTER
        else:
            note.title = re.sub(r'^#', '',buflines[0]).strip()
            note = self.api.editTag(note, buflines[1].replace('Tags:', ''))
            parsedContent = markdownAndENML.parseMarkdown("\n".join(buflines[2:]))
            note.content  = EvernoteAPI.NOTECONTENT_HEADER + parsedContent.encode('utf-8') + EvernoteAPI.NOTECONTENT_FOOTER

        return note
