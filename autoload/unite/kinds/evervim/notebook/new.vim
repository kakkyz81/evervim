let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/notebook/new',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'new',
      \ }

function! unite#kinds#evervim#notebook#new#define() "{{{
  return s:kind
endfunction"}}}

let s:action_table.new = {
      \ 'description' : 'Create new notebook',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 0,
      \ }
function! s:action_table.new.func(candidate) "{{{
  if has_key(a:candidate, 'source__notebook_name') && a:candidate.source__new_notebook == 1
    let notebook_name = a:candidate.source__notebook_name
    " TODO notebookを生成する処理
    call unite#print_message('TODO create new notebook')
  else
    call unite#print_message('Note is already exists')
  endif
endfunction"}}}
