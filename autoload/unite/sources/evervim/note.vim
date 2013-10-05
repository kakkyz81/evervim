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

  if len(a:args) > 0 && type(a:args[0]) == type('')
    let guid = a:args[0]

    let candidates = s:get_notelist(guid)
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

function! s:get_notelist(guid) "{{{
  call unite#print_message('TODO guidからnoteの一覧を取得&表示する')

  let sample_candidate = {
        \ 'word' : 'sample name',
        \ 'kind' : 'evervim/note',
        \ 'default_action' : 'open',
        \ 'source__new_note' : 0,
        \ 'source__guid' : a:guid,
        \ }

  return [sample_candidate]
endfunction"}}}
