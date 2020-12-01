from typing import Type, Dict

import pydantic.utils
from pydantic import BaseModel, create_model
from pydantic.fields import ModelField, UndefinedType


class A(BaseModel):
    x: int
    y: float
    z: str


def dynamic_model():
    return create_model("A", x=(int, ...), y=(float, ...), z=(str, ...))


DYNAMIC_MODEL = dynamic_model()


def get_field_name_to_pydantic_field(model_type: Type[BaseModel]) -> Dict[str, ModelField]:
    return {field.name: field for field in model_type.__fields__.values()}


def assert_model_fields(mf1, mf2):
    assert mf1.type_ is mf2.type_
    assert mf1.name == mf2.name
    assert mf1.default == mf2.default
    assert mf1.required == mf2.required

    if isinstance(mf1.field_info.default, UndefinedType):
        assert isinstance(mf2.field_info.default, UndefinedType)
    else:
        assert mf1.field_info.default == mf2.field_info.default
    assert mf1.field_info.const == mf2.field_info.const
    assert mf1.field_info.extra == mf2.field_info.extra


def test_statically_and_dynamically_created_equivalent_models():
    print(f"\n{pydantic.utils.version_info()}")

    print("\nCreated statically:")
    for n, mf in get_field_name_to_pydantic_field(A).items():
        print(n, mf, mf.default)

    print("\nCreated dynamically:")
    for n, mf in get_field_name_to_pydantic_field(DYNAMIC_MODEL).items():
        print(n, mf, mf.default)

    for field_name in A.__fields__:
        assert_model_fields(A.__fields__[field_name], DYNAMIC_MODEL.__fields__[field_name])


if __name__ == "__main__":
    main()
