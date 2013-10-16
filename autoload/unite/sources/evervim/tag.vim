let s:source = {
      \ 'name' : 'evervim/tag',
      \ 'default_kind' : 'evervim/tag',
      \ 'hooks' : {},
      \ }

function! unite#sources#evervim#tag#define() "{{{
  return s:source
endfunction"}}}

function! s:source.hooks.on_init(args, context) "{{{
  call unite#sources#evervim#initialize()
endfunction"}}}

function! s:source.gather_candidates(args, context) "{{{
  if exists('candidates')
    unlet candidates
  endif
  let candidates = []
  " set candidates on python code.
  python Evervimmer.getInstance().uniteSourcesTag()

  return candidates
endfunction"}}}
