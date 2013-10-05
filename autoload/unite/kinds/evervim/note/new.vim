let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/note/new',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'new',
      \ }

function! unite#kinds#evervim#note#new#define() "{{{
  return s:kind
endfunction"}}}

let s:action_table.new = {
      \ 'description' : 'Create new note',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1,
      \ }
function! s:action_table.new.func(candidate) "{{{
  let candidate = a:candidate

  if has_key(a:candidate, 'source__note_name') && a:candidate.source__new_note == 1
    let note_name = a:candidate.source__note_name
    call evervim#createNoteBuf()
    0,1substitute!^.*$!\=note_name!g
  else
    call unite#print_message('Note is already exists')
  endif
endfunction"}}}
