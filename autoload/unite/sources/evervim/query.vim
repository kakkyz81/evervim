let s:source = {
      \ 'name' : 'evervim/query',
      \ 'hooks': {},
      \ }

function! unite#sources#evervim#query#define() "{{{
  return s:source
endfunction"}}}

function! s:source.hooks.on_init(args, context) "{{{
  let a:context.source__input = a:context.input
  if a:context.source__input == ''
    let a:context.source__input =
          \ unite#util#input('Please input search query: ', '')
  endif

  call unite#sources#evervim#initialize()

  call unite#print_source_message('Search word: '
        \ . a:context.source__input, s:source.name)
endfunction"}}}

function! s:source.gather_candidates(args, context) "{{{
  let query = a:context.source__input
  call unite#print_message('TODO 検索 -> candidatesに変換')

  return [{ 'word': 'Input query:' . query }]
endfunction"}}}
