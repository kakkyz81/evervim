# encoding: utf-8    
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import vim,sys
from evernoteapi import EvernoteAPI 
from xml.dom import minidom

class Evervim:
    """ interface to vim """
    #{{{
    try:
        api = EvernoteAPI(vim.eval("g:evervim_username"), vim.eval("s:evervim_password"))
    except:
        api = None

    # recentry loaded 
    currentnote = None
    notes = []
    notebooks = []
    tags = []
    # recentry loaded 
    windows = (vim.eval("has('win32')") != '0') or (vim.eval("has('win64')") != '0')
    # }}}
    def setAPI(self): #{{{
        Evervim.api = EvernoteAPI(vim.eval("g:evervim_username"), vim.eval("s:evervim_password"))
    #}}}
    
    def auth(self): #{{{
        Evervim.api.auth()
    #}}}
    
    def notesByNotebook(self): #{{{
        selectnotebook = Evervim.notebooks[self.__getArrayIndexByCurrentLine()]
        Evervim.notes = Evervim.api.notesByNotebook(selectnotebook)
        self.sortNotes()
        
        notetitles = [ self.__u2s(note.title) for note in Evervim.notes ]
        self.__setBufferList(notetitles, " [notebook:%s]" % self.__u2s(selectnotebook.name))
    #}}}
    
    def sortNotes(self): #{{{
        sortOpt = vim.eval('g:evervim_sortnotes').split()
        if sortOpt[1] == 'asc':
            Evervim.notes.sort(lambda a,b : cmp(getattr(a, sortOpt[0]),
                                                getattr(b, sortOpt[0])))
        else:
            Evervim.notes.sort(lambda a,b : cmp(getattr(b, sortOpt[0]),
                                                getattr(a, sortOpt[0])))

    #}}}

    def notesByTag(self): #{{{
        selecttag = Evervim.tags[self.__getArrayIndexByCurrentLine()]
        Evervim.notes = Evervim.api.notesByTag(selecttag)
        self.sortNotes()
        
        notetitles = [ self.__u2s(note.title) for note in Evervim.notes ]
        self.__setBufferList(notetitles, " [tag:%s]" % self.__u2s(selecttag.name))
    #}}}

    def listNotebooks(self): #{{{
        Evervim.notebooks = Evervim.api.listNotebooks()
        sortOpt = vim.eval('g:evervim_sortnotebooks').split()
        if sortOpt[1] == 'asc':
            Evervim.notebooks.sort(lambda a,b : cmp(getattr(a, sortOpt[0]),
                                                    getattr(b, sortOpt[0])))
        else:
            Evervim.notebooks.sort(lambda a,b : cmp(getattr(b, sortOpt[0]),
                                                    getattr(a, sortOpt[0])))

        strs = [ self.__u2s(notebook.name) for notebook in Evervim.notebooks ]
        self.__setBufferList(strs, " [all notebooks]")
    #}}}

    def listTags(self): #{{{
        Evervim.tags = Evervim.api.listTags()
        sortOpt = vim.eval('g:evervim_sorttags').split()
        if sortOpt[1] == 'asc':
            Evervim.tags.sort(lambda a,b : cmp(getattr(a, sortOpt[0]),
                                               getattr(b, sortOpt[0])))
        else:
            Evervim.tags.sort(lambda a,b : cmp(getattr(b, sortOpt[0]),
                                               getattr(a, sortOpt[0])))

        strs = [ self.__u2s(tag.name) for tag in Evervim.tags ]
        self.__setBufferList(strs, " [all tags]")
    #}}}

    def checkNote(self): #{{{
        """ check note format """
        contents = [self.__s2u(line) for line in vim.current.buffer[:] ]

        if (vim.eval("g:evervim_hidexmlheader") != '0'):
            contents = contents[0:2] + [EvernoteAPI.NOTECONTENT_HEADER] + contents[2::] + [EvernoteAPI.NOTECONTENT_FOOTER]

        note = Evervim.api.editNote(Evervim.currentnote, "\n".join(contents))

        minidom.parseString(note.content)
        Evervim.currentnote = note
        if len(note.title) == 0:
            raise StandardError("*** must set title! ***")
    #}}}

    def updateNote(self): #{{{
        self.checkNote()

        Evervim.api.updateNote(Evervim.currentnote)
        print 'update successful.'
    #}}}

    def searchByQuery(self): #{{{
        query = vim.eval("a:word")
        Evervim.notes = Evervim.api.notesByQuery(query)
        self.sortNotes()
        
        notetitles = [ self.__u2s(note.title) for note in Evervim.notes ]
        self.__setBufferList(notetitles, " [query:%s]" % query)
 
    #}}}

    def createNote(self): #{{{
        Evervim.currentnote = Evervim.api.newNote()
        self.checkNote()
        Evervim.api.createNote(Evervim.currentnote)
    #}}}

    def createNoteBuf(self): #{{{
        vim.current.buffer[:] = None # clear buffer & 1 ( title )
        vim.current.buffer.append('') # 2 ( tag )
        if (vim.eval("g:evervim_hidexmlheader") == '0'):
            vim.current.buffer.append(EvernoteAPI.NOTECONTENT_HEADER) # 3 ( content ( header )))
        vim.current.buffer.append('') # 4 ( content )
        if (vim.eval("g:evervim_hidexmlheader") == '0'):
            vim.current.buffer.append(EvernoteAPI.NOTECONTENT_FOOTER) # 5 ( content ( header )))
    #}}}
 
    def getNote(self): #{{{
        currentline = int(vim.eval('l:pointer'))
        selectedNote = Evervim.notes[currentline - 2]

        note = Evervim.api.getNote(selectedNote)
        Evervim.currentnote = note

        vim.current.buffer[:] = None # clear buffer
        vim.current.buffer[0] = self.__u2s(note.title)
        vim.current.buffer.append(self.__u2s(','.join(note.tagNames)))
        
        doc = minidom.parseString(note.content)
        # format and convert 
        contentxml = doc.toprettyxml(indent=vim.eval('g:evervim_xmlindent')
                ,encoding='utf-8')
        
        # remove header
        if (vim.eval("g:evervim_hidexmlheader") != '0'): 
            contentxml = "\n".join(line.lstrip() for line in contentxml.splitlines()[4:-1])

        # remove empty lines 
        if vim.eval('g:evervim_removeemptylineonxml') != '0':
            vim.current.buffer.append([self.__u2s(line) for line 
                in contentxml.splitlines() if len(line.strip()) != 0 ])
        else:
            vim.current.buffer.append([self.__u2s(line) for line 
                in contentxml.splitlines()])
    #}}}
# ----- private methods 
    def __setBufferList(self, buffertitlelist, title): # {{{
        vim.current.buffer[:] = None  # clear buffer
        vim.current.buffer[0] = title # remove empty line(line 1)
        for bufline in buffertitlelist: # ˆêŠ‡‚¾‚ÆMemoryError
            vim.current.buffer.append(bufline)
    # }}}

    def __getArrayIndexByCurrentLine(self): # {{{
        """ get index  ** 1st line is title """
        try:
            index = int(vim.eval('line(".")')) - 2 
            return index if index >= 0 else 0
        except:
            return 0
    # }}}

    def __u2s(self, string): # {{{
        """ change utf8 to shift-jis """
        if(Evervim.windows):
            return unicode(string, 'utf-8').encode('sjis')
        else:
            return string

    # }}}
    def __s2u(self, string): # {{{
        """ change shift-jis to utf-8 """
        if(Evervim.windows):
            return unicode(string, 'sjis').encode('utf-8')
        else:
            return string
    # }}}
