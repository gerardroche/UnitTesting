import sys

import sublime
import sublime_plugin

from .test_coverage import UnitTestingCoverageCommand


class UnitTestingCurrentPackageCommand(sublime_plugin.WindowCommand):

    def run(self):
        print('UnitTesting: DEPRECATED command; use unit_testing_test_suite instead')
        self.window.run('unit_testing_test_suite')


# TODO This is DEPRECATED and should be REMOVED; Use `unit_testing_test_suite with args {'coverage': true}` instead.
# TODO Refactor UnitTestingCurrentPackageCoverageCommand code into new command unit_testing_test_suite
class UnitTestingCurrentPackageCoverageCommand(UnitTestingCoverageCommand):

    def run(self):
        project_name = self.current_package_name
        if not project_name:
            sublime.message_dialog("Cannot determine package name.")
            return

        super(UnitTestingCurrentPackageCoverageCommand, self).run(project_name)

    def is_enabled(self):
        return "coverage" in sys.modules


# TODO This is DEPRECATED and should be REMOVED; Use `unit_testing_test_file with args {'coverage': true}` instead.
# TODO Refactor UnitTestingCurrentFileCoverageCommand code into new command unit_testing_test_file
class UnitTestingCurrentFileCoverageCommand(UnitTestingCoverageCommand):

    def run(self):
        project_name = self.current_package_name
        if not project_name:
            sublime.message_dialog("Cannot determine package name.")
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

        super(UnitTestingCurrentFileCoverageCommand, self).run("{}:{}".format(project_name, test_file))

    def is_enabled(self):
        return "coverage" in sys.modules


class UnitTestingCurrentFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        print('UnitTesting: DEPRECATED command; use unit_testing_test_file instead')
        self.window.run('unit_testing_test_file')
