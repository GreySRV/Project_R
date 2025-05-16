"""change_password_to_hash

Revision ID: fe65dff2b2e2
Revises: 8c8ad4772c5c
Create Date: 2025-05-02 16:48:07.981222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe65dff2b2e2'
down_revision: Union[str, None] = '8c8ad4772c5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('clients', 'password', 
                   new_column_name='password_hash',
                   type_=sa.String(128),
                   existing_type=sa.String(50))



def downgrade():
    op.alter_column('clients', 'password_hash',
                   new_column_name='password',
                   type_=sa.String(50),
                   existing_type=sa.String(128))
