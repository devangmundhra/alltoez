__author__ = 'devangmundhra'

from pipeline.compilers.less import LessCompiler
from pipeline.compilers.coffee import CoffeeScriptCompiler


class FixedLessCompiler(LessCompiler):

    def is_outdated(self, *args, **kwargs):
        try:
            super(FixedLessCompiler, self).is_outdated(*args, **kwargs)
        except AttributeError:
            return True


class FixedCoffeeScriptCompiler(CoffeeScriptCompiler):

    def is_outdated(self, *args, **kwargs):
        try:
            super(FixedCoffeeScriptCompiler, self).is_outdated(*args, **kwargs)
        except AttributeError:
            return True