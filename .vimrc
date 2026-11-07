vim9script
scriptencoding utf-8

# Vimrc file
# Version 0.6
# © Stefan Blecko 2026
#
# Needs Vim 9.0+ (target: Vim 9.2).  Works in the Windows GUI/console and in
# the GitHub Codespaces terminal (Linux).
#   Linux / Codespaces : save as ~/.vimrc
#   Windows            : save as ~/_vimrc   (plugins live in ~/vimfiles)
# Check your version first:  vim --version | head -1   (must say 9.x)

# ---------- Platform ----------
const isWin = has('win32')
# Vim looks for packages in ~/vimfiles on Windows and in ~/.vim elsewhere.
const vimDir = isWin ? expand('~/vimfiles') : expand('~/.vim')

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
# Adapted from :help shell-powershell; falls back to Windows PowerShell
# when pwsh (PowerShell 7) is not installed.
if isWin
    &shell = executable('pwsh') ? 'pwsh' : 'powershell'
    &shellcmdflag = '-NoLogo -NoProfile -ExecutionPolicy RemoteSigned -Command [Console]::InputEncoding=[Console]::OutputEncoding=[System.Text.Encoding]::UTF8;'
    &shellredir = '2>&1 | Out-File -Encoding UTF8 %s; exit $LastExitCode'
    &shellpipe = '2>&1 | Out-File -Encoding UTF8 %s; exit $LastExitCode'
    &shellquote = ''
    &shellxquote = ''
endif

# ---------- Colors / GUI ----------
if has('termguicolors') && !has('gui_running')
    # True color (works in the Codespaces terminal).
    set termguicolors
endif
set background=dark
if has('gui_running')
    # Remove toolbar.
    set guioptions-=T
    if isWin
        set guifont=Consolas:h16
    endif
endif
# Solarized is not bundled with Vim: fall back gracefully if it is missing.
# Install:  git clone https://github.com/altercation/vim-colors-solarized \
#               ~/.vim/pack/downloads/start/vim-colors-solarized
try
    colorscheme solarized
catch
    colorscheme desert
endtry

# ---------- Reload files changed outside Vim (git pull, checkout, ...) ----------
augroup AutoReload
    autocmd!
    autocmd FocusGained,BufEnter,CursorHold * silent! checktime
augroup END

# ---------- Python code completion ----------
set completeopt=menuone,noinsert,popup
set pumheight=12
# Tab / Shift-Tab move through the popup menu when it is open.
# Ctrl-y accepts the selected item, Ctrl-e closes the menu.
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
# Ctrl-Space opens omni completion (<C-@> is what most terminals send).
inoremap <C-Space> <C-x><C-o>
inoremap <C-@> <C-x><C-o>

# The LSP plugin is only used when BOTH the plugin and pyright are installed.
# Otherwise Vim's built-in omni completion is used.
const lspDir = vimDir .. '/pack/downloads/opt/lsp'
const useLsp = isdirectory(lspDir) && executable('pyright-langserver')

augroup PythonSupport
    autocmd!
    autocmd FileType python setlocal tabstop=4 shiftwidth=4 softtabstop=4 expandtab autoindent
    autocmd FileType python setlocal colorcolumn=88
    if !useLsp
        # Built-in omni completion (needs +python3, else generic syntax words).
        autocmd FileType python &l:omnifunc = has('python3') ? 'python3complete#Complete' : 'syntaxcomplete#Complete'
    endif
    # F5 = save and run the current file (%:S = file name, shell-escaped).
    if isWin
        autocmd FileType python nnoremap <buffer> <F5> :update<CR>:!python %:S<CR>
    else
        autocmd FileType python nnoremap <buffer> <F5> :update<CR>:!python3 %:S<CR>
    endif
augroup END

# ---------- Optional: LSP for Python (better completion) ----------
# Install (Linux / Codespaces):
#   git clone https://github.com/yegappan/lsp ~/.vim/pack/downloads/opt/lsp
#   npm install -g pyright
# Install (Windows): clone into ~/vimfiles/pack/downloads/opt/lsp instead.
# Check inside Vim:  :LspShowAllServers
var lspOpts = {autoHighlightDiags: true}
var lspServers = [{
    name: 'pyright',
    filetype: ['python'],
    path: 'pyright-langserver',
    args: ['--stdio']
}]
if useLsp
    packadd lsp
    augroup LspSupport
        autocmd!
        autocmd User LspSetup g:LspOptionsSet(lspOpts)
        autocmd User LspSetup g:LspAddServer(lspServers)
        # Mappings exist only in buffers where the server is attached,
        # so Vim's own gd and K keep working everywhere else.
        autocmd User LspAttached {
            nnoremap <buffer> <silent> gd <cmd>LspGotoDefinition<CR>
            nnoremap <buffer> <silent> gr <cmd>LspShowReferences<CR>
            nnoremap <buffer> <silent> K <cmd>LspHover<CR>
            nnoremap <buffer> <silent> [d <cmd>LspDiag prev<CR>
            nnoremap <buffer> <silent> ]d <cmd>LspDiag next<CR>
        }
    augroup END
endif

# ---------- Git from inside Vim ----------
# Leader = Space. :update saves the file first. %:S = current file, escaped.
g:mapleader = ' '
nnoremap <leader>gs :!git status<CR>
nnoremap <leader>ga :update<CR>:!git add %:S<CR>
nnoremap <leader>gA :!git add -A<CR>
nnoremap <leader>gp :!git push<CR>
nnoremap <leader>gP :!git pull<CR>
nnoremap <leader>gd :!git --no-pager diff %:S<CR>
nnoremap <leader>gl :!git --no-pager log --oneline -10<CR>
nnoremap <leader>gt :botright terminal ++rows=12<CR>
# Commit with a prompt: no quoting problems, empty message aborts.
nnoremap <leader>gc <ScriptCmd>GitCommit()<CR>

def GitCommit()
    const msg = input('Commit message: ')
    if empty(msg)
        echo ' (aborted: empty message)'
        return
    endif
    # shellescape(..., 1) also protects the special characters ! % #
    execute '!git commit -m ' .. shellescape(msg, 1)
enddef

# :G status, :G log --oneline -5, :G checkout -b new-branch, ...
command! -nargs=+ G execute '!git ' .. <q-args>

# In a Vim terminal window: press Esc Esc to get to Normal mode (scroll/copy),
# then i to go back to typing.
tnoremap <Esc><Esc> <C-w>N

