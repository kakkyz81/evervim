let s:action_table = {}
let s:kind = {
      \ 'name' : 'evervim/note',
      \ 'action_table' : s:action_table,
      \ 'default_action' : 'open',
      \ }

function! unite#kinds#evervim#note#define() " {{{
    return [unite#kinds#evervim#note#new#define(), s:kind]
endfunction " }}}

let s:action_table.open = {
      \ 'description' : 'edit note',
      \ 'is_selectable' : 0,
      \ 'is_quit' : 1
      \ }
function! s:action_table.open.func(candidate) " {{{
    call evervim#noteBufSetup()
    setlocal modifiable
    python << CODE
Evervimmer.getInstance().getNoteUnite(vim.eval('a:candidate.source__note_guid'))
CODE
    exec 'silent! :w!'
    call evervim#setBufAutocmdWhenWritePost()
endfunction " }}}

let s:action_table.unite__new_candidate = {
      \ 'description' : 'create new note',
      \ 'is_invalidate_cache' : 1,
      \ }
function! s:action_table.unite__new_candidate.func(candidate) "{{{
  let note_name = unite#util#input('Please input note title: ', '')
  call unite#kinds#evervim#note#new#create_buffer(note_name)
endfunction"}}}
