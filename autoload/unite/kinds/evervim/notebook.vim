let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/notebook',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'get_notes',
      \ }

function! unite#kinds#evervim#notebook#define() "{{{
  return [unite#kinds#evervim#notebook#new#define(), s:kind]
endfunction"}}}

" kindは、複数のactionを定義したaction_tableに名前をつけて、
" 複数のsourceで使いまわせるようにする仕組みです。
" source側kindに指定した名前のkindが使えるようになります。

let s:action_table.get_notes = {
      \ 'description' : 'Get notes',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1,
      \ }
function! s:action_table.get_notes.func(candidate) "{{{
  if has_key(a:candidate, 'source__notebook_guid')
    let guid = a:candidate.source__notebook_guid
    let context = unite#get_context()
    let context.input = ''

    call unite#start([['evervim/note','notebook', guid]], context)
  else
    call unite#print_error('guid is empty!')
  endif
endfunction"}}}

let s:action_table.rename = {
      \ 'description' : 'rename',
      \ 'is_selectable' : 1,
      \ 'is_quit' : 0
      \ }
function! s:action_table.rename.func(candidates) "{{{
  call unite#print_message('TODO リネーム処理')
endfunction"}}}

let s:action_table.delete = {
      \ 'description' : 'delete',
      \ 'is_selectable' : 1,
      \ 'is_quit' : 0
      \ }
function! s:action_table.delete.func(candidates) "{{{
  call unite#print_message('TODO 削除処理')
endfunction"}}}
