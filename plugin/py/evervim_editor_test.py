# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import unittest
from evervim_editor import EvervimEditor
from evervim_editor import EvervimPref

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
        pref = EvervimPref.getInstance()
        self.assertIsNone(pref.workdir)
        self.assertIsNone(pref.username)
        self.assertIsNone(pref.password)
        self.assertIsNone(pref.sortnotes)
        self.assertIsNone(pref.sortnotebooks)
        self.assertIsNone(pref.sorttags)
        self.assertIsNone(pref.hidexmlheader)
        self.assertIsNone(pref.removeemptylineonxml)
        self.assertIsNone(pref.xmlindent)
        self.assertIsNone(pref.usemarkdown)
        self.assertRaises(AttributeError, lambda: pref.zzzzzzzzzzzz)
        self.assertRaises(RuntimeError, lambda: EvervimPref())

    def testEditor(self):  # {{{
        self.assertRaises(RuntimeError, lambda: EvervimEditor())

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
#   suite.addTest(TestEvernoteAPI('testWhenUpdateNoteTagDelete'))
#   unittest.TextTestRunner().run(suite)
