import sublime
import sublime_plugin
from .utils import is_python_scope, send_request
from .console_logging import getLogger


class PythonCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return is_python_scope(self.view, self.view.sel()[0].begin())

    @property
    def logger(self):
        return getLogger(__name__)


class BicycleRepairRenameCommand(PythonCommand):
    def __init__(self, *args, **kwargs):
        super(BicycleRepairRenameCommand, self).__init__(*args, **kwargs)
        self.caption = "Please enter a new name"

    def run(self, edit):
        initial_text = ""
        self.view.window().show_input_panel(
            self.caption, initial_text, self.on_done, None, None
        )

    def on_done(self, new_name):
        line, column = self.view.rowcol(self.view.sel()[0].begin())
        filename = self.view.file_name()
        kwargs = dict(
            filename=filename,
            line=line + 1,
            column=column + 1,
            new_name=new_name
        )
        self.logger.debug("rename({0})".format(kwargs))
        send_request('rename', self.view, kwargs, self.on_response)

    def on_response(self, view, content):
        if not content:
            # TODO
            return

        window = view.window()
        for file_name, line, column in content:
            # join to /path/to/file.py:10:30
            full_path = ':'.join([file_name, str(line), str(column + 1)])
            window.open_file(full_path, sublime.ENCODED_POSITION)


class BicycleRepairUndoLastRefactoringCommand(PythonCommand):
    def run(self, edit):
        message = (
            "Undoes the last refactoring? \n\n"
            "!!! WARNING !!! \n"
            "This is dangerous if files was modified since the last refactoring"
        )
        if sublime.ok_cancel_dialog(message, "Confirm"):
            send_request('undo', self.view, {}, self.on_response)

    def on_response(self, view, content):
        if not content:
            # TODO
            return

        if content == "UndoStackEmptyException":
            sublime.message_dialog("Bicycle Repair Man could not did undo")

        window = view.window()
        for file_name in content:
            window.open_file(file_name)
