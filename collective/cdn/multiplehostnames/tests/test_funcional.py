# -*- coding:utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.cdn.multiplehostnames.testing import FUNCTIONAL_TESTING

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('browser.txt',
                          package='collective.cdn.multiplehostnames.docs',
                          optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        doctest.DocTestSuite(
            module='collective.cdn.multiplehostnames.provider'
                            ),
    ])
    return suite
