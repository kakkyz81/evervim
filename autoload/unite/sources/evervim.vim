function! unite#sources#evervim#define() "{{{
  if has('python')
    " autoload/unite/sources/evervim/*.vimを読み込む
    return evervim#util#get_unite_definitions('sources')
  else
    return []
  endif
endfunction"}}}

function! unite#sources#evervim#initialize() "{{{
  " 初期化処理を記述します。
  if exists('s:loaded_evervim_intializer')
    return
  endif
  let s:loaded_evervim_intializer = 1

  call unite#print_message('Initialize evervim...')
  call evervim#setup()
  python << CODE
import vim
import json
CODE

endfunction"}}}
