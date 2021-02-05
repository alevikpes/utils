" .vimrc

" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf8

"""""""""""""""""""
""" Indentation """
"""""""""""""""""""

filetype plugin indent on

" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab
" Be smart when using tabs ;)
set smarttab
set ai "Auto indent
set wrap "Wrap lines
" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l
" C style indentation
set cindent

""""""""""""""""""""""""
""" Set line numbers """
""""""""""""""""""""""""

" set hybrid numbers
set number relativenumber
" automatically switch between absolute (in Insert mode)
" and relative (in Command mode) numbering
augroup numbertoggle
    autocmd!
    autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
    autocmd BufLeave,FocusLost,InsertEnter * set norelativenumber
augroup END

""""""""""""""""""""""""
""" Set a map leader """
""""""""""""""""""""""""
" https://github.com/theicfire/dotfiles/blob/master/vim/.vimrc

" With a map leader it's possible to do extra key combinations
" like <leader>w saves the current file
let mapleader = " " " Leader is the space key
let g:mapleader = " "

" set some useful mapings
" easier write
nmap <leader>w :w!<cr>
nmap <leader>wa :wa!<cr>
" easier quit
nmap <leader>q :q<cr>
" silence search highlighting
nnoremap <leader>sh :nohlsearch<Bar>:echo<CR>

" scrolling
inoremap <C-E> <C-X><C-E> " scrolling on insert
inoremap <C-Y> <C-X><C-Y>
set scrolloff=3 " keep three lines between the cursor and the edge of the screen

""""""""""""""""""""""""

" set search options
set incsearch
set hlsearch

" Vertical split to the right
set splitright

" Set colour scheme
syntax enable
set t_Co=16
set background=dark
"let g:solarized_termcolors=256
"colorscheme solarised

"""""""""""""""""""""""""""""""""""
""" Highlight lines and columns """
"""""""""""""""""""""""""""""""""""

" highlight column 80
hi ColorColumn ctermbg=052
set colorcolumn=80

" highlight cursor position
hi CursorLine cterm=underline
hi CursorColumn ctermbg=237
set cursorline
set cursorcolumn

"""""""""""""""""""""""""""""""""""

" set matching brackets colour
hi MatchParen cterm=bold ctermbg=darkred ctermfg=darkgreen
" { [ ( ' " " ' ) ] }

"Remove all trailing whitespace by pressing F5
nnoremap <F5> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar>:nohl<Bar>:unlet _s<CR>

" set name of the current file in the terminal title
autocmd BufEnter * let &titlestring = ' ' . expand("%:p")             
set title

""""""""""""""""""""""""""""""""""""""""""
""" Highlight active window status bar """
""""""""""""""""""""""""""""""""""""""""""
" for the current window
hi StatusLine   ctermfg=Yellow  guifg=#ffffff ctermbg=Red guibg=#B40404 cterm=bold gui=bold
" for the Not Current window
"hi StatusLineNC ctermfg=249 guifg=#b2b2b2 ctermbg=237 guibg=#3a3a3a cterm=none gui=none

"""""""""""""""""""""""""""""""""
""" Better windows navigation """
"""""""""""""""""""""""""""""""""
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-h> <C-w>h
nnoremap <C-l> <C-w>l

"""""""""""""""""""""""""""""""""

"""""""""""""""""
"""" vim-plug """
"""""""""""""""""
" https://github.com/junegunn/vim-plug

" Install `vim-plug` if does not exist
"if !isdirectory($HOME . '/.vim/autoload')
if empty(glob('~/.vim/autoload/plug.vim'))
    silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
        \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
    autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" Start vim-plug
call plug#begin('~/.vim/bundle')

""" ctrlp.vim
" https://github.com/ctrlpvim/ctrlp.vim
Plug 'ctrlpvim/ctrlp.vim'

""" pep8-indent
" https://github.com/Vimjas/vim-python-pep8-indent
Plug 'https://github.com/Vimjas/vim-python-pep8-indent'

""" typescript-vim
" https://github.com/leafgarland/typescript-vim
"Plug 'leafgarland/typescript-vim'

""" fzf-vim
" https://github.com/junegunn/fzf.vim
"Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
"Plug 'junegunn/fzf.vim'

""" elm-format plugin
" https://github.com/ElmCast/elm-vim
"Plug 'elmcast/elm-vim'

""" vim-vue plugin
Plug 'https://github.com/posva/vim-vue.git'
" Plug 'posva/vim-vue'

""" match-count-statusline plugin
Plug 'https://github.com/emilyst/match-count-statusline.git'

" Initialize plugin system
call plug#end()

"""""""""""""""""

"" elm-format
"let g:elm_format_autosave = 1

""""""""""""""""""""""""
""" ctrlp.vim config """
""""""""""""""""""""""""
set runtimepath^=~/.vim/bundle/ctrlp.vim
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
let g:ctrlp_switch_buffer = 'Et'
let g:ctrlp_show_hidden = 1
let g:ctrlp_max_files = 0
let g:ctrlp_max_depth = 100
let g:ctrlp_open_new_file = 'v'

""""""""""""""""""""""""

"""""""""""""""""""
""" PEP8-indent """
"""""""""""""""""""
let g:pymode_indent = 0
set runtimepath^=~/.vim/bundle/pep8-indent

"""""""""""""""""""
