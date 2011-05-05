# encoding: utf-8    
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import unittest
from evernoteapi import EvernoteAPI 
from xml.dom import minidom, Node
import evernote.edam.type.ttypes as Types

import json

testdata = json.load(open("evernoteapi_testdata.json"))

USERNAME = testdata["username"]
PASSWORD = testdata["password"]

NOTECONTENT_HEADER = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>' 
NOTECONTENT_FOOTER = '</en-note>'

class TestEvernoteAPI(unittest.TestCase):
    """ doc """

    def setUp(self): #{{{
        self.api = EvernoteAPI(USERNAME, PASSWORD)
    #}}}

#   def testAuth(self): #{{{
#       """ test auth """
#       self.api.auth()
#       self.assertIsNotNone(self.api.user)
#       self.assertIsNotNone(self.api.authToken)
#   #}}}

#   def testAuthFairueByUsername(self): #{{{
#       try:
#           failureApi = EvernoteAPI('wrong_user_name_xxxxxxxx', PASSWORD)
#           self.assertTrue(false) # must be exception
#       except StandardError:
#           pass
#   #}}}

#   def testAuthFairueByPassword(self): #{{{
#       try:
#           failureApi = EvenoteAPI(USERNAME, 'wrong_user_name_xxxxxxxx')
#           self.assertTrue(false) # must be exception
#       except StandardError:
#           pass
#   #}}}
#   
#   def testListNoteBooks(self): #{{{
#       notebooks = self.api.listNotebooks()
#       self.assertIsInstance(notebooks, list)
#       self.assertNotEquals(0, len(notebooks))
#       for notebook in notebooks:
#           self.assertTrue(hasattr(notebook,'guid'))
#           self.assertTrue(hasattr(notebook,'name'))
#   #}}}

#   def testListTags(self): #{{{
#       tags = self.api.listTags()
#       self.assertIsInstance(tags , list)
#       self.assertNotEquals(0, len(tags))
#       for tag in tags:
#           self.assertTrue(hasattr(tag,'guid'))
#           self.assertTrue(hasattr(tag,'name'))
#
#   #}}}
#   
#   def testNotesByTag(self): #{{{
#       tags = self.api.listTags()
#       notes = []
#       for tag in tags:
#           [notes.append(note) for note in self.api.notesByTag(tag)]
#       # less more 1 notes
#       self.assertNotEquals(0, len(notes))
#       for note in notes:
#           self.assertTrue(hasattr(note, 'guid'))
#    #}}}

#   def testNotesByNotebook(self): #{{{
#       notebooks = self.api.listNotebooks()
#       notes = []
#       for notebook in notebooks:
#           [notes.append(note) for note in self.api.notesByNotebook(notebook)]
#       # less more 1 notes
#       self.assertNotEquals(0, len(notes))
#       for note in notes:
#           self.assertTrue(hasattr(note, 'guid'))
#    #}}}
#
#   def testNotesByQuery(self): #{{{
#       notes = self.api.notesByQuery('日本語')
#       # less more 1 notes
#       self.assertNotEquals(0, len(notes))
#       for note in notes:
#           self.assertTrue(hasattr(note, 'guid'))
#    #}}}

#   def testGetNote(self): #{{{
#       note = self.__getOneNote()
#       self.assertIsNone(note.content)
#       notewithContent = self.api.getNote(note)
#       self.assertIsNotNone(notewithContent.content)
#       notewithContent.tagNames.append('google')
#       self.api.updateNote(notewithContent)
#   #}}}

#   def testEditNoteIllegalParameter(self): #{{{
#       note = self.__getOneNote()
#       try:
#           self.assertRaises(StandardError, self.api.editNote(note, "1 line"))
#       except StandardError:
#           pass
#       try:
#           self.assertRaises(StandardError, self.api.editNote(note, "2 line\n 2"))
#       except StandardError:
#           pass
#       self.api.editNote(note, "3 line\n 1 \n 2")
#       self.assertTrue(True)
#   #}}}

    def testEditNote(self): #{{{
        return # FIXME
        note = self.__getOneNote()
        notewithContent = self.api.getNote(note)
        content = minidom.parseString(notewithContent.content)
        editText = """this is test
tag1, newTag
""" + NOTECONTENT_HEADER + """this is content
日本語オーケー
追加部分""" + NOTECONTENT_FOOTER
        self.api.editNote(notewithContent, editText)
        self.assertListEqual(notewithContent.tagNames, [])
        self.assertNotEqual(0, len(notewithContent.guid))
        self.assertEqual(notewithContent.title, 'this is test')
        self.assertEqual(notewithContent.content, NOTECONTENT_HEADER + """this is content
日本語オーケー
追加部分""" + NOTECONTENT_FOOTER)
        self.api.updateNote(notewithContent)
        self.assertTrue(True)
    #}}}
    
    def testCreateNote(self): #{{{
    #   return # FIXME 
        note = Types.Note()
        editText = """createNote 
tag1, newTag
""" + NOTECONTENT_HEADER + """this is content
日本語"""+ NOTECONTENT_FOOTER
        note = self.api.editNote(note, editText)
        createdNote = self.api.createNote(note)

        self.assertIsNotNone(createdNote.guid, None)
        getnote = Types.Note()
        getnote.guid = createdNote.guid
        self.assertIsNotNone(self.api.getNote(getnote))
    #}}}

    def testWhenUpdateNoteTagDelete(self): #{{{
        return # FIXME 
        note = Types.Note()
        editText = """createNote 
tag1, newTag
this is content
日本語"""
        note = self.api.editNote(note, editText)
        createdNote = self.api.createNote(note)
        editTextNoTag = """createNoteUpdated 

this is content updated"""
        createdNote = self.api.editNote(createdNote, editTextNoTag)
        self.api.updateNote(createdNote)

        getnote = Types.Note()
        getnote.guid = createdNote.guid
        getnote = self.api.getNote(getnote)
        self.assertIsNotNone(getnote)
        self.assertIsNone(getnote.tagGuids)
    #}}}

    def __getOneNote(self): #{{{
        notes = self.api.notesByQuery('日本語')
        self.assertNotEquals(0, len(notes))
        for note in notes:
            return note
    #}}}
 
if __name__ == '__main__':
#   import test.pystone
#   import cProfile
#   import pstats

#   prof = cProfile.run("unittest.main()", 'cprof.prof')
#   p = pstats.Stats('cprof.prof')
#   p.strip_dirs()
#   p.sort_stats('cumulative')
#   p.print_stats()
    unittest.main()
