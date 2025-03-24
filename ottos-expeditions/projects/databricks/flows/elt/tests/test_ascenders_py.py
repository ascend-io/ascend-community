from ascend.resources import TestResult, ref, singular_test


@singular_test(inputs=[ref("ascenders")], severity="error")
def test_ascenders_py(context, ascenders):
    if ascenders.count().to_pyarrow().as_py() > 0:
        return TestResult("test_ascenders_py", True, TestResult.EMPTY)
    else:
        return TestResult(
            "test_ascenders_py",
            False,
            ascenders,
            "ascenders must be non-empty, please check the data",
        )
