# encoding: utf-8    
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import unittest
from evervim_editor import EvervimEditor

class TestEvervimEditor(unittest.TestCase):
    """ doc """

    def setUp(self): #{{{
        self.editor = EvervimEditor()
    #}}}

    def testSetAPI(self): #{{{
        self.assertIsNone(EvervimEditor.api)
        self.editor.setAPI()
        self.assertIsNotNone(EvervimEditor.api)
    #}}}

if __name__ == '__main__':
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
