function! evervim#util#get_unite_definitions(kinds_or_sources) "{{{
  let definition_path = 'autoload/unite/' . a:kinds_or_sources . '/evervim/*.vim'
  let paths = split(globpath(&runtimepath, definition_path), '\n')
  let file_names = map(paths, 'fnamemodify(v:val, ":t:r")')

  let definitions = []

  for file_name in file_names
    let definition = unite#{a:kinds_or_sources}#evervim#{file_name}#define()

    if !empty(definition)
      if type(definition) == type([])
        call extend(definitions, definition)
      elseif type(definition) == type({})
        call add(definitions, definition)
      endif
    endif

    unlet definition
  endfor

  return definitions
endfunction"}}}
