# vibe-checker demo
# Run from the repo root: vhs demo/demo.tape
# Requires: brew install vhs

Output demo/demo.gif

Require vibe-check
Require flake8

Set Shell zsh
Set FontSize 13
Set FontFamily "Andale Mono"
Set Width 1100
Set Height 620
Set Theme "Catppuccin Mocha"
Set Padding 24
Set TypingSpeed 55ms
Set CursorBlink false

Hide
Type "cd ~/Documents/GitHub/vibe-checker"
Enter
Sleep 500ms
Show

Sleep 400ms

Type "flake8 --select=VIB demo/api.py"
Sleep 500ms
Enter

Sleep 5s

Type "vibe-check demo/"
Sleep 500ms
Enter

Sleep 6s
