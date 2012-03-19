# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import vim
import re
import markdownAndENML
from evervim_editor import EvervimEditor
from evervim_editor import EvervimPref
from xml.dom import minidom


class Evervimmer(object):
    _instance = None

    def __init__(self):
        if Evervimmer._instance is not None:
            raise RuntimeError("EvervimPref must be one object!!!")

    @classmethod
    def getInstance(self):
        if Evervimmer._instance is None:
            Evervimmer._instance = Evervimmer()
            Evervimmer._instance.setPref()
            Evervimmer._instance.setAPI()

        return Evervimmer._instance

    """ interface to vim """
#   # {{{
#   try:
#       api = EvernoteAPI(vim.eval("g:evervim_username"),
#               vim.eval("s:evervim_password"))
#   except:
#       api = None

    # recentry loaded
    currentnote = None
    notes = []
    notebooks = []
    tags = []
    # recentry loaded
    """ if environment is windows then true """
    windows = \
        (vim.eval("has('win32')") != '0') or (vim.eval("has('win64')") != '0')
    # }}}

    editor  = EvervimEditor.getInstance()
    pref = EvervimPref.getInstance()

    """ prefs from vim option """
    def setPref(self):  # {{{
        self.pref.workdir              = vim.eval("g:evervim_workdir")
        self.pref.username             = vim.eval("g:evervim_username")
        self.pref.password             = vim.eval("s:evervim_password")
        self.pref.sortnotes            = vim.eval("g:evervim_sortnotes")
        self.pref.sortnotebooks        = vim.eval("g:evervim_sortnotebooks")
        self.pref.sorttags             = vim.eval("g:evervim_sorttags")
        self.pref.hidexmlheader        = vim.eval("g:evervim_hidexmlheader")
        self.pref.removeemptylineonxml = vim.eval("g:evervim_removeemptylineonxml")
        self.pref.xmlindent            = vim.eval("g:evervim_xmlindent")
        self.pref.usemarkdown          = vim.eval("g:evervim_usemarkdown")
        self.pref.encoding             = vim.eval('&enc')
    # }}}

    def setAPI(self):  # {{{
        """
        setup API
        """
        Evervimmer.editor.setAPI()
    #}}}

    def auth(self):  # {{{
        """ auth """
        Evervimmer.editor.api.auth()
    #}}}

    def notesByNotebook(self):  # {{{
        """ get notelist by notebook """
        selectnotebook = Evervimmer.notebooks[self.__getArrayIndexByCurrentLine()]
        Evervimmer.notes = Evervimmer.editor.api.notesByNotebook(selectnotebook)
        self.sortNotes()

        notetitles = [self.__changeEncodeToBuffer(note.title) for note in Evervimmer.notes]
        self.__setBufferList(notetitles,
                " [notebook:%s]" % self.__changeEncodeToBuffer(selectnotebook.name))
    #}}}

    def sortNotes(self):  # {{{
        sortOpt = vim.eval('g:evervim_sortnotes').split()
        if sortOpt[1] == 'asc':
            Evervimmer.notes.sort(lambda a, b: cmp(getattr(a, sortOpt[0]),
                                                getattr(b, sortOpt[0])))
        else:
            Evervimmer.notes.sort(lambda a, b: cmp(getattr(b, sortOpt[0]),
                                                getattr(a, sortOpt[0])))

    #}}}

    def notesByTag(self):  # {{{
        selecttag = Evervimmer.tags[self.__getArrayIndexByCurrentLine()]
        Evervimmer.notes = Evervimmer.editor.api.notesByTag(selecttag)
        self.sortNotes()

        notetitles = [self.__changeEncodeToBuffer(note.title) for note in Evervimmer.notes]
        self.__setBufferList(notetitles,
                " [tag:%s]" % self.__changeEncodeToBuffer(selecttag.name))
    #}}}

    def listNotebooks(self):  # {{{
        Evervimmer.notebooks = Evervimmer.editor.api.listNotebooks()
        sortOpt = vim.eval('g:evervim_sortnotebooks').split()
        if sortOpt[1] == 'asc':
            Evervimmer.notebooks.sort(lambda a, b: cmp(getattr(a, sortOpt[0]),
                                                    getattr(b, sortOpt[0])))
        else:
            Evervimmer.notebooks.sort(lambda a, b: cmp(getattr(b, sortOpt[0]),
                                                    getattr(a, sortOpt[0])))

        strs = [self.__changeEncodeToBuffer(notebook.name) for notebook in Evervimmer.notebooks]
        self.__setBufferList(strs, " [all notebooks]")
    #}}}

    def listTags(self):  # {{{
        Evervimmer.tags = Evervimmer.editor.api.listTags()
        sortOpt = vim.eval('g:evervim_sorttags').split()
        if sortOpt[1] == 'asc':
            Evervimmer.tags.sort(lambda a, b: cmp(getattr(a, sortOpt[0]),
                                               getattr(b, sortOpt[0])))
        else:
            Evervimmer.tags.sort(lambda a, b: cmp(getattr(b, sortOpt[0]),
                                               getattr(a, sortOpt[0])))

        strs = [self.__changeEncodeToBuffer(tag.name) for tag in Evervimmer.tags]
#       strs = [tag.name for tag in Evervimmer.tags]
        self.__setBufferList(strs, " [all tags]")
    #}}}

    def checkNote(self):  # {{{
        """ check note format """
        bufstrs = [self.__changeEncodeFromBuffer(line) for line in vim.current.buffer[:]]

        note = self.editor.buffer2note(Evervimmer.currentnote, bufstrs)

        print 'len:{0}'.format(len(note.content))
        print 'content:{0}'.format(note.content)
        print 'content:type{0}'.format(type(note.content))

        minidom.parseString(note.content)
        Evervimmer.currentnote = note

        if len(note.title) == 0:
            raise StandardError("*** must set title! ***")
    #}}}

    def updateNote(self):  # {{{
        self.checkNote()

        Evervimmer.editor.api.updateNote(Evervimmer.currentnote)
        print 'update successful.'
    #}}}

    def searchByQuery(self):  # {{{
        query = vim.eval("a:word")
        Evervimmer.notes = Evervimmer.editor.api.notesByQuery(query)
        self.sortNotes()

        notetitles = [self.__changeEncodeToBuffer(note.title) for note in Evervimmer.notes]
        self.__setBufferList(notetitles, " [query:%s]" % query)

    #}}}

    def createNote(self):  # {{{
        Evervimmer.currentnote = Evervimmer.editor.api.newNote()
        self.checkNote()
        Evervimmer.editor.api.createNote(Evervimmer.currentnote)
    #}}}

    def createNoteBuf(self):  # {{{
        vim.current.buffer[:] = None   # clear buffer
    #}}}

    def getNote(self):  # {{{
        currentline = int(vim.eval('l:pointer'))
        selectedNote = Evervimmer.notes[currentline - 2]

        note = Evervimmer.editor.api.getNote(selectedNote)
        Evervimmer.currentnote = note

        vim.current.buffer[:] = None  # clear buffer
        lines = [self.__changeEncodeToBuffer(line) for line in self.editor.note2buffer(note)]

        vim.current.buffer[0] = lines[0]
        for line in lines[1:]:
            vim.current.buffer.append(line)

    #}}}

    def editNoteBufferByMarkdown(self, note):  # {{{
        """
        @param  note note from evernote
        @return note buffer String (markdown parsed from xml)
        """
        bufferStrings = []
        title = self.__changeEncodeToBuffer(note.title)
        tags = self.__changeEncodeToBuffer(','.join(note.tagNames))

        doc = minidom.parseString(note.content)
        mkd = markdownAndENML.parseENML(doc.documentElement)

        bufferStrings.append(title)
        bufferStrings.append(tags)
        bufferStrings += [self.__encode(line) for line in mkd.splitlines()]

        return bufferStrings
    #}}}

    def editNoteBufferByXML(self, note):  # {{{
        """
        @param  note note from evernote
        @return note buffer String
        """
        bufferStrings = []
        title = self.__changeEncodeToBuffer(note.title)
        tags = self.__changeEncodeToBuffer(','.join(note.tagNames))
        doc = minidom.parseString(note.content)
        # format and convert
        contentxml = doc.toprettyxml(indent=vim.eval('g:evervim_xmlindent'), encoding='utf-8')

        headre = re.compile('^' + vim.eval('g:evervim_xmlindent'))
        # remove header
        if (vim.eval("g:evervim_hidexmlheader") != '0'):
            contentxml = "\n".join(re.sub(headre, '', line) for line in contentxml.splitlines()[4:-1])

        lines = []

        # remove empty lines
        if vim.eval('g:evervim_removeemptylineonxml') != '0':
            for setline in ([self.__changeEncodeToBuffer(line) for line in contentxml.splitlines() if len(line.strip()) != 0]):
                lines.append(setline)
        else:
            lines = [self.__changeEncodeToBuffer(line) for line in contentxml.splitlines()]

        bufferStrings.append(title)
        bufferStrings.append(tags)
        bufferStrings += lines

        return bufferStrings
    #}}}
# ----- private methods

    def __setBufferList(self, buffertitlelist, title):  # {{{
        vim.current.buffer[:] = None   # clear buffer
        vim.current.buffer[0] = title  # remove empty line(line 1)
        for bufline in buffertitlelist:  # 一括だとMemoryError
            vim.current.buffer.append(bufline)
    # }}}

    def __getArrayIndexByCurrentLine(self):  # {{{
        """ get index  ** 1st line is title """
        try:
            index = int(vim.eval('line(".")')) - 2
            return index if index >= 0 else 0
        except:
            return 0
    # }}}

    def __changeEncodeFromBuffer(self, string):  # {{{
        """ change &enc to utf-8 """
        if(self.pref.encoding == 'utf-8'):
            return string
        else:
            try:
                return unicode(string, self.pref.encoding).encode('utf-8')
            except:
                return string

    # }}}

    def __changeEncodeToBuffer(self, string):  # {{{
        """ change utf-8 to &enc"""
        if(self.pref.encoding == 'utf-8'):
            return string
        else:
            try:
                return unicode(string, 'utf-8').encode(self.pref.encoding)
            except:
                return string

    def __encode(self, unicodeData):  # {{{
        """ change unicode to output """
        if(Evervimmer.windows):
            return unicodeData.encode('sjis')
        else:
            return unicodeData.encode('utf-8')
    # }}}
