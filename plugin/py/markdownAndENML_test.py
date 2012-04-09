# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
import markdownAndENML
import unittest
from xml.dom import minidom


class TestMarkdownAndENML(unittest.TestCase):
    """ doc """

    def setUp(self):  # {{{
        pass
    #}}}

    def testParseENML(self):  # {{{
        sampleXML = '<?xml version="1.0" encoding="utf-8"?>'
        sampleXML += '<!DOCTYPE en-note'
        sampleXML += '  SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        sampleXML += '<en-note style="word-wrap: break-word;">'
        sampleXML += '   <h1 style="color: rgb(0, 0, 0); font-weight: normal;">'
        sampleXML += '       <font size="3">'
        sampleXML += '           らき☆すた'
        sampleXML += '       </font>'
        sampleXML += '   </h1>'
        sampleXML += '   <div style="margin-top: 5px;">'
        sampleXML += '       <a href="http://www.google.com" style="color: blue !important;">'
        sampleXML += '           <font size="3">'
        sampleXML += '               <img src="http://www.google.co.jp/images/nav_logo101.png" alt="hope-echoes" />'
        sampleXML += '               泉こなた'
        sampleXML += '           </font>'
        sampleXML += '       </a>'
        sampleXML += '   </div>'
        sampleXML += '   <en-media hash="xxxxx" style="cursor: default; vertical-align: middle;" type="image/jpeg"/>'
        sampleXML += '   <ul>'
        sampleXML += '       <li>リスト１</li>'
        sampleXML += '       <li>りすと２</li>'
        sampleXML += '       <li>リスト３</li>'
        sampleXML += '   </ul>'
        sampleXML += '   <en-todo checked="false"/>チェックボックス<br/>'
        sampleXML += '   <en-todo checked="true"/>チェック済み'
        sampleXML += '   <ol>'
        sampleXML += '       <li> 数字付１</li>'
        sampleXML += '       <li> 同じく２</li>'
        sampleXML += '       <li> おまけに３</li>'
        sampleXML += '   </ol>'
        sampleXML += '   <ol>'
        sampleXML += '       <li> list2-1</li>'
        sampleXML += '       <li> list2-2</li>'
        sampleXML += '   </ol>'
        sampleXML += '       <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">'
        sampleXML += '           <div> インデント</div>'
        sampleXML += '           <div> インデント２</div>'
        sampleXML += '       </blockquote>'
        sampleXML += '   <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">'
        sampleXML += '       <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">'
        sampleXML += '           <p> ２重インデント'
        sampleXML += '            ２重インデント２</p>'
        sampleXML += '       </blockquote>'
        sampleXML += '   </blockquote>'
        sampleXML += '   <p>normal line</p>'
        sampleXML += '   <pre><code>def haruhi(self):\n'
        sampleXML += '    pass<a href="hoge"> test </a>\n'
        sampleXML += '    > >'
        sampleXML += '   </code></pre>'
        sampleXML += '   <h3>asuka.langley</h3>'
        sampleXML += '</en-note>'
        dom = minidom.parseString(sampleXML)
        lines = markdownAndENML.parseENML(dom.documentElement).splitlines()
    #   print "\n".join(lines)
        self.assertEqual(lines[0], u'# らき☆すた')
        self.assertEqual(lines[1] , u'[<img alt="hope-echoes" src="http://www.google.co.jp/images/nav_logo101.png"/>')
        self.assertEqual(lines[2] , u'泉こなた](http://www.google.com)')
        self.assertEqual(lines[3] , u'<en-media hash="xxxxx" style="cursor: default; vertical-align: middle;" type="image/jpeg"/>')
        self.assertEqual(lines[4] , u'* リスト１')
        self.assertEqual(lines[5] , u'* りすと２')
        self.assertEqual(lines[6] , u'* リスト３')
        self.assertEqual(lines[7] , u'')
        self.assertEqual(lines[8] , u'<en-todo checked="false"/>')
        self.assertEqual(lines[9], u'チェックボックス')
        self.assertEqual(lines[10], u'<en-todo checked="true"/>')
        self.assertEqual(lines[11], u'チェック済み')
        self.assertEqual(lines[12], u'1. 数字付１')
        self.assertEqual(lines[13], u'2. 同じく２')
        self.assertEqual(lines[14], u'3. おまけに３')
        self.assertEqual(lines[15], u'')
        self.assertEqual(lines[16], u'1. list2-1')
        self.assertEqual(lines[17], u'2. list2-2')
        self.assertEqual(lines[18], u'')
        self.assertEqual(lines[19], u'> インデント')
        self.assertEqual(lines[20], u'> インデント２')
        self.assertEqual(lines[21], u'')
        self.assertEqual(lines[22], u'> > ２重インデント            ２重インデント２')
        self.assertEqual(lines[23], u'')
        self.assertEqual(lines[24], u'')
        self.assertEqual(lines[25], u'')
        self.assertEqual(lines[26], u'normal line')
        self.assertEqual(lines[27], u'')
        self.assertEqual(lines[28], u'    def haruhi(self):')
        self.assertEqual(lines[29], u'        pass<a href="hoge"> test </a>')
        self.assertEqual(lines[30], u'        > >')
        self.assertEqual(lines[31], u'')
        self.assertEqual(lines[32], u'### asuka.langley')
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
#   suite.addTest(TestMarkdownAndENML('testParseENML'))
#   unittest.TextTestRunner().run(suite)
