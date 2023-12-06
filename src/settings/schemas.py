

from typing import Annotated

from pydantic_core import MultiHostUrl
from pydantic.networks import UrlConstraints


SqliteDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=False,
        allowed_schemes=[
            'sqlite',
        ],
    ),
]