function! unite#kinds#evervim#define() "{{{
  " autoload/unite/kinds/evervim/*.vimを読み込む
  return evervim#util#get_unite_definitions('kinds')
endfunction"}}}
