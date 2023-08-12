# Flaky Test Code

## Motivation
A package showcasing common examples of flaky tests

## Overview
This package contains a number of tests that are flaky and will fail intermittently. For each flaky test, a reliable counterpart test is provided. 

All of the code is located under the `tests` directory. The package is solely set up to create a cli tool that would walk through the tests and run them but it is not implemented yet.

### Running the tests
To run the tests, instead of using `pytest`, use `python` given each test's main module is executable and would run `pytest` multiple times, with different arguments, plugins and will compute a percent of failures.

For example, to run the `test_flaky.py` test under `tests/inter_test/resource_leak/memory_usage_flaky.csv`, run the following command:

```
python tests/inter_test/resource_leak/memory_usage_flaky.csv/test_flaky.py
```


### Layout
The tests are organized in the following way:
```
tests
├── __init__.py
├── external_resource
│   ├── __init__.py
│   ├── async_wait
│   │   ├── __init__.py
│   │   ├── test_flaky.py
│   │   └── test_reliable.py
│   ├── io
│   ├── network
│   │   ├── __init__.py
│   │   ├── test_flaky.py
│   │   └── test_reliable.py
│   └── time
│       ├── test_flaky.py
│       └── test_reliable.py
├── inter_test
│   ├── __init__.py
│   ├── order_dependence
│   │   ├── __init__.py
│   │   ├── fixture_scoping
│   │   │   ├── __init__.py
│   │   │   ├── test_flaky.py
│   │   │   └── test_reliable.py
│   │   ├── polluted_mock
│   │   │   ├── __init__.py
│   │   │   ├── test_flaky.py
│   │   │   └── test_reliable.py
│   │   └── shared_resource
│   │       ├── __init__.py
│   │       ├── database_isolation
│   │       │   ├── __init__.py
│   │       │   ├── test_flaky.py
│   │       │   └── test_reliable.py
│   │       └── filesystem_conflict
│   │           ├── __init__.py
│   │           ├── test_flaky.py
│   │           └── test_reliable.py
│   └── resource_leak
│       ├── __init__.py
│       ├── memory_usage_flaky.csv
│       ├── memory_usage_flaky.png
│       ├── memory_usage_reliable.csv
│       ├── memory_usage_reliable.png
│       ├── test_flaky.py
│       └── test_reliable.py
└── intra_test
    ├── __init__.py
    ├── concurrency
    │   ├── __init__.py
    │   ├── test_flaky.py
    │   └── test_reliable.py
    ├── floating_point
    │   ├── __init__.py
    │   └── rounding
    │       ├── __init__.py
    │       ├── overflow
    │       │   ├── __init__.py
    │       │   ├── test_flaky.py
    │       │   └── test_reliable.py
    │       └── precision_loss
    │           ├── __init__.py
    │           ├── test_flaky.py
    │           └── test_reliable.py
    ├── randomness
    │   ├── __init__.py
    │   └── algorithmic_non_determinism
    │       ├── __init__.py
    │       ├── test_flaky.py
    │       └── test_reliable.py
    ├── timeout
    │   ├── __init__.py
    │   ├── test_flaky.py
    │   └── test_reliable.py
    └── too_restrictive
        ├── __init__.py
        ├── test_flaky.py
        ├── test_fuzzing.py
        └── test_reliable.py
```

