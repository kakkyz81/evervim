# encoding: utf-8
# vim: sts=4 sw=4 fdm=marker
# Author: kakkyz <kakkyz81@gmail.com>
# License: MIT
import markdown


class parserOption:  # {{{
    def __init__(self):
        self.a          = False
        self.ul         = False
        self.ol         = False
        self.li         = False
        self.pre        = False
        self.code       = False
        self.blockquote = 0
        self.count      = 0

    def __str__(self):
        return "a={0} ul={1} ol={2} li={3} pre={4} code={5} blockquote={6} count={7} ".format(self.a,
               self.ul,
               self.ol,
               self.li,
               self.pre,
               self.code,
               self.blockquote,
               self.count)
#}}}


def parseENML(node, level=0, result='', option=parserOption()):  # {{{
    """ doctest # {{{

    >>> from xml.dom.minidom import parseString
    >>> sampleXML =   '<?xml version="1.0" encoding="utf-8"?>'
    >>> sampleXML +=  '<!DOCTYPE en-note'
    >>> sampleXML +=  '  SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    >>> sampleXML +=  '<en-note style="word-wrap: break-word;">'
    >>> sampleXML +=  '   <h1 style="color: rgb(0, 0, 0); font-weight: normal;">'
    >>> sampleXML +=  '       <font size="3">'
    >>> sampleXML +=  '           らき☆すた'
    >>> sampleXML +=  '       </font>'
    >>> sampleXML +=  '   </h1>'
    >>> sampleXML +=  '   <div style="margin-top: 5px;">'
    >>> sampleXML +=  '       <a href="http://www.google.com" style="color: blue !important;">'
    >>> sampleXML +=  '           <font size="3">'
    >>> sampleXML +=  '               <img src="http://www.google.co.jp/images/nav_logo101.png" alt="hope-echoes" />'
    >>> sampleXML +=  '               泉こなた'
    >>> sampleXML +=  '           </font>'
    >>> sampleXML +=  '       </a>'
    >>> sampleXML +=  '   </div>'
    >>> sampleXML +=  '   <en-media hash="xxxxx" style="cursor: default; vertical-align: middle;" type="image/jpeg"/>'
    >>> sampleXML +=  '   <ul>'
    >>> sampleXML +=  '       <li>リスト１</li>'
    >>> sampleXML +=  '       <li>りすと２</li>'
    >>> sampleXML +=  '       <li>リスト３</li>'
    >>> sampleXML +=  '   </ul>'
    >>> sampleXML +=  '   <en-todo checked="false"/>チェックボックス<br/>'
    >>> sampleXML +=  '   <en-todo checked="true"/>チェック済み'
    >>> sampleXML +=  '   <ol>'
    >>> sampleXML +=  '       <li> 数字付１</li>'
    >>> sampleXML +=  '       <li> 同じく２</li>'
    >>> sampleXML +=  '       <li> おまけに３</li>'
    >>> sampleXML +=  '   </ol>'
    >>> sampleXML +=  '   <ol>'
    >>> sampleXML +=  '       <li> list2-1</li>'
    >>> sampleXML +=  '       <li> list2-2</li>'
    >>> sampleXML +=  '   </ol>'
    >>> sampleXML +=  '       <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">'
    >>> sampleXML +=  '           <div> インデント</div>'
    >>> sampleXML +=  '           <div> インデント２</div>'
    >>> sampleXML +=  '       </blockquote>'
    >>> sampleXML +=  '   <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">'
    >>> sampleXML +=  '       <blockquote style="margin: 0 0 0 40px; border: none; padding: 0px;">'
    >>> sampleXML +=  '           <div> ２重インデント</div>'
    >>> sampleXML +=  '           <div> ２重インデント２</div>'
    >>> sampleXML +=  '       </blockquote>'
    >>> sampleXML +=  '   </blockquote>'
    >>> sampleXML +=  '   <pre><code>def haruhi(self):\\n'
    >>> sampleXML +=  '    pass'
    >>> sampleXML +=  '   </code></pre>'
    >>> sampleXML +=  '   <h3>asuka.langley</h3>'
    >>> sampleXML +=  '</en-note>'
    >>> dom = parseString(sampleXML)
    >>> lines = parseENML(dom.documentElement).splitlines()
    >>> #"\\n".join([line.encode('shift-jis') for line in lines])
    >>> print lines[0]
    # らき☆すた
    >>> print lines[1]
    [<img alt="hope-echoes" src="http://www.google.co.jp/images/nav_logo101.png"/>
    >>> print lines[2]
    泉こなた](http://www.google.com)
    >>> print lines[3]
    <en-media hash="xxxxx" style="cursor: default; vertical-align: middle;" type="image/jpeg"/>
    >>> print lines[4]
    * リスト１
    >>> print lines[5]
    * りすと２
    >>> print lines[6]
    * リスト３
    >>> print lines[7]
    <en-todo checked="false"/>
    >>> print lines[8]
    チェックボックス
    >>> print lines[9]
    <en-todo checked="true"/>
    >>> print lines[10]
    チェック済み
    >>> print lines[11]
    1.数字付１
    >>> print lines[12]
    2.同じく２
    >>> print lines[13]
    3.おまけに３
    >>> print lines[14]
    1.list2-1
    >>> print lines[15]
    2.list2-2
    >>> print lines[16]
    > インデント
    >>> print lines[17]
    > インデント２
    >>> print lines[18]
    > > ２重インデント
    >>> print lines[19]
    > > ２重インデント２
    >>> print lines[20]
        def haruhi(self):
    >>> print lines[21]
            pass
    >>> print lines[22]
    ### asuka.langley
    >>> #print "\\n".join(lines)
    """  
    # }}}

#   print node.toxml()
#   print "{0}:{1}:{2}:{3}:{4}:{5}".format(
#           level ,
#           _getNodeType(node) ,
#           _getTagName(node),
#           _getAttribute(node),
#           _getData(node), option)
    if node.nodeType == node.ELEMENT_NODE:
        tag = _getTagName(node)
        if tag == "a":
            htmlhref = _getAttribute(node)
            option.a = True
            htmltext = "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
            option.a = False
            result += '[{0}]({1})'.format(htmltext, htmlhref)
            result += "\n"
        elif tag == "ul":
            option.ul = True
            option.count = 0
            result += "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
            option.ul = False
        elif tag == "ol":
            option.ol = True
            option.count = 0
            result += "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
            option.ol = False
        elif tag == "pre":
            option.pre = True
            result += "".join([parseENML(child, level + 1, result, option) for child in node.childNodes])
            option.pre = False
        elif tag == "code":
            option.code = True
            result += "".join([parseENML(child, level + 1, result, option) for child in node.childNodes])
            option.code = False
        elif tag == "li":
            option.count += 1
            if option.ul:
                result += "* " + "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
            if option.ol:
                result += str(option.count) + "." + "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
        elif tag == "blockquote":
            option.blockquote += 1
            result += "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
            option.blockquote -= 1
        elif tag in ["img", "en-media", "en-todo", "en-crypt"]:  # 後で改行を除去して見やすくする？
            return node.toxml() + "\n"
        elif tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            headerlv = tag[1:]
            result += ("#" * int(headerlv)) + " " + "".join([parseENML(child, level + 1, "", option) for child in node.childNodes])
        else:
            result += "".join([parseENML(child, level + 1, result, option) for child in node.childNodes])
    elif node.nodeType == node.TEXT_NODE:
        if _getData(node).strip():
            if option.blockquote > 0:
                result += "> " * option.blockquote + _getData(node)
            elif option.pre and option.code:
                result += "\n".join(["    " + line for line in _getData(node).splitlines()])
            else:
                result += _getData(node)
            if option.a == False:
                result += "\n"
    return result
#}}}


def parseMarkdown(mkdtext):  # {{{
    #patch
#   mkdtext = [line + "<br />"for line in mkdtext]
#   print mkdtext
    m = markdown.markdown(mkdtext)
    return m
#}}}

# ----- private methods


def _getTagName(node):  # {{{
    if node.nodeType == node.ELEMENT_NODE:
        return node.tagName
    return None
#}}}


def _getData(node):  # {{{
    """ return textdata """
    if node.nodeType == node.TEXT_NODE:
        return node.data.strip()
    return ""
#}}}


def _getAttribute(node):  # {{{
    try:
        if _getTagName(node) == "a":
            return node.getAttribute("href")
    except:
        pass
    return None
#}}}


def _getNodeType(node):  # {{{
    """ return NodeType as String """
    if   node.nodeType == node.ELEMENT_NODE                    : return   "ELEMENT_NODE"
    elif node.nodeType == node.ATTRIBUTE_NODE                  : return   "ATTRIBUTE_NODE"
    elif node.nodeType == node.TEXT_NODE                       : return   "TEXT_NODE"
    elif node.nodeType == node.CDATA_SECTION_NODE              : return   "CDATA_SECTION_NODE"
    elif node.nodeType == node.ENTITY_NODE                     : return   "ENTITY_NODE"
    elif node.nodeType == node.PROCESSING_INSTRUCTION_NODE     : return   "PROCESSING_INSTRUCTION_NODE"
    elif node.nodeType == node.COMMENT_NODE                    : return   "COMMENT_NODE"
    elif node.nodeType == node.DOCUMENT_NODE                   : return   "DOCUMENT_NODE"
    elif node.nodeType == node.DOCUMENT_TYPE_NODE              : return   "DOCUMENT_TYPE_NODE"
    elif node.nodeType == node.NOTATION_NODE                   : return   "NOTATION_NODE"
    return "UKNOWN NODE"
#}}}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
