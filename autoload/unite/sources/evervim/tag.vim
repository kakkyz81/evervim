let s:source = {
      \ 'name' : 'evervim/tag',
      \ 'kind' : 'evernote/tag',
      \ 'hooks' : {},
      \ }

function! unite#sources#evervim#tag#define() "{{{
  return s:source
endfunction"}}}

function! s:source.hooks.on_init(args, context) "{{{
  call unite#sources#evervim#initialize()
endfunction"}}}

function! s:source.gather_candidates(args, context) "{{{
  let candidates = [] " TODO tagリストを返す
  return candidates
endfunction"}}}
