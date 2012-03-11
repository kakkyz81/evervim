# encoding: utf-8    
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import unittest
from evervim_editor import EvervimEditor
from evervim_editor import EvervimSetting

class TestEvervimEditor(unittest.TestCase):
    """ doc """

    def setUp(self): #{{{
        self.editor  = EvervimEditor()
    #}}}

    def testSetting(self): #{{{
        setting = EvervimSetting()
        self.assertIsNone(setting.workdir              )
        self.assertIsNone(setting.username             )
        self.assertIsNone(setting.password             )
        self.assertIsNone(setting.sortnotes            )
        self.assertIsNone(setting.sortnotebooks        )
        self.assertIsNone(setting.sorttags             )
        self.assertIsNone(setting.hidexmlheader        )
        self.assertIsNone(setting.removeemptylineonxml )
        self.assertIsNone(setting.xmlindent            )
        self.assertIsNone(setting.usemarkdown          )
        self.assertRaises(AttributeError, lambda:setting.zzzzzzzzzzzz )
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
