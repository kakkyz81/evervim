"=============================================================================
" File: evervim.vim
" Author: kakkyz <kakkyz81@gmail.com>
" WebPage: http://kakkyz81.github.com/evervim/
" License: MIT
"
"scriptencoding utf-8

" ---------------------------------------------------------------------------
" functions
" ---------------------------------------------------------------------------
function! evervim#logincheck() " {{{
    try
    python << EOF
try:
    Evervimmer.getInstance().auth()
    print 'login successful.'
    f = open(os.path.join(vim.eval('g:evervim_workdir'),'evervim_account.txt'), 'w')
    f.write(vim.eval("g:evervim_username"))
    f.write("\n")
    password = vim.eval("g:evervim_password")
    f.write(password.encode('rot13'))
    f.close()
except StandardError, e:
    print e
EOF
catch
    return '0'
endtry
    return '1'
endfunction
"}}}

function! evervim#setPref() " {{{
    python Evervimmer.getInstance().setPref()
    echo 'reload global variable for setting.'
endfunction
"}}}

function! evervim#setup() " {{{
    python Evervimmer.getInstance().setAPI()
    python Evervimmer.getInstance().setPref()
    return evervim#logincheck()
endfunction
"}}}

function! evervim#notesByNotebook() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().notesByNotebook()
    setlocal nomodifiable
    set ft=notes

    map <silent> <buffer> <CR> :call evervim#getNote()<CR>
endfunction
"}}}

function! evervim#notesByTag() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().notesByTag()
    setlocal nomodifiable
    set ft=notesbytag

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
    call evervim#setBufAutocmdWhenWritePost()
endfunction
"}}}

function! evervim#setBufAutocmdWhenWritePost() " {{{
    augroup evervimNote
        autocmd!
        autocmd BufWritePost <buffer> call evervim#updateNote()
        autocmd BufUnload <buffer> call delete(g:evervim_workdir . '/__EVERVIM_NOTE__')
    augroup END
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
    set ft=notebooks

    map <silent> <buffer> <CR> :call evervim#notesByNotebook()<CR>
endfunction
"}}}

function! evervim#evervimSearchByQuery(word) " {{{
    call evervim#listBufSetup()

    setlocal modifiable
    python Evervimmer.getInstance().searchByQuery()
    setlocal nomodifiable
    set ft=notesbyquery

    map <silent> <buffer> <CR> :call evervim#getNote()<CR>
endfunction
"}}}
 
function! evervim#pageNext() " {{{
    if &ft != 'notes' && &ft != 'notesbytag' && &ft != 'notesbyquery'
        return
    endif

    setlocal modifiable
    if &ft == 'notes'
        python Evervimmer.getInstance().notesByNotebookNextpage()
    elseif &ft == 'notesbytag'
        python Evervimmer.getInstance().notesByTagNextpage()
    elseif &ft == 'notesbyquery'
        python Evervimmer.getInstance().searchByQueryNextpage()
    endif
    setlocal nomodifiable
endfunction
"}}}

function! evervim#pagePrev() " {{{
    if &ft != 'notes' && &ft != 'notesbytag' && &ft != 'notesbyquery'
        return
    endif

    setlocal modifiable
    if &ft == 'notes'
        python Evervimmer.getInstance().notesByNotebookPrevpage()
    elseif &ft == 'notesbytag'
        python Evervimmer.getInstance().notesByTagPrevpage()
    elseif &ft == 'notesbyquery'
        python Evervimmer.getInstance().searchByQueryPrevpage()
    endif
    setlocal nomodifiable
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
    try
        python Evervimmer.getInstance().createNote() 
        " clear Create autocmd
        augroup evervimCreate
            autocmd!
        augroup END
        call evervim#setBufAutocmdWhenWritePost()
        echomsg 'create normal finish'
    catch
        echoerr 'createNote error! aborted.'
    endtry
endfunction
"}}}

function! evervim#createNoteBuf() " {{{
    call evervim#noteBufSetup()

    silent %delete _

    " clear buffer
    call append(0, "")
    call append(1, "Tags:")
    call cursor(1,0)
    setlocal nomodified

    if g:evervim_usemarkdown != '0'
        call evervim#markdownBufSetup()
    endif

    augroup evervimCreate
        autocmd!
        autocmd BufWritePost <buffer> :call evervim#createNote()
    augroup END
endfunction
"}}}

function! evervim#listTags() " {{{
    call evervim#listBufSetup()
    
    setlocal modifiable
    python Evervimmer.getInstance().listTags()
    setlocal nomodifiable
    set ft=taglists

    map <silent> <buffer> <CR> :call evervim#notesByTag()<CR>
endfunction
"}}}

function! evervim#listBufSetup() " {{{
" __EVERVIM_LIST__というバッファがカレントで表示されているか調べ、ない場合は縦分割で開く。
    let bufnr = bufwinnr('__EVERVIM_LIST__')
    if bufnr > 0
        " already open, nothing do
        exec bufnr.'wincmd w'
    else
        exec ':lcd ' . g:evervim_workdir
        exec g:evervim_splitoption . "sp __EVERVIM_LIST__"
        setlocal noshowcmd
        setlocal noswapfile
        setlocal buftype=nofile
        setlocal nowrap
        setlocal nonumber
        nmap <silent> <buffer> > :<C-u>EvervimPageNext<CR>
        nmap <silent> <buffer> < :<C-u>EvervimPagePrev<CR>
    endif
endfunction
"}}}

function! evervim#noteBufSetup() " {{{
" __EVERVIM_NOTE__というバッファがカレントで表示されているか調べ、ない場合は開く。
" __EVERVIM_NOTE__は作業用ディレクトリに保存され、バッファのアンロード時に削除
" される
    let bufnr = bufwinnr('__EVERVIM_NOTE__')
    if bufnr > 0
        exec bufnr.'wincmd w'
    else
        " buffer is nott opened , open it.
        exec ':lcd ' . g:evervim_workdir
        exec 'silent! rightbelow ' . g:evervim_splitoption . 'sp __EVERVIM_NOTE__'
    endif

    if g:evervim_usemarkdown != '0'
        call evervim#markdownBufSetup()
    endif
    " clear autosave. because when reuse buffer, autosaved(bug fix).
    augroup evervimNote
        autocmd!
    augroup END
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

function! evervim#openBrowser() " {{{
    if &ft == 'notes' || &ft == 'notesbytag' || &ft == 'notesbyquery'
        python Evervimmer.getInstance().cursorNoteOpenBrowser()
    else
        python Evervimmer.getInstance().currentNoteOpenBrowser()
    endif
endfunction
"}}}

function! evervim#openClient() " {{{
    if &ft == 'notes' || &ft == 'notesbytag' || &ft == 'notesbyquery'
        python Evervimmer.getInstance().cursorNoteOpenClient()
    else
        python Evervimmer.getInstance().currentNoteOpenClient()
    endif
endfunction
"}}}

" add command {{{
" Check OpenBrowser is installed that must be after plugin loaded, so check this.
if exists(':OpenBrowser') == 2
    command! EvervimOpenBrowser call evervim#openBrowser()
endif
"}}}

python << EOF
import sys,os,vim
sys.path.append(os.path.join(vim.eval('expand("<sfile>:p:h")'),'../plugin/py/'))
from evervimmer import Evervimmer
EOF

" vim: sts=4 sw=4 fdm=marker
