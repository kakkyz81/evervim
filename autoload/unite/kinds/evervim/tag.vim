let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/tag',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'get_notes',
      \ }

function! unite#kinds#evervim#tag#define() "{{{
  return s:kind
endfunction"}}}

let s:action_table.get_notes = {
      \ 'description' : 'Get notes',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1,
      \ }
function! s:action_table.get_notes.func(candidate) "{{{
  if has_key(a:candidate, 'source__tag_guid')
    let guid = a:candidate.source__tag_guid
    let context = unite#get_context()
    let context.input = ''

    call unite#start([['evervim/note','tag' ,guid]], context)
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
  call unite#print_message('TODO Delete処理')
endfunction"}}}

let s:action_table.unite__new_candidate = {
      \ 'description' : 'create new tag',
      \ 'is_invalidate_cache' : 1,
      \ }
function! s:action_table.unite__new_candidate.func(candidate) "{{{
  let tag_name = unite#util#input('Please input tag name: ', '')
  call unite#print_message('TODO create tag')
endfunction"}}}
