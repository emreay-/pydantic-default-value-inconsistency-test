# pydantic-default-value-inconsistency-test

For bug report: https://github.com/samuelcolvin/pydantic/issues/2165

It seems `pydantic` sets the default value of a required field of a statically created model as `None`. This was the case until `v1.7.2` for the required fields of dynamically created models. However with the `v1.7.3` there seems to be an inconsistent behaviour where the default value for the required fields of dynamically created models are set to be `Ellipsis`. I'm not aware whether this was intentional, or consistent behaviour between statically and dynamically created models is sought after but I wanted to point that out in case it is a regression.

To run the tests with different pydantic versions:
```
PYDANTIC_VERSION=<desired_version> make run
```

eg.:

```
 PYDANTIC_VERSION=1.7.2 make run
```

The output for `pydantic==1.7.2` (warnings are pytest cache warnings):
```
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /
collected 1 item                                                                                                                                                                                                  

pydantic_default_issue.py 
             pydantic version: 1.7.2
            pydantic compiled: True
                 install path: /usr/local/lib/python3.8/site-packages/pydantic
               python version: 3.8.6 (default, Nov 25 2020, 02:47:44)  [GCC 8.3.0]
                     platform: Linux-5.6.0-1033-oem-x86_64-with-glibc2.2.5
     optional deps. installed: []

Created statically:
x name='x' type=int required=True None
y name='y' type=float required=True None
z name='z' type=str required=True None

Created dynamically:
x name='x' type=int required=True None
y name='y' type=float required=True None
z name='z' type=str required=True None
.

========================================================================================== 1 passed, 2 warnings in 0.05s ==========================================================================================
```

The output for `pydantic==1.7.3` (warnings are pytest cache warnings):
```
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.8.6, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
rootdir: /
collected 1 item                                                                                                                                                                                                  

pydantic_default_issue.py 
             pydantic version: 1.7.3
            pydantic compiled: True
                 install path: /usr/local/lib/python3.8/site-packages/pydantic
               python version: 3.8.6 (default, Nov 25 2020, 02:47:44)  [GCC 8.3.0]
                     platform: Linux-5.6.0-1033-oem-x86_64-with-glibc2.2.5
     optional deps. installed: []

Created statically:
x name='x' type=int required=True None
y name='y' type=float required=True None
z name='z' type=str required=True None

Created dynamically:
x name='x' type=int required=True Ellipsis
y name='y' type=float required=True Ellipsis
z name='z' type=str required=True Ellipsis
F

==================================================================================================== FAILURES =====================================================================================================
____________________________________________________________________________ test_statically_and_dynamically_created_equivalent_models ____________________________________________________________________________

    def test_statically_and_dynamically_created_equivalent_models():
        print(f"\n{pydantic.utils.version_info()}")
    
        print("\nCreated statically:")
        for n, mf in get_field_name_to_pydantic_field(A).items():
            print(n, mf, mf.default)
    
        print("\nCreated dynamically:")
        for n, mf in get_field_name_to_pydantic_field(DYNAMIC_MODEL).items():
            print(n, mf, mf.default)
    
        for field_name in A.__fields__:
>           assert_model_fields(A.__fields__[field_name], DYNAMIC_MODEL.__fields__[field_name])

pydantic_default_issue.py:51: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

mf1 = ModelField(name='x', type=int, required=True), mf2 = ModelField(name='x', type=int, required=True)

    def assert_model_fields(mf1, mf2):
        assert mf1.type_ is mf2.type_
        assert mf1.name == mf2.name
>       assert mf1.default == mf2.default
E       AssertionError: assert None == Ellipsis
E        +  where None = ModelField(name='x', type=int, required=True).default
E        +  and   Ellipsis = ModelField(name='x', type=int, required=True).default

pydantic_default_issue.py:28: AssertionError
============================================================================================= short test summary info =============================================================================================
FAILED pydantic_default_issue.py::test_statically_and_dynamically_created_equivalent_models - AssertionError: assert None == Ellipsis
========================================================================================== 1 failed, 3 warnings in 0.07s ==========================================================================================
```
