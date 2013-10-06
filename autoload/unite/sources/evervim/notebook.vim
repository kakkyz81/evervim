let s:source = {
      \ 'name' : 'evervim/notebook',
      \ 'default_kind' : 'evervim/notebook',
      \ 'hooks' : {},
      \ }

" unite用のsourceを返す
function! unite#sources#evervim#notebook#define() "{{{
  return s:source
endfunction"}}}

" sourceの初期化処理
function! s:source.hooks.on_init(args, context) "{{{
  call unite#sources#evervim#initialize()

  " hooks以下に関数を定義することで、フックを実行できる。
  " 詳細はuniteのdocumentを見る事
  " on_syntax
  " on_close
  " on_pre_filter
  " on_post_filter
  " on_pre_init
endfunction"}}}

" 候補を取得
function! s:source.gather_candidates(args, context) "{{{
  if exists('candidates')
    unlet candidates
  endif

  " 簡単に実装してみました。
  " candidatesは下記のような仕様になっています。
  " [
  "   {
  "     'word': '検索の際に、実際使われる文字列',
  "     'abbr': '表示される文字列',
  "     'kind': '適用されるkindの名前',
  "     'source__{hogehoge}' : 'sourceにて独自に追加する要素。actionなどで使用する',
  "     'action__{hogehoge}' : 'actionにて独自に追加する要素。actionなどで使用する',
  "   },
  " ...
  " ]
  " TODO リファクタリング
  python << CODE
candidates = []
encoding = vim.eval('&enc')

for notebook in Evervimmer.editor.api.listNotebooks():
    candidate = {}
    candidate['word'] = unicode(notebook.name, 'utf-8').encode(encoding)
    candidate['source__notebook_guid'] = notebook.guid
    candidate['source__new_notebook'] = 0
    candidates.append(candidate)

candidates = sorted(candidates, key=lambda x:x['word']) # sort by notebook name
vim.command('let candidates = %s' % json.dumps(candidates, ensure_ascii=False, sort_keys=True))
CODE

  return candidates
endfunction " }}}

" 検索のクエリが書き換えられたときに候補の追加を行う
function! s:source.change_candidates(args, context) "{{{
  if a:context.input =~ '^\s*$'
    return []
  endif

  let new_notebook = {
        \ 'word'   : '[Create new notebook] ' . a:context.input,
        \ 'source' : s:source.name,
        \ 'kind' : 'evervim/notebook/new',
        \ 'source__notebook_name' : a:context.input,
        \ 'source__new_notebook' : 1
        \ }

  return [new_notebook]
endfunction"}}}
