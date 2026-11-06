vim9script
# Vimrc file
# Version 0.5
# © Stefan Blecko 2026
# Vim 9.0+ (target: Vim 9.2). Works in Windows GUI/console and in the
# GitHub Codespaces terminal (Linux). Save as ~/.vimrc

# ---------- Core ----------
# 'nocompatible' is always on in Vim9 script and a ~/.vimrc enables it too.
set encoding=utf-8
syntax on
filetype plugin indent on

# ---------- Files ----------
set nobackup
set nowritebackup
set noswapfile
set hidden
set autoread

# ---------- Indentation (4 spaces) ----------
set tabstop=4
set shiftwidth=4
set softtabstop=4
set smarttab
set expandtab
set autoindent

# ---------- UI ----------
set statusline=%f\ -\ FileType:\ %y
set laststatus=2
set showmode
set number
set ruler
set showmatch
set showcmd
set wildmenu
set wildmode=full
set hlsearch
set incsearch
set mouse=a
set ttimeout
set ttimeoutlen=50
set backspace=indent,eol,start
set belloff=all
set spelllang=en_us

# ---------- Shell (Windows only) ----------
# In Codespaces (Linux) the default shell (bash) is used.
if has('win32')
    set shell=pwsh
    &shellcmdflag = '-NoLogo -NoProfile -Command'
    &shellquote = ''
    &shellxquote = ''
endif

# ---------- Colors / GUI ----------
if has('termguicolors') && !has('gui_running')
    set termguicolors    # true color in the Codespaces terminal
endif
set background=dark
if has('gui_running')
    set guioptions-=T    # Remove toolbar
    if has('win32')
        set guifont=Consolas:h16
    endif
endif
# Solarized is not bundled with Vim: fall back gracefully if it is missing.
try
    colorscheme solarized
catch
    colorscheme desert
endtry

# ---------- Python code completion ----------
set completeopt=menuone,noinsert,popup
set pumheight=12
# Tab / Shift-Tab move through the popup menu when it is open
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
# Ctrl-Space opens omni completion (<C-@> is what most terminals send)
inoremap <C-Space> <C-x><C-o>
inoremap <C-@> <C-x><C-o>

augroup PythonSupport
    autocmd!
    autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab autoindent
    autocmd FileType python setlocal colorcolumn=88
    # Built-in omni completion, used only when the LSP plugin is not installed
    if !isdirectory(expand('~/.vim/pack/downloads/opt/lsp'))
        autocmd FileType python &l:omnifunc = has('python3') ? 'python3complete#Complete' : 'syntaxcomplete#Complete'
    endif
    # F5 = save and run the current file
    if has('win32')
        autocmd FileType python nnoremap <buffer> <F5> :update<CR>:!python %<CR>
    else
        autocmd FileType python nnoremap <buffer> <F5> :update<CR>:!python3 %<CR>
    endif
augroup END

# ---------- Optional: LSP for Python (better completion) ----------
# Install:  git clone https://github.com/yegappan/lsp ~/.vim/pack/downloads/opt/lsp
#           npm install -g pyright
var lspOpts = {autoHighlightDiags: true}
var lspServers = [{
    name: 'pyright',
    filetype: ['python'],
    path: 'pyright-langserver',
    args: ['--stdio']
}]
if isdirectory(expand('~/.vim/pack/downloads/opt/lsp'))
    packadd lsp
    autocmd User LspSetup call LspOptionsSet(lspOpts)
    autocmd User LspSetup call LspAddServer(lspServers)
    nnoremap gd :LspGotoDefinition<CR>
    nnoremap K :LspHover<CR>
endif

# ---------- Git from inside Vim ----------
# Leader = Space. :update saves the file first. % = current file.
g:mapleader = ' '
nnoremap <leader>gs :!git status<CR>
nnoremap <leader>ga :update<CR>:!git add %<CR>
nnoremap <leader>gA :!git add -A<CR>
nnoremap <leader>gc :!git commit -m ""<Left>
nnoremap <leader>gp :!git push<CR>
nnoremap <leader>gd :!git --no-pager diff %<CR>
nnoremap <leader>gl :!git --no-pager log --oneline -10<CR>
nnoremap <leader>gt :botright terminal ++rows=12<CR>
