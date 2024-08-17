vim9script
# Vimrc fil
# Version 0.1
# Copyright Stefan Blecko
# compatible with Vim 9 script syntax
set encoding=utf-8
syntax on
filetype on
filetype indent on
filetype plugin on

# disable Vi compatibility
set nocompatible

set nobackup
set nowritebackup
set noswapfile
set tabstop=4
set shiftwidth=4
set softtabstop=4
set smarttab
set expandtab

set statusline=%f\ -\ FileType:\ %y
set showmode
set number
set showmatch
set showcmd
set wildmenu
set wildmode=full
set spelllang=en_us
set hlsearch
set incsearch
set ruler
set shell=pwsh
set guioptions-=T  # Remove toolbar
set guifont=Consolas:h16
if has('gui_running')
    set background=dark
    colorscheme solarized
else
    colorscheme default

endif
