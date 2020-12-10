# pyruicore

[![Build Status](https://travis-ci.com/RuiCoreSci/pyruicore.svg?branch=master)](https://travis-ci.com/RuiCoreSci/pyruicore) &nbsp; [![Coverage Status](https://coveralls.io/repos/github/RuiCoreSci/pyruicore/badge.svg?branch=master)](https://coveralls.io/github/RuiCoreSci/pyruicore?branch=master) &nbsp; [![codebeat badge](https://codebeat.co/badges/af92f04f-6d5e-4a0a-82c6-53a8bcfb0341)](https://codebeat.co/projects/github-com-ruicoresci-pyruicore-master) &nbsp; ![python3.8](https://img.shields.io/badge/language-python3.8-blue.svg) &nbsp; ![issues](https://img.shields.io/github/issues/RuiCoreSci/pyruicore) ![stars](https://img.shields.io/github/stars/RuiCoreSci/pyruicore) &nbsp; ![license](https://img.shields.io/github/license/RuiCoreSci/pyruicore)

* This package is used to load python dict data to python class.

## Usage

* pip install pyruicore -i https://pypi.org/simple

```py


from pyruicore import BaseModel, Field


class Department(BaseModel):
    name: str
    address: str


class User(BaseModel):
    age: int = Field(default_factory=lambda: 1)
    departs: List[Department]


user = User(
    departs=[
        {"name": "de1", "address": "address1"},
        Department(name="2", address="address2"),
    ]
)
user_dict = user.dict()
"""
user_dict = {
    "age": 1,
    "departs": [
        {"name": "de1", "address": "address1"},
        {"name": "2", "address": "address2"},
    ]
}
"""

```

##  Maintainers

[@ruicore](https://github.com/ruicore)

## Contributing

PRs are accepted, this is first workout version, may have many bugs, so welcome to point out bugs and fix it.

## License

MIT © 2020 ruicore
