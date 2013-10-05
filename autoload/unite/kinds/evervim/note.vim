let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/note',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'open',
      \ }

function! unite#kinds#evervim#note#define() "{{{
  return [unite#kinds#evervim#note#new#define(), s:kind]
endfunction"}}}

let s:action_table.open = {
      \ 'description' : 'edit note',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1
      \ }
function! s:action_table.open.func(candidate) "{{{
  call unite#print_message('Todo: noteを編集する処理')
endfunction"}}}
