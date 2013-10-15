let s:source = {
      \ 'name' : 'evervim/note',
      \ 'default_kind' : 'evervim/note',
      \ 'hooks' : {},
      \ }

" unite用のsourceを返す
function! unite#sources#evervim#note#define() "{{{
  return s:source
endfunction"}}}

" sourceの初期化処理
function! s:source.hooks.on_init(args, context) "{{{
  call unite#sources#evervim#initialize()
endfunction"}}}

" 候補を取得
function! s:source.gather_candidates(args, context) "{{{
  if exists('candidates')
    unlet candidates
  endif

  if len(a:args) > 0 && type(a:args[1]) == type('')
    if 'notebook' == a:args[0]
      let guid = a:args[1]
      let candidates = s:get_notelist_by_notebook(guid)
    elseif 'tag' == a:args[0]
      let guid = a:args[1]
      let candidates = s:get_notelist_by_tag(guid)
    elseif 'query' == a:args[0]
      let query = a:args[1]
      let candidates = s:get_notelist_by_query(query)
    endif
    return candidates
  else
    call unite#print_error('guid is empty!')
    return [{ 'word' : 'guid is empty!', 'is_dummy': 1 }]
  endif
endfunction"}}}

" 検索のクエリが書き換えられたときに候補の追加を行う
function! s:source.change_candidates(args, context) "{{{
  if a:context.input =~ '^\s*$'
    return []
  endif

  let new_note = {
        \ 'word'   : '[Create new note] ' . a:context.input,
        \ 'source' : s:source.name,
        \ 'kind' : 'evervim/note/new',
        \ 'source__note_name' : a:context.input,
        \ 'source__new_note' : 1
        \ }

  return [new_note]
endfunction"}}}

" get note list from notebook guid
function! s:get_notelist_by_notebook(guid) "{{{
  if exists('candidates')
    unlet candidates
  endif

python << CODE
import vim
import json

candidates = []
encoding = vim.eval('&enc')
guid = vim.eval('a:guid')

notebook = type("", (), {'guid':guid})

for note in Evervimmer.editor.api.notesByNotebook(notebook).elem:
    candidate = {}
    candidate['word'] = unicode(note.title, 'utf-8').encode(encoding)
    candidate['kind'] = 'evervim/note'
    candidate['source__note_guid'] = note.guid
    candidate['source__new_note'] = 0
    candidates.append(candidate)

vim.command('let candidates = %s' % json.dumps(candidates, ensure_ascii=False, sort_keys=True))
CODE
  return candidates
endfunction " }}}

" get note list from notebook tag
function! s:get_notelist_by_tag(guid) "{{{
  if exists('candidates')
    unlet candidates
  endif

python << CODE
candidates = []
encoding = vim.eval('&enc')
guid = vim.eval('a:guid')
tag = type("", (), {'guid':guid})

for note in Evervimmer.editor.api.notesByTag(tag).elem:
    candidate = {}
    candidate['word'] = unicode(note.title, 'utf-8').encode(encoding)
    candidate['kind'] = 'evervim/note'
    candidate['source__note_guid'] = note.guid
    candidate['source__new_note'] = 0
    candidates.append(candidate)

vim.command('let candidates = %s' % json.dumps(candidates, ensure_ascii=False, sort_keys=True))
CODE
  return candidates
endfunction " }}}

" get note list from search query
function! s:get_notelist_by_query(query) "{{{
  if exists('candidates')
    unlet candidates
  endif

python << CODE
candidates = []
encoding = vim.eval('&enc')
query = vim.eval('a:query')

for note in Evervimmer.editor.api.notesByQuery(query).elem:
    candidate = {}
    candidate['word'] = unicode(note.title, 'utf-8').encode(encoding)
    candidate['kind'] = 'evervim/note'
    candidate['source__note_guid'] = note.guid
    candidate['source__new_note'] = 0
    candidates.append(candidate)

vim.command('let candidates = %s' % json.dumps(candidates, ensure_ascii=False, sort_keys=True))
CODE
  return candidates
endfunction " }}}
