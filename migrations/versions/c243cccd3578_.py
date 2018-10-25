"""empty message

Revision ID: c243cccd3578
Revises: 87255adf2722
Create Date: 2018-10-25 16:26:20.185981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c243cccd3578'
down_revision = '87255adf2722'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('salarys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee', sa.String(length=10), nullable=False),
    sa.Column('account', sa.String(length=20), nullable=True),
    sa.Column('base_funtion', sa.Float(), nullable=True),
    sa.Column('basic_performance', sa.Float(), nullable=True),
    sa.Column('solid_result', sa.Float(), nullable=True),
    sa.Column('housing_allowance', sa.Float(), nullable=True),
    sa.Column('position_allowance', sa.Float(), nullable=True),
    sa.Column('fixed_overtime', sa.Float(), nullable=True),
    sa.Column('traffic_allowance', sa.Float(), nullable=True),
    sa.Column('provident_fund', sa.Float(), nullable=True),
    sa.Column('union_due', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_salarys_employee'), 'salarys', ['employee'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_salarys_employee'), table_name='salarys')
    op.drop_table('salarys')
    # ### end Alembic commands ###