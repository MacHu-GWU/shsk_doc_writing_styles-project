# -*- coding: utf-8 -*-

from shsk_doc_writing_styles import api


def test():
    _ = api


if __name__ == "__main__":
    from shsk_doc_writing_styles.tests import run_cov_test

    run_cov_test(
        __file__,
        "shsk_doc_writing_styles.api",
        preview=False,
    )
