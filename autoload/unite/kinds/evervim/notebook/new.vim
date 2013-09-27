function! unite#kinds#evervim#notebook#new#define() "{{{
  return s:kind
endfunction"}}}

let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/notebook/new',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'new',
      \ }

let s:action_table.new = {
      \ 'description' : 'Create new notebook',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1,
      \ }
function! s:action_table.new.func(candidate) "{{{
  let candidate = a:candidate

  if has_key(a:candidate, 'source__notebook_name') && a:candidate.source__new_notebook == 1
    let notebook_name = a:candidate.source__notebook_name
    call evervim#createNoteBuf()
    0,1substitute!^.*$!\=notebook_name!g
  else
    call unite#print_message('Notebook is already exists')
  endif
endfunction"}}}
