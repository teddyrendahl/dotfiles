" Disable beep if enabled
set noerrorbells visualbell t_vb=

" General Settings
set number

"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Show docstrings when folded
let g:SimpylFold_docstring_preview=1

" Syntax highlighting
let python_highlight_all=1
syntax on

" Python settings
au FileType python
    \ set tabstop=4
    \     softtabstop=4
    \     shiftwidth=4
    \     textwidth=79
    \     expandtab
    \     autoindent
    \     fileformat=unix
    \     encoding=utf-8

" General settings for shell/vim scripts, c++, etc.
au FileType sh,vim,cpp,yaml
    \ set tabstop=2
    \     softtabstop=2
    \     shiftwidth=2
    \     expandtab
    \     autoindent

" Show bad whitespace in an obvious but not obnoxious color
highlight pythonSpaceError ctermbg=darkgreen guibg=darkgreen
highlight BadWhitespace ctermbg=darkgreen guibg=darkgreen
au BufNewFile,BufRead *.py,*.pyw,*.c,*.h,*.cc,*.hh,*.sh match BadWhitespace /\s\+$/

" Store last position
if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
endif
