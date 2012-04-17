# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib/'))
import evernote.edam.type.ttypes as Types
from evervim_editor import EvervimEditor
from evervim_editor import EvervimPref
from evernoteapi import EvernoteAPI

import json
testdata = json.load(open("evernoteapi_testdata.json"))

USERNAME = testdata["username"]
PASSWORD = testdata["password"]


class TestEvervimEditor(unittest.TestCase):
    """ doc """

    def setUp(self):  # {{{
        self.editor  = EvervimEditor.getInstance()
    #}}}

    def testPref(self):  # {{{
        pref = EvervimPref._instance = None
        pref = EvervimPref.getInstance()
        self.assertIsNone(pref.workdir)
        self.assertIsNone(pref.username)
        self.assertIsNone(pref.password)
        self.assertIsNone(pref.sortnotebooks)
        self.assertIsNone(pref.sorttags)
        self.assertIsNone(pref.xmlindent)
        self.assertIsNone(pref.usemarkdown)
        self.assertRaises(AttributeError, lambda: pref.zzzzzzzzzzzz)
        self.assertRaises(RuntimeError, lambda: EvervimPref())
    # }}}

    def testEditor(self):  # {{{
        self.assertRaises(RuntimeError, lambda: EvervimEditor())
    #}}}

    def testSetAPI(self):  # {{{
        pref = EvervimPref.getInstance()
        pref.username = None
        pref.password = None
        self.assertRaises(AttributeError, lambda: self.editor.setAPI())
        self.setPrefUserName()
        self.editor.setAPI()
        self.assertTrue(True)
    #}}}

    def setPrefUserName(self):  # {{{
        pref = EvervimPref.getInstance()
        pref.username = USERNAME
        pref.password = PASSWORD
    #}}}

    def testNote2buffer(self):  # {{{
        editor = EvervimEditor.getInstance()
        note = Types.Note()
        note.title = u'タイトルテスト'.encode('utf-8')
        note.tagNames = [u'タグ１'.encode('utf-8'), u'*タグ２'.encode('utf-8')]
        note.content = u"""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>this is content
本文テスト
<h3>たぐ３</h3>
</en-note>
""".encode('utf-8')
        EvervimPref.getInstance().usemarkdown = '0'     # dont use markdown
        EvervimPref.getInstance().xmlindent   = '    '  # default ts=4
        xmlStrings = editor.note2buffer(note)
        self.assertEqual(u'タイトルテスト'.encode('utf-8'), xmlStrings[0])
        self.assertEqual(u'Tags:タグ１,*タグ２'.encode('utf-8'), xmlStrings[1])
        self.assertEqual('this is content'.encode('utf-8'), xmlStrings[2])  # this is content
        self.assertEqual('本文テスト'.encode('utf-8'), xmlStrings[3])       # 本文テスト
        self.assertEqual('<h3>'.encode('utf-8'), xmlStrings[4])             # <h3>
        self.assertEqual('    たぐ３'.encode('utf-8'), xmlStrings[5])       #     たぐ３
        self.assertEqual('</h3>'.encode('utf-8'), xmlStrings[6])            # </h3>

        EvervimPref.getInstance().usemarkdown = '1'  # dont use markdown
        mkdStrings = editor.note2buffer(note)
        self.assertEqual(u'# タイトルテスト'.encode('utf-8'), mkdStrings[0])
        self.assertEqual(u'Tags:タグ１,*タグ２'.encode('utf-8'), xmlStrings[1])
        self.assertEqual('this is content'.encode('utf-8'), mkdStrings[2])
        self.assertEqual('本文テスト'.encode('utf-8'), mkdStrings[3])
        self.assertEqual('### たぐ３'.encode('utf-8'), mkdStrings[4])
    # }}}

    def testBuffer2note(self):  # {{{
        editor = EvervimEditor.getInstance()
        pref = EvervimPref.getInstance()
        pref.username = USERNAME
        pref.password = PASSWORD
        editor.setAPI()
        note = Types.Note()
        xmlBufferHead = u"""タイトルテスト
タグ１,*タグ２
""".encode('utf-8')
        xmlBufferContent = u"""this is content
本文テスト
<h3>たぐ３</h3>""".encode('utf-8')

        EvervimPref.getInstance().usemarkdown = '0'     # dont use markdown
        editednote = editor.buffer2note(note, (xmlBufferHead + xmlBufferContent).splitlines())
        self.assertEqual(u'タイトルテスト'.encode('utf-8'), editednote.title)
        self.assertEqual([u'タグ１'.encode('utf-8'), u'*タグ２'.encode('utf-8')], editednote.tagNames)
        self.assertEqual(EvernoteAPI.NOTECONTENT_HEADER + xmlBufferContent + EvernoteAPI.NOTECONTENT_FOOTER, editednote.content)

        EvervimPref.getInstance().usemarkdown = '1'
        note = Types.Note()
        mkdBuffer = u"""# タイトルテスト
タグ１,*タグ２
this is content
本文テスト
### たぐ３""".encode('utf-8')
        mkdConverted = u"""<p>this is content
本文テスト</p>
<h3>たぐ３</h3>""".encode('utf-8')

        mkdeditednote = editor.buffer2note(note, mkdBuffer.splitlines())
        self.assertEqual(u'タイトルテスト'.encode('utf-8'), mkdeditednote.title)
        self.assertEqual([u'タグ１'.encode('utf-8'), u'*タグ２'.encode('utf-8')], mkdeditednote.tagNames)
        self.assertEqual(EvernoteAPI.NOTECONTENT_HEADER + mkdConverted + EvernoteAPI.NOTECONTENT_FOOTER, mkdeditednote.content)

        # 1行目の先頭が #で始まっていない場合も、テストが通ること
        note = Types.Note()
        mkdBuffer = u"""タイトルテスト ### 途中#
タグ１,*タグ２
this is content
本文テスト
### たぐ３""".encode('utf-8')
        mkdConverted = u"""<p>this is content
本文テスト</p>
<h3>たぐ３</h3>""".encode('utf-8')

        mkdeditednote = editor.buffer2note(note, mkdBuffer.splitlines())
        self.assertEqual(u'タイトルテスト ### 途中#'.encode('utf-8'), mkdeditednote.title)
        self.assertEqual([u'タグ１'.encode('utf-8'), u'*タグ２'.encode('utf-8')], mkdeditednote.tagNames)
        self.assertEqual(EvernoteAPI.NOTECONTENT_HEADER + mkdConverted + EvernoteAPI.NOTECONTENT_FOOTER, mkdeditednote.content)
    # }}}

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
#   suite.addTest(TestEvervimEditor('testBuffer2note'))
#   unittest.TextTestRunner().run(suite)
