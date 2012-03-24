"=============================================================================
" File: evervim.vim
" Author: kakkyz <kakkyz81@gmail.com>
" Last Change: 2011-05-05
" Version: 0.1
" WebPage: httpevervim#//github.com/kakkyz81/evervim
" License: MIT
"
"scriptencoding utf-8

" ---------------------------------------------------------------------------
" functions
" ---------------------------------------------------------------------------
function! evervim#logincheck(evervim_password) " {{{
    python << EOF
try:
    Evervimmer.getInstance().auth()
    print 'login successful.'
    f = open(os.path.join(vim.eval('g:evervim_workdir'),'account.txt'), 'w')
    f.write(vim.eval("g:evervim_username"))
    f.write("\n")
    f.write(vim.eval("g:evervim_password"))
    f.close()
    vim.command("call evervim#setCommand()")
except StandardError, e:
    print e
EOF
endfunction
"}}}

function! evervim#setPref() " {{{
    python Evervimmer.getInstance().setPref()
    echo 'reload global variable for setting.'
endfunction
"}}}

function! evervim#setup(evervim_password) " {{{
    python Evervimmer.getInstance().setAPI()
    python Evervimmer.getInstance().setPref()
    call evervim#logincheck()
endfunction
"}}}

function! evervim#notesByNotebook() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().notesByNotebook()
    setlocal nomodifiable
    
    map <silent> <buffer> <CR> :call evervim#getNote()<CR>
endfunction
"}}}

function! evervim#notesByTag() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().notesByTag()
    setlocal nomodifiable
    
    map <silent> <buffer> <CR> :call evervim#getNote()<CR>
endfunction
"}}}

function! evervim#getNote() " {{{
    if evervim#isTitle()
        return
    endif

    let l:pointer = line('.')
    call evervim#noteBufSetup()
 
    setlocal modifiable
    python Evervimmer.getInstance().getNote()
    exec 'silent! :w!'

    autocmd BufWritePost <buffer> call evervim#updateNote()
    autocmd BufUnload <buffer> call delete(g:evervim_workdir . '/__EVERVIM_NOTE__')
endfunction
"}}}

function! evervim#updateNote() " {{{
    python Evervimmer.getInstance().updateNote() 
endfunction
"}}}

function! evervim#notebookList() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().listNotebooks()
    setlocal nomodifiable

    map <silent> <buffer> <CR> :call evervim#notesByNotebook()<CR>
endfunction
"}}}

function! evervim#evervimSearchByQuery(word) " {{{
    call evervim#listBufSetup()

    setlocal modifiable
    python Evervimmer.getInstance().searchByQuery()
    setlocal nomodifiable

    map <silent> <buffer> <CR> :call evervim#getNote()<CR>
endfunction
"}}}

function! evervim#isTitle() " {{{
    let l:current = line('.')
    if l:current == 1
        return 1
    else
        return 0
    endif
endfunction
"}}}

function! evervim#createNote() " {{{
    python Evervimmer.getInstance().createNote() 
    bwipeout
endfunction
"}}}

function! evervim#createNoteBuf() " {{{
    let l:tmpflile = tempname()

    exec 'edit ' . l:tmpflile
    
    python Evervimmer.getInstance().createNoteBuf() 

    if g:evervim_usemarkdown != '0'
        call evervim#markdownBufSetup()
    endif

    autocmd BufWritePost <buffer> :call evervim#createNote()
endfunction
"}}}

function! evervim#listTags() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().listTags()
    setlocal nomodifiable

    map <silent> <buffer> <CR> :call evervim#notesByTag()<CR>
endfunction
"}}}

function! evervim#listBufSetup() " {{{
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

function! evervim#noteBufSetup() " {{{
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
        call evervim#markdownBufSetup()
    endif

endfunction
"}}}

function! evervim#markdownBufSetup() " {{{
    set filetype=markdown
    syn match evervimTagBase '^Tags:.*$' contains=evervimTagWord
    syn keyword evervimTagWord Tags contained
    hi link evervimTagBase Statement
    hi link evervimTagWord Type
endfunction
"}}}

python << EOF
import sys,os,vim
sys.path.append(os.path.join(vim.eval('expand("<sfile>:p:h")'),'../plugin/py/'))
from evervimmer import Evervimmer
EOF

" vim: sts=4 sw=4 fdm=marker
