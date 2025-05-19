"""AfterPack

Revision ID: 371437e41c6c
Revises: fe65dff2b2e2
Create Date: 2025-05-13 17:24:26.606817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '371437e41c6c'
down_revision: Union[str, None] = 'fe65dff2b2e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
