import os

import sublime
import sublime_plugin

from .test_package import UnitTestingCommand


class UnitTestingTestSuiteCommand(UnitTestingCommand):

    # Run test suite of the current file.

    def run(self, coverage=False):
        if coverage:
            # TODO Refactor unit_testing_current_suite_coverage (which is deprecated) code into this command.
            return sublime.active_window().run_command('unit_testing_current_suite_coverage')

        project_name = self.current_package_name
        if not project_name:
            sublime.message_dialog("Cannot determine package name.")
            return

        sublime.set_timeout_async(
            lambda: super(UnitTestingTestSuiteCommand, self).run(project_name))

    def unit_testing(self, stream, package, settings):
        parent = super(UnitTestingTestSuiteCommand, self)
        if settings["reload_package_on_testing"]:
            self.reload_package(
                package, dummy=True, show_reload_progress=settings["show_reload_progress"])

        sublime.set_timeout(lambda: parent.unit_testing(stream, package, settings))


class UnitTestingTestFileCommand(UnitTestingCommand):

    # Run tests for the current file. If the current file is not a test file, it
    # runs tests of the test file for the current file.

    def run(self, coverage=False):
        if coverage:
            # TODO Refactor unit_testing_current_file_coverage (which is deprecated) code into this command.
            return sublime.active_window().run_command('unit_testing_current_file_coverage')

        project_name = self.current_package_name
        if not project_name:
            sublime.message_dialog('Cannot determine package name.')
            return

        test_file = self.current_test_file
        if not test_file:

            # If the test file is empty the test run will error woth message
            # like: "ERROR: Start directory is not importable:
            # '/path/to/st/Packages/PackageName:/tests'"
            sublime.message_dialog('Cannot determine test file name.')
            return

        if not test_file.startswith('test_'):
            test_file = 'test_' + test_file

        sublime.set_timeout_async(
            lambda: super(UnitTestingTestFileCommand, self).run(
                '{}:{}'.format(project_name, test_file)))

    def unit_testing(self, stream, package, settings):
        parent = super(UnitTestingTestFileCommand, self)
        if settings["reload_package_on_testing"]:
            self.reload_package(
                package, dummy=True, show_reload_progress=settings["show_reload_progress"])

        sublime.set_timeout(lambda: parent.unit_testing(stream, package, settings))


class UnitTestingTestNearestCommand(sublime_plugin.WindowCommand):

    # Run a test nearest to the cursor (supports multiple selections). If the
    # current file is not a test file, it runs tests of the test file for the
    # current file.

    def run(self):
        # TODO Should run the nearest test; Currently just proxies to test_file.
        self.window.run_command('test_file')


class UnitTestingTestLastCommand(sublime_plugin.WindowCommand):

    # Run the last test.

    def run(self):
        raise NotImplementedError('TODO {} not implemented yet'.format(self.__class__.__name__))


class UnitTestingTestVisitCommand(sublime_plugin.WindowCommand):

    # Open the last run test in the current window (useful when you're trying to
    # make a test pass, and you dive deep into application code and close your
    # test buffer to make more space, and once you've made it pass you want to
    # go back to the test file to write more tests).

    def run(self):
        raise NotImplementedError('TODO {} not implemented yet'.format(self.__class__.__name__))


def _get_switchable(window):
    view = window.active_view()
    if not view:
        print('UnitTesting: view not found')
        return

    file_name = view.file_name()
    if not file_name:
        print('UnitTesting: file name not found')
        return

    if not file_name.endswith('.py'):
        return

    # We need to evaluate the realpath of the file in order to mutate it to and
    # from test -> file and file -> test.
    file_name = os.path.realpath(file_name)

    for package in os.listdir(sublime.packages_path()):
        p_path = os.path.join(sublime.packages_path(), package)
        if file_name.startswith(p_path):
            if os.path.isdir(p_path):
                f_path, f_base = os.path.split(file_name)

                if f_base.startswith('test_'):
                    # Switch from test -> file
                    switch_to_file = os.path.join(
                        f_path.replace(os.path.join(p_path, 'tests'), os.path.join(p_path)),
                        f_base[5:])
                else:
                    # Switch from file -> test
                    switch_to_file = os.path.join(
                        f_path.replace(p_path, os.path.join(p_path, 'tests')),
                        'test_' + f_base)

                # Checks to see if the file we're switching to is already open,
                # and takes into account symlinks i.e. if we didn't do this then
                # we would end up opening a second view with the realpath file
                # rather than opening the symlinked one.
                for view in window.views():
                    if view.file_name():
                        if os.path.realpath(view.file_name()) == switch_to_file:
                            return view.file_name()

                if os.path.isfile(switch_to_file):
                    return switch_to_file


class UnitTestingTestSwitchCommand(sublime_plugin.WindowCommand):

    # Switch between the nearest test module and module under test.

    def run(self):
        switchable = _get_switchable(self.window)
        if switchable:
            self.window.open_file(switchable)


class UnitTestingTestResultsCommand(sublime_plugin.WindowCommand):

    # Show the test results panel.

    def run(self):
        self.window.run_command('show_panel', {'panel': 'output.UnitTesting'})


class UnitTestingTestCancelCommand(sublime_plugin.WindowCommand):

    # Cancel current test run.

    def run(self):
        raise NotImplementedError('TODO {} not implemented yet'.format(self.__class__.__name__))
