###############################################################################
# _*_ coding: utf-8
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2020, John McNamara, jmcnamara@cpan.org
#
from __future__ import unicode_literals
from ..excel_comparison_test import ExcelComparisonTest
from ...workbook import Workbook


class TestCompareXLSXFiles(ExcelComparisonTest):
    """
    Test file created by XlsxWriter against a file created by Excel.

    """

    def setUp(self):

        self.set_filename('utf8_11.xlsx')

    def test_create_file(self):
        """Test the creation of an XlsxWriter file with utf-8 strings."""

        workbook = Workbook(self.got_filename, {'strings_to_urls': True})

        worksheet = workbook.add_worksheet()

        worksheet.write('A1', '１２３４５')

        workbook.close()

        self.assertExcelEqual()
