"=============================================================================
" File: evervim.vim
" Author: kakkyz <kakkyz81@gmail.com>
" Last Change: 2011-05-05
" Version: 0.1
" WebPage: https://github.com/kakkyz81/evervim
" License: MIT
"
"scriptencoding utf-8
if !has('python')
    " TODO more suitable message.
    echo "Need python. evervim finished."
    finish
endif
"
" initialize {{{
" 作業用フォルダの位置"
if !exists('g:evervim_workdir')
    let g:evervim_workdir = $HOME . '/.evervim'
endif

if !isdirectory(g:evervim_workdir)
    call mkdir(g:evervim_workdir, 'p')
endif

if !exists('g:evervim_username')
    let g:evervim_username = ''
endif

if !exists('g:evervim_password')
    let g:evervim_password = ''
endif

if !exists('g:evervim_sortnotes') " (updated|created|title) (asc|desc)
    let g:evervim_sortnotes = 'updated desc'
endif

if !exists('g:evervim_sortnotebooks') " (name|serviceCreated|serviceUpdated) (asc|desc)
    let g:evervim_sortnotebooks = 'name asc'
endif

if !exists('g:evervim_sorttags') " (name) (asc|desc)
    let g:evervim_sorttags= 'name asc'
endif

if !exists('g:evervim_xmlindent') " 
    let g:evervim_xmlindent= '    '
endif
" use markdown when edit content(default = 1 means use markdown)
if !exists('g:evervim_usemarkdown') "
    let g:evervim_usemarkdown= 1 
endif
""}}}

" ---------------------------------------------------------------------------
" functions
" ---------------------------------------------------------------------------
function! s:setCommand() " {{{
    command! EvervimNotebookList call s:notebookList()
    command! -nargs=+ EvervimmerSearchByQuery call s:evervimSearchByQuery(<q-args>)
    command! EvervimCreateNote call evervim#createNoteBuf()
    command! EvervimListTags call s:listTags()
    command! EvervimReloadPref call s:setPref()
endfunction
"}}}

function! s:loadAccount() " {{{
    let accountfile = g:evervim_workdir . '/account.txt'
    if !filereadable(accountfile)
        return
    else
        let account = readfile(accountfile)
        let g:evervim_username = account[0]
        let g:evervim_password = account[1]
    endif
endfunction
"command! EvervimmerLoadAccount call s:loadAccount()
"}}}

function! s:logincheck() " {{{
    call evervim#logincheck()
endfunction
"}}}

function! s:setusername() " {{{
    let g:evervim_username = input('evernote username : ')
endfunction
"}}}

function! s:setpassword() " {{{
    let g:evervim_password = input('evernote password : ')
endfunction
"}}}

function! s:setPref() " {{{
    call evervim#setPref()
endfunction
"}}}

function! s:setup() " {{{
    call s:setusername()
    call s:setpassword()
    echo 'login check...'
    call evervim#setup()
endfunction
"}}}

function! s:notesByNotebook() " {{{
    call evervim#notesByNotebook() 
endfunction
"}}}

function! s:notesByTag() " {{{
    call evervim#notesByTag()
endfunction
"}}}

function! s:getNote() " {{{
    call evervim#getNote()
endfunction
"}}}

function! s:updateNote() " {{{
    call evervim#updateNote()
endfunction
"}}}

function! s:notebookList() " {{{
    call evervim#notebookList()
endfunction
"}}}

function! s:evervimSearchByQuery(word) " {{{
    call evervim#evervimSearchByQuery(a:word)
endfunction
"}}}

function! s:createNote() " {{{
    call evervim#createNote()
endfunction
"}}}

function! s:listTags() " {{{
    call evervim#listTags()
endfunction
"}}}

function! s:listBufSetup() " {{{
    call evervim#listBufSetup()
endfunction
"}}}

function! s:noteBufSetup() " {{{
    call evervim#noteBufSetup()
endfunction
"}}}

function! s:markdownBufSetup() " {{{
    call evervim#markdownBufSetup()
endfunction
"}}}

" ---------------------------------------------------------------------------
" setup
" ---------------------------------------------------------------------------
command! EvervimSetup call s:setup()
call s:loadAccount()
if g:evervim_password != ''
    call s:setCommand()
endif

" vim: sts=4 sw=4 fdm=marker
