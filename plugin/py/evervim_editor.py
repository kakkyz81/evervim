# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import markdownAndENML
import evervimmer
from evernoteapi import EvernoteAPI
from xml.dom import minidom

class EvervimEditor:
    """ interface to vim """
    # {{{
    try:
        api = EvernoteAPI(vim.eval("g:evervim_username"),
                vim.eval("s:evervim_password"))
    except:
        api = None
    
    vimmer = Evervimmer()
    # }}}

    def setAPI(self):  # {{{
        """
        setup API
        """
        Evervim.api = EvernoteAPI(vim.eval("g:evervim_username"),
                vim.eval("s:evervim_password"))
    #}}}

    def auth(self):  # {{{
        """ auth """
        Evervim.api.auth()
    #}}}

    def notesByNotebook(self):  # {{{
        """ get notelist by notebook """
        selectnotebook = Evervim.notebooks[self.__getArrayIndexByCurrentLine()]
        Evervim.notes = Evervim.api.notesByNotebook(selectnotebook)
        self.sortNotes()

        notetitles = [self.__u2s(note.title) for note in Evervim.notes]
        self.__setBufferList(notetitles,
                " [notebook:%s]" % self.__u2s(selectnotebook.name))
    #}}}

    def sortNotes(self):  # {{{
        sortOpt = vim.eval('g:evervim_sortnotes').split()
        if sortOpt[1] == 'asc':
            Evervim.notes.sort(lambda a, b: cmp(getattr(a, sortOpt[0]),
                                                getattr(b, sortOpt[0])))
        else:
            Evervim.notes.sort(lambda a, b: cmp(getattr(b, sortOpt[0]),
                                                getattr(a, sortOpt[0])))

    #}}}

    def notesByTag(self):  # {{{
        selecttag = Evervim.tags[self.__getArrayIndexByCurrentLine()]
        Evervim.notes = Evervim.api.notesByTag(selecttag)
        self.sortNotes()

        notetitles = [self.__u2s(note.title) for note in Evervim.notes]
        self.__setBufferList(notetitles,
                " [tag:%s]" % self.__u2s(selecttag.name))
    #}}}

    def listNotebooks(self):  # {{{
        Evervim.notebooks = Evervim.api.listNotebooks()
        sortOpt = vim.eval('g:evervim_sortnotebooks').split()
        if sortOpt[1] == 'asc':
            Evervim.notebooks.sort(lambda a, b: cmp(getattr(a, sortOpt[0]),
                                                    getattr(b, sortOpt[0])))
        else:
            Evervim.notebooks.sort(lambda a, b: cmp(getattr(b, sortOpt[0]),
                                                    getattr(a, sortOpt[0])))

        strs = [self.__u2s(notebook.name) for notebook in Evervim.notebooks]
        self.__setBufferList(strs, " [all notebooks]")
    #}}}

    def listTags(self):  # {{{
        Evervim.tags = Evervim.api.listTags()
        sortOpt = vim.eval('g:evervim_sorttags').split()
        if sortOpt[1] == 'asc':
            Evervim.tags.sort(lambda a, b: cmp(getattr(a, sortOpt[0]),
                                               getattr(b, sortOpt[0])))
        else:
            Evervim.tags.sort(lambda a, b: cmp(getattr(b, sortOpt[0]),
                                               getattr(a, sortOpt[0])))

        strs = [self.__u2s(tag.name) for tag in Evervim.tags]
        self.__setBufferList(strs, " [all tags]")
    #}}}

    def checkNote(self):  # {{{
        """ check note format """
        bufstrs = [self.__s2u(line) for line in vim.current.buffer[:]]
        if vim.eval('g:evervim_usemarkdown') != '0':
            title    = self.__getTitleFromMkdBuf(bufstrs)
            tags     = self.__getTagsFromMkdBuf(bufstrs)
            contents = self.__getContentsFromMkdBuf(bufstrs)
        else:
            title    = self.__getTitleFromXMLBuf(bufstrs)
            tags     = self.__getTagsFromXMLBuf(bufstrs)
            contents = self.__getContentsFromXMLBuf(bufstrs)

        print contents
        print '-----------------------------------------'
        note = Evervim.api.editNote(Evervim.currentnote, title, tags, contents)

        print note.content
        minidom.parseString(note.content)
        Evervim.currentnote = note

        if len(note.title) == 0:
            raise StandardError("*** must set title! ***")
    #}}}

    def __getTitleFromXMLBuf(self, strings):  # {{{
        return strings[0]
    #}}}

    def __getTagsFromXMLBuf(self, strings):  # {{{
        return strings[1]
    #}}}

    def __getContentsFromXMLBuf(self, strings):  # {{{
        if (vim.eval("g:evervim_hidexmlheader") != '0'):
            return [EvernoteAPI.NOTECONTENT_HEADER] + strings[2::] + [EvernoteAPI.NOTECONTENT_FOOTER]
        else:
            return strings[2::]
    #}}}

    def __getTitleFromMkdBuf(self, strings):  # {{{
        return strings[0]
    #}}}

    def __getTagsFromMkdBuf(self, strings):  # {{{
        return ""
# TODO        return strings[1]
    #}}}

    def __getContentsFromMkdBuf(self, strings):  # {{{
        return [EvernoteAPI.NOTECONTENT_HEADER] + markdownAndENML.parseMarkdown("".join(strings[2::])) + [EvernoteAPI.NOTECONTENT_FOOTER]
    #}}}

    def updateNote(self):  # {{{
        self.checkNote()

        Evervim.api.updateNote(Evervim.currentnote)
        print 'update successful.'
    #}}}

    def searchByQuery(self):  # {{{
        query = vim.eval("a:word")
        Evervim.notes = Evervim.api.notesByQuery(query)
        self.sortNotes()

        notetitles = [self.__u2s(note.title) for note in Evervim.notes]
        self.__setBufferList(notetitles, " [query:%s]" % query)

    #}}}

    def createNote(self):  # {{{
        Evervim.currentnote = Evervim.api.newNote()
        self.checkNote()
        Evervim.api.createNote(Evervim.currentnote)
    #}}}

    def createNoteBuf(self):  # {{{
        vim.current.buffer[:] = None   # clear buffer & 1 ( title )
        vim.current.buffer.append('')  # 2 ( tag )
        if (vim.eval("g:evervim_hidexmlheader") == '0'):
            vim.current.buffer.append(EvernoteAPI.NOTECONTENT_HEADER)
        vim.current.buffer.append('')
        if (vim.eval("g:evervim_hidexmlheader") == '0'):
            vim.current.buffer.append(EvernoteAPI.NOTECONTENT_FOOTER)
    #}}}

    def getNote(self):  # {{{
        currentline = int(vim.eval('l:pointer'))
        selectedNote = Evervim.notes[currentline - 2]

        note = Evervim.api.getNote(selectedNote)
        Evervim.currentnote = note

        vim.current.buffer[:] = None  # clear buffer

        if vim.eval('g:evervim_usemarkdown') != '0':
            lines = self.editNoteBufferByMarkdown(note)
        else:
            lines = self.editNoteBufferByXML(note)

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
        title = self.__u2s(note.title)
        tags = self.__u2s(','.join(note.tagNames))

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
        title = self.__u2s(note.title)
        tags = self.__u2s(','.join(note.tagNames))
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
            for setline in ([self.__u2s(line) for line in contentxml.splitlines() if len(line.strip()) != 0]):
                lines.append(setline)
        else:
            lines = [self.__u2s(line) for line in contentxml.splitlines()]

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

    def __u2s(self, string):  # {{{
        """ change utf8 to shift-jis """
        if(Evervim.windows):
            try:
                return unicode(string, 'utf-8').encode('sjis')
            except:
                return string
        else:
            return string

    def __encode(self, unicodeData):  # {{{
        """ change unicode to output """
        if(Evervim.windows):
            return unicodeData.encode('sjis')
        else:
            return unicodeData.encode('utf-8')


    # }}}
    def __s2u(self, string):  # {{{
        """ change shift-jis to utf-8 """
        if(Evervim.windows):
            return unicode(string, 'sjis').encode('utf-8')
        else:
            return string
    # }}}
