# vibe-checker demo
# Run from the repo root: vhs demo/demo.tape
# Requires: brew install vhs

Output demo/demo.gif

Require vibe-check

Set Shell zsh
Set FontSize 14
Set FontFamily "Andale Mono"
Set Width 920
Set Height 520
Set Theme "Catppuccin Mocha"
Set Padding 24
Set TypingSpeed 60ms
Set CursorBlink false

Hide
Type "cd ~/Documents/GitHub/vibe-checker"
Enter
Sleep 500ms
Show

Sleep 500ms

Type "vibe-check demo/"
Sleep 400ms
Enter

Sleep 6s
