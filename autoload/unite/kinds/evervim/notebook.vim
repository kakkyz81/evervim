function! unite#kinds#evervim#notebook#define() "{{{
  return [unite#kinds#evervim#notebook#new#define(), s:kind]
endfunction"}}}

let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/notebook',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'note',
      \ }

" kindは、複数のactionを定義したaction_tableに名前をつけて、
" 複数のsourceで使いまわせるようにする仕組みです。
" source側kindに指定した名前のkindが使えるようになります。
let s:action_table.note = { 
      \ 'description' : 'Get notes',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1,
      \ }
function! s:action_table.note.func(candidate) "{{{
  call unite#print_message('TODO 選択されたcandidateをもとに、notelistを取得してuniteを起動する')
  echo a:candidate
endfunction"}}}
