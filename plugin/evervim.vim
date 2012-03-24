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

if !exists('s:evervim_password')
    if !exists('g:evervim_password')
        let g:evervim_password = ''
    endif
    let s:evervim_password = g:evervim_password
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
    command! EvervimCreateNote call s:createNoteBuf()
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
        let s:evervim_password = account[1]
    endif
endfunction
"command! EvervimmerLoadAccount call s:loadAccount()
"}}}

function! s:logincheck() " {{{
    python << EOF
try:
    Evervimmer.getInstance().auth()
    print 'login successful.'
    f = open(os.path.join(vim.eval('g:evervim_workdir'),'account.txt'), 'w')
    f.write(vim.eval("g:evervim_username"))
    f.write("\n")
    f.write(vim.eval("s:evervim_password"))
    f.close()
    vim.command("call s:setCommand()")
except StandardError, e:
    print e
EOF
endfunction
""command! EvervimmerLoginCheck call s:logincheck()
"}}}

function! s:setusername() " {{{
    let g:evervim_username = input('evernote username : ')
endfunction
"}}}

function! s:setpassword() " {{{
    let s:evervim_password = input('evernote password : ')
endfunction
"}}}

function! s:setPref() " {{{
    python Evervimmer.getInstance().setPref()
    echo 'reload global variable for setting.'
endfunction
"}}}

function! s:setup() " {{{
    call s:setusername()
    call s:setpassword()
    echo 'login check...'
    python Evervimmer.getInstance().setAPI()
    python Evervimmer.getInstance().setPref()
    call s:logincheck()
endfunction
"}}}

function! s:notesByNotebook() " {{{
    call s:listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().notesByNotebook()
    setlocal nomodifiable
    
    map <silent> <buffer> <CR> :call <SID>getNote()<CR>
endfunction
"}}}

function! s:notesByTag() " {{{
    call s:listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().notesByTag()
    setlocal nomodifiable
    
    map <silent> <buffer> <CR> :call <SID>getNote()<CR>
endfunction
"}}}

function! s:getNote() " {{{
    if s:isTitle()
        return
    endif

    let l:pointer = line('.')
    call s:noteBufSetup()
 
    setlocal modifiable
    python Evervimmer.getInstance().getNote()
    exec 'silent! :w!'

    autocmd BufWritePost <buffer> call s:updateNote()
    autocmd BufUnload <buffer> call delete(g:evervim_workdir . '/__EVERVIM_NOTE__')
endfunction
"}}}

function! s:updateNote() " {{{
    python Evervimmer.getInstance().updateNote() 
endfunction
"}}}

function! s:notebookList() " {{{
    call s:listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().listNotebooks()
    setlocal nomodifiable

    map <silent> <buffer> <CR> :call <SID>notesByNotebook()<CR>
endfunction
"}}}

function! s:evervimSearchByQuery(word) " {{{
    call s:listBufSetup()

    setlocal modifiable
    python Evervimmer.getInstance().searchByQuery()
    setlocal nomodifiable

    map <silent> <buffer> <CR> :call <SID>getNote()<CR>
endfunction
"}}}

function! s:isTitle() " {{{
    let l:current = line('.')
    if l:current == 1
        return 1
    else
        return 0
    endif
endfunction
"}}}

function! s:createNote() " {{{
    python Evervimmer.getInstance().createNote() 
    bwipeout
endfunction
"}}}

function! s:createNoteBuf() " {{{
    let l:tmpflile = tempname()

    exec 'edit ' . l:tmpflile
    
    python Evervimmer.getInstance().createNoteBuf() 

    if g:evervim_usemarkdown != '0'
        call s:markdownBufSetup()
    endif

    autocmd BufWritePost <buffer> :call <SID>createNote()
endfunction
"}}}

function! s:listTags() " {{{
    call s:listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().listTags()
    setlocal nomodifiable

    map <silent> <buffer> <CR> :call <SID>notesByTag()<CR>
endfunction
"}}}

function! s:listBufSetup() " {{{
" __EVERVIM_LIST__というバッファがカレントで表示されているか調べ、ない場合は縦分割で開く。
    if getreg('%') == '__EVERVIM_LIST__'
        " already open, nothing do
    else
        exec ':lcd ' . g:evervim_workdir
        exec "vsp __EVERVIM_LIST__"
        setlocal noshowcmd
        setlocal noswapfile
        setlocal buftype=nofile
    "   setlocal bufhidden=delete
    "   setlocal nobuflisted
        setlocal nowrap
        setlocal nonumber
    endif
endfunction
"}}}

function! s:noteBufSetup() " {{{
" __EVERVIM_NOTE__というバッファがカレントで表示されているか調べ、ない場合は開く。
" __EVERVIM_NOTE__は作業用ディレクトリに保存され、バッファのアンロード時に削除
" される
    if getreg('%') == '__EVERVIM_NOTE__'
        " already open, nothing do
    else
        exec ':lcd ' . g:evervim_workdir
        exec 'silent! hide edit __EVERVIM_NOTE__'
    endif

    if g:evervim_usemarkdown != '0'
        call s:markdownBufSetup()
    endif

endfunction
"}}}

function! s:markdownBufSetup() " {{{
    set filetype=markdown
    syn match evervimTagBase '^Tags:.*$' contains=evervimTagWord
    syn keyword evervimTagWord Tags contained
    hi link evervimTagBase Statement
    hi link evervimTagWord Type
endfunction
"}}}

" ---------------------------------------------------------------------------
" setup
" ---------------------------------------------------------------------------
command! EvervimSetup call s:setup()
call s:loadAccount()
if s:evervim_password != ''
    call s:setCommand()
endif

python << EOF
import sys,os,vim
sys.path.append(os.path.join(vim.eval('expand("<sfile>:p:h")'),'py/'))
from evervimmer import Evervimmer
EOF

" vim: sts=4 sw=4 fdm=marker
