export function init() {
    const ace_editor = ace.edit("editor");
    ace_editor.setTheme("ace/theme/chrome");
    ace_editor.session.setMode("ace/mode/nginx");
    ace_editor.setOptions({
        autoScrollEditorIntoView: true,
        copyWithEmptySelection: true,
    });
    return ace_editor;
}