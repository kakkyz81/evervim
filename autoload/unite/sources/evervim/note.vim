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
    let candidates = s:get_notelist_all()
    return candidates
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

  python Evervimmer.getInstance().uniteSourcesNoteByNotebook()
  return candidates
endfunction " }}}

" get note list from notebook tag
function! s:get_notelist_by_tag(guid) "{{{
  if exists('candidates')
    unlet candidates
  endif

  python Evervimmer.getInstance().uniteSourcesNoteByTag()
  return candidates
endfunction " }}}

" get note list from search query
function! s:get_notelist_by_query(query) "{{{
  if exists('candidates')
    unlet candidates
  endif

  python Evervimmer.getInstance().uniteSourcesNoteByQuery()
  return candidates
endfunction " }}}

" get note list all
function! s:get_notelist_all() "{{{
  if exists('candidates')
    unlet candidates
  endif

  python Evervimmer.getInstance().uniteSourcesNoteAll()
  return candidates
endfunction " }}}
