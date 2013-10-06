let s:source = {
      \ 'name' : 'evervim/tag',
      \ 'default_kind' : 'evervim/tag',
      \ 'hooks' : {},
      \ }

function! unite#sources#evervim#tag#define() "{{{
  return s:source
endfunction"}}}

function! s:source.hooks.on_init(args, context) "{{{
  call unite#sources#evervim#initialize()
endfunction"}}}

function! s:source.gather_candidates(args, context) "{{{
  if exists('candidates')
    unlet candidates
  endif
  let candidates = []
  python << CODE
candidates = []
encoding = vim.eval('&enc')

for tag in Evervimmer.editor.api.listTags():
    candidate = {}
    candidate['word'] = unicode(tag.name, 'utf-8').encode(encoding)
    candidate['source__tag_guid'] = tag.guid
    candidate['source__new_tag'] = 0
    candidates.append(candidate)

candidates = sorted(candidates, key=lambda x:x['word']) # sort by tag name
vim.command('let candidates = %s' % json.dumps(candidates, ensure_ascii=False, sort_keys=True))
CODE

  return candidates
endfunction"}}}
