import unittest

from loader import chain


class SimpleCommand(chain.Command):
    @staticmethod
    def is_executable(self, ctx: chain.Context):
        return ctx.has_key("simple")

    @staticmethod
    def execute(self, ctx: chain.Context):
        if self.is_executable(ctx):
            ctx.add_value("simple_out", "test")


class OtherCommand(chain.Command):
    @staticmethod
    def is_executable(self, ctx: chain.Context):
        return ctx.has_key("other")

    @staticmethod
    def execute(self, ctx: chain.Context):
        if self.is_executable(ctx):
            ctx.add_value("other_out", "test")


class ChainTest(unittest.TestCase):
    def test_context(self):
        ctx = chain.Context()
        ctx.add_value("test", "Test Value")
        self.assertTrue(ctx.has_key("test"))
        value = ctx.get_value("test")
        self.assertEqual("Test Value", value)

        self.assertFalse(ctx.has_key("test2"))

    def test_simple_command(self):
        ctx = chain.Context()
        cmd = SimpleCommand()
        cmd.execute(ctx)
        self.assertFalse(ctx.has_key("simple_out"))
        ctx.add_value('simple', True)
        cmd.execute(ctx)
        self.assertTrue(ctx.has_key("simple_out"))

    def test_simple_chain(self):
        ctx = chain.Context()

        chain = chain.BaseChain()

        self.assertFalse(chain.is_executable(ctx))

        chain.add_command(SimpleCommand())
        chain.add_command(OtherCommand())

        self.assertTrue(chain.is_executable(ctx))

        ctx.add_value("simple", True)
        chain.execute(ctx)
        self.assertTrue(ctx.has_key("simple_out"))
        self.assertFalse(ctx.has_key("other_out"))
