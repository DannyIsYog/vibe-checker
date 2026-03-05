import * as vscode from 'vscode';
import { execFile } from 'child_process';

interface Violation {
  file: string; line: number; col: number;
  code: string; message: string;
}

function computeScore(violations: Violation[]): number {
  return Math.max(0, Math.min(100, 100 - violations.length * 5));
}

export function activate(context: vscode.ExtensionContext): void {
  const decorationType = vscode.window.createTextEditorDecorationType({
    after: {
      fontStyle: 'italic',
      color: new vscode.ThemeColor('editorGhostText.foreground'),
      margin: '0 0 0 3ch',
    },
    rangeBehavior: vscode.DecorationRangeBehavior.ClosedClosed,
  });

  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBar.tooltip = 'Vibe score for this file — click to check workspace';
  statusBar.command = 'vibe-checker.checkWorkspace';

  const outputChannel = vscode.window.createOutputChannel('Vibe Checker');

  function applyDecorations(editor: vscode.TextEditor, violations: Violation[]): void {
    const byLine = new Map<number, string[]>();
    for (const v of violations) {
      const msgs = byLine.get(v.line) ?? [];
      msgs.push(v.message);
      byLine.set(v.line, msgs);
    }
    const decorations: vscode.DecorationOptions[] = [];
    for (const [line, msgs] of byLine) {
      decorations.push({
        range: new vscode.Range(line - 1, Number.MAX_SAFE_INTEGER, line - 1, Number.MAX_SAFE_INTEGER),
        renderOptions: { after: { contentText: `  ${msgs.join(' · ')}` } },
      });
    }
    editor.setDecorations(decorationType, decorations);
  }

  function updateStatusBar(violations: Violation[]): void {
    const score = computeScore(violations);
    const icon = score === 100 ? '$(check)' : score >= 70 ? '$(warning)' : '$(error)';
    statusBar.text = `${icon} Vibes: ${score}/100`;
    statusBar.show();
  }

  function check(doc: vscode.TextDocument): void {
    if (doc.languageId !== 'python') {
      statusBar.hide();
      return;
    }
    execFile('vibe-check', [doc.fileName, '--json'], (_err, stdout) => {
      const editor = vscode.window.visibleTextEditors.find(e => e.document === doc);
      if (!editor) return;
      try {
        const violations: Violation[] = JSON.parse(stdout || '[]');
        applyDecorations(editor, violations);
        updateStatusBar(violations);
      } catch {
        editor.setDecorations(decorationType, []);
      }
    });
  }

  const checkWorkspace = vscode.commands.registerCommand('vibe-checker.checkWorkspace', () => {
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!root) {
      vscode.window.showWarningMessage('No workspace folder open.');
      return;
    }
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.appendLine('Running vibe-check on workspace...\n');
    execFile('vibe-check', [root, '--json'], (_err, stdout) => {
      try {
        const violations: Violation[] = JSON.parse(stdout || '[]');
        const score = computeScore(violations);
        if (violations.length === 0) {
          outputChannel.appendLine('No violations found. Vibes: 100/100 ✓');
          return;
        }
        const byFile = new Map<string, Violation[]>();
        for (const v of violations) {
          const list = byFile.get(v.file) ?? [];
          list.push(v);
          byFile.set(v.file, list);
        }
        for (const [file, vs] of byFile) {
          outputChannel.appendLine(file);
          for (const v of vs) {
            outputChannel.appendLine(`  ${v.line}:${v.col}  ${v.code}  ${v.message}`);
          }
          outputChannel.appendLine('');
        }
        outputChannel.appendLine(`Vibe score: ${score}/100  (${violations.length} violation(s))`);
      } catch {
        outputChannel.appendLine('Failed to parse vibe-check output.');
      }
    });
  });

  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(check),
    vscode.window.onDidChangeActiveTextEditor(e => {
      if (e) check(e.document);
      else statusBar.hide();
    }),
    decorationType,
    statusBar,
    outputChannel,
    checkWorkspace,
  );
}

export function deactivate(): void {}
