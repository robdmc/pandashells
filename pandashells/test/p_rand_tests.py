#! /usr/bin/env python
from mock import patch, MagicMock
from unittest import TestCase

from pandashells.bin.p_rand import fill_default_mu, main


class TestFillDefaultMu(TestCase):
    def test_normal_mu_default(self):
        args = MagicMock(type=['normal'], mu=None)
        fill_default_mu(args)
        self.assertEqual(args.mu, [0.])

    def test_normal_mu_non_default(self):
        args = MagicMock(type=['normal'], mu=[7.])
        fill_default_mu(args)
        self.assertEqual(args.mu, [7.])

    def test_poisson_mu_default(self):
        args = MagicMock(type=['poisson'], mu=None)
        fill_default_mu(args)
        self.assertEqual(args.mu, [1.])

    def test_poisson_mu_non_default(self):
        args = MagicMock(type=['normal'], mu=[7.])
        fill_default_mu(args)
        self.assertEqual(args.mu, [7.])


class TestMain(TestCase):
    @patch(
        'pandashells.bin.p_rand.sys.argv',
        'p.rand -n 10 -t uniform'.split())
    @patch('pandashells.bin.p_rand.io_lib.df_to_output')
    def test_uniform(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(len(df), 10)
        self.assertTrue(all([x <= 1 for x in df.c0]))
        self.assertTrue(all([x >= 0 for x in df.c0]))

    @patch(
        'pandashells.bin.p_rand.sys.argv',
        'p.rand -n 10 -t normal'.split())
    @patch('pandashells.bin.p_rand.io_lib.df_to_output')
    def test_normal(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(len(df), 10)
        self.assertTrue(df.c0.mean() < 100)
        self.assertTrue(df.c0.mean() > -100)

    @patch(
        'pandashells.bin.p_rand.sys.argv',
        'p.rand -n 10 -t poisson'.split())
    @patch('pandashells.bin.p_rand.io_lib.df_to_output')
    def test_poisson(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(len(df), 10)
        self.assertTrue(all([round(x, 0) == x for x in df.c0]))
        self.assertTrue(all([x >= 0 for x in df.c0]))

    @patch(
        'pandashells.bin.p_rand.sys.argv',
        'p.rand -n 10 -t beta'.split())
    @patch('pandashells.bin.p_rand.io_lib.df_to_output')
    def test_beta(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(len(df), 10)
        self.assertTrue(all([x >= 0 for x in df.c0]))
        self.assertTrue(all([x <= 1 for x in df.c0]))

    @patch(
        'pandashells.bin.p_rand.sys.argv',
        'p.rand -n 10 -t gamma'.split())
    @patch('pandashells.bin.p_rand.io_lib.df_to_output')
    def test_gamma(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(len(df), 10)
        self.assertTrue(all([x >= 0 for x in df.c0]))

    @patch(
        'pandashells.bin.p_rand.sys.argv',
        'p.rand -n 10 -t binomial'.split())
    @patch('pandashells.bin.p_rand.io_lib.df_to_output')
    def test_binomial(self, df_to_output_mock):
        main()
        df = df_to_output_mock.call_args_list[0][0][1]
        self.assertEqual(len(df), 10)
        self.assertTrue(all([round(x, 0) == x for x in df.c0]))
        self.assertTrue(all([x >= 0 for x in df.c0]))
        self.assertTrue(all([x <= 10 for x in df.c0]))
