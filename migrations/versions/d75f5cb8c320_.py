"""empty message

Revision ID: d75f5cb8c320
Revises: c08cf7341410
Create Date: 2023-11-19 00:40:25.257319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd75f5cb8c320'
down_revision = 'c08cf7341410'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('poke', schema=None) as batch_op:
        batch_op.drop_column('poke_added')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('poke', schema=None) as batch_op:
        batch_op.add_column(sa.Column('poke_added', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
