let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/query',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'get_notes',
      \ }

function! unite#kinds#evervim#query#define() "{{{
  return s:kind
endfunction "}}}

let s:action_table.get_notes = {
      \ 'description' : 'Get notes',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1,
      \ }
function! s:action_table.get_notes.func(candidate) "{{{
  if has_key(a:candidate, 'source__query')
    let query = a:candidate.source__query
    let context = unite#get_context()
    let context.input = ''

    call unite#start([['evervim/note','query', query]], context)
  else
    call unite#print_error('query is empty!')
  endif
endfunction "}}}
