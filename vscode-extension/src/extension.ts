import * as vscode from 'vscode';
import { execFile } from 'child_process';

interface Violation {
  file: string; line: number; col: number;
  code: string; message: string;
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

  function check(doc: vscode.TextDocument): void {
    if (doc.languageId !== 'python') return;
    execFile('vibe-check', [doc.fileName, '--json'], (_err, stdout) => {
      const editor = vscode.window.visibleTextEditors.find(e => e.document === doc);
      if (!editor) return;
      try {
        const violations: Violation[] = JSON.parse(stdout || '[]');
        applyDecorations(editor, violations);
      } catch {
        editor.setDecorations(decorationType, []);
      }
    });
  }

  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(check),
    vscode.window.onDidChangeActiveTextEditor(e => { if (e) check(e.document); }),
    decorationType,
  );
}

export function deactivate(): void {}
