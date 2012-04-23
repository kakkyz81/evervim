# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import unittest
from evernoteapi import EvernoteAPI
from evernoteapi import EvernoteList
import evernote.edam.type.ttypes as Types

import json

testdata = json.load(open("evernoteapi_testdata.json"))

USERNAME = testdata["username"]
PASSWORD = testdata["password"]

NOTECONTENT_HEADER = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>'
NOTECONTENT_FOOTER = '</en-note>'


class TestEvernoteAPI(unittest.TestCase):
    """ doc """

    def setUp(self):  # {{{
        self.api = EvernoteAPI(USERNAME, PASSWORD)
    #}}}

    def testAuth(self):  # {{{
        """ test auth """
        self.api = EvernoteAPI(USERNAME, PASSWORD)
        self.api.auth()
        self.assertIsNotNone(self.api.user)
        self.assertIsNotNone(self.api.refreshAuthDataTime)
        self.assertIsNotNone(self.api.expirationDataTime)
    #}}}

    def testRefreshAuth(self):  # {{{
        self.api = EvernoteAPI(USERNAME, PASSWORD)
        self.api.auth()
        token               = self.api.authToken
        refreshAuthDataTime = self.api.refreshAuthDataTime
        expirationDataTime  = self.api.expirationDataTime
        self.api.refreshAuth()
        self.assertNotEqual(token               , self.api.authToken)
        self.assertNotEqual(refreshAuthDataTime , self.api.refreshAuthDataTime)
        self.assertNotEqual(expirationDataTime  , self.api.expirationDataTime)
    #}}}

    def testAuthFairueByUsername(self):  # {{{
        api = EvernoteAPI('wrong_user_name_xxxxxxxx', PASSWORD)
        self.assertRaises(StandardError, lambda: {api.auth()})

    #}}}

    def testAuthFairueByPassword(self):  # {{{
        api = EvernoteAPI(USERNAME, 'wrong_user_name_xxxxxxxx')
        self.assertRaises(StandardError, lambda: {api.auth()})
    #}}}

    def testListNoteBooks(self):  # {{{
        notebooks = self.api.listNotebooks()
        self.assertIsInstance(notebooks, list)
        self.assertNotEquals(0, len(notebooks))
        for notebook in notebooks:
            self.assertTrue(hasattr(notebook, 'guid'))
            self.assertTrue(hasattr(notebook, 'name'))
    #}}}

    def testListTags(self):  # {{{
        tags = self.api.listTags()
        self.assertIsInstance(tags , list)
        self.assertNotEquals(0, len(tags))
        for tag in tags:
            self.assertTrue(hasattr(tag, 'guid'))
            self.assertTrue(hasattr(tag, 'name'))

    #}}}

    def testNotesByTag(self):  # {{{
        tags = self.api.listTags()
        notes = []
        for tag in tags:
            [notes.append(note) for note in self.api.notesByTag(tag).elem]
        # less more 1 notes
        self.assertNotEquals(0, len(notes))
        for note in notes:
            self.assertTrue(hasattr(note, 'guid'))
     #}}}

    def testNotesByNotebook(self):  # {{{
        notebooks = self.api.listNotebooks()
        notes = []
        for notebook in notebooks:
            [notes.append(note) for note in self.api.notesByNotebook(notebook).elem]
        # less more 1 notes
        self.assertNotEquals(0, len(notes))
        for note in notes:
            self.assertTrue(hasattr(note, 'guid'))
     #}}}

    def testNotesByQuery(self):  # {{{
        notes = self.api.notesByQuery('日本語').elem
        # less more 1 notes
        self.assertNotEquals(0, len(notes))
        for note in notes:
            self.assertTrue(hasattr(note, 'guid'))
     #}}}

    def testGetNote(self):  # {{{
        note = self.__getOneNote()
        self.assertIsNone(note.content)
        notewithContent = self.api.getNote(note)
        self.assertIsNotNone(notewithContent.content)
        notewithContent.tagNames.append('google')
        self.api.updateNote(notewithContent)
    #}}}

    def testCreateNote(self):  # {{{
        note = Types.Note()
        editText = NOTECONTENT_HEADER + """this is content
日本語""" + NOTECONTENT_FOOTER
        note.title = "createNote"
        note.content = editText
        note = self.api.editTag(note, "tag1, newTag")
        createdNote = self.api.createNote(note)

        self.assertIsNotNone(createdNote.guid, None)
        getnote = Types.Note()
        getnote.guid = createdNote.guid
        self.assertIsNotNone(self.api.getNote(getnote))
    #}}}

    def testWhenUpdateNoteTagDelete(self):  # {{{
        note = Types.Note()
        editText = NOTECONTENT_HEADER + """this is content
日本語""" + NOTECONTENT_FOOTER
        note.title = "createNote"
        note.content = editText
        note = self.api.editTag(note, "tag1, newTag")
        createdNote = self.api.createNote(note)
        editTextNoTag = NOTECONTENT_HEADER + """this is content updated""" + NOTECONTENT_FOOTER

        createdNote.title = 'createNoteUpdated'
        createdNote.content = editTextNoTag
        createdNote = self.api.editTag(createdNote, "")
        self.api.updateNote(createdNote)

        getnote = Types.Note()
        getnote.guid = createdNote.guid
        getnote = self.api.getNote(getnote)
        self.assertIsNotNone(getnote)
        self.assertIsNone(getnote.tagGuids)
    #}}}

    def __getOneNote(self):  # {{{
        notes = self.api.notesByQuery('日本語').elem
        self.assertNotEquals(0, len(notes))
        for note in notes:
            return note
    #}}}

    def testEvernoteList(self):  # {{{
        evernoteList = EvernoteList()
        self.assertTrue(hasattr(evernoteList, 'elem'))
        self.assertTrue(hasattr(evernoteList, 'maxcount'))
        self.assertTrue(hasattr(evernoteList, 'maxpages'))
        self.assertTrue(hasattr(evernoteList, 'currentpage'))
    #}}}

    def testNoteList2EvernoteList(self):  # {{{
        class dummy(object):
            pass

        noteList = dummy()
        setattr(noteList , 'notes', [])
        setattr(noteList , 'totalNotes', 1)
        setattr(noteList , 'startIndex', 0)
        # test of private method!
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.maxpages, 0)
        self.assertEqual(evernoteList.currentpage, 0)

        setattr(noteList , 'totalNotes', 50)  # 0 - 50 -> 0 ( 0 is none )
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.maxpages, 0)

        setattr(noteList , 'totalNotes', 51)  # 51 - 100 -> 1
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.maxpages, 1)

        setattr(noteList , 'totalNotes', 100)  # 101 - 150 -> 2
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.maxpages, 1)

        setattr(noteList , 'totalNotes', 151)
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.maxpages, 3)

        setattr(noteList , 'startIndex', 49)   # 0 - 49 -> 0index is start from 0
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.currentpage, 0)

        setattr(noteList , 'startIndex', 50)   # 50 - 99 -> 1
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.currentpage, 1)

        setattr(noteList , 'startIndex', 100)
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.currentpage, 2)

        setattr(noteList , 'startIndex', 101)
        evernoteList = self.api._EvernoteAPI__NoteList2EvernoteList(noteList)
        self.assertEqual(evernoteList.currentpage, 2)

    #}}}

if __name__ == '__main__':
    from time import localtime, strftime
    print '\n**' + strftime("%a, %d %b %Y %H:%M:%S", localtime()) + '**\n'
# profileを取るとき
#   import test.pystone
#   import cProfile
#   import pstats
#   prof = cProfile.run("unittest.main()", 'cprof.prof')
#   p = pstats.Stats('cprof.prof')
#   p.strip_dirs()
#   p.sort_stats('cumulative')
#   p.print_stats()
#
# 全て流す時
    unittest.main()
#
# 個別でテストするとき
#   suite = unittest.TestSuite()
#   suite.addTest(TestEvernoteAPI('testNotesByNotebook'))
#   suite.addTest(TestEvernoteAPI('testNoteList2EvernoteList'))
#   suite.addTest(TestEvernoteAPI('testRefreshAuth'))
#   unittest.TextTestRunner().run(suite)
