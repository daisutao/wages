"""empty message

Revision ID: 87255adf2722
Revises: 4daaaa5413c6
Create Date: 2018-10-25 14:02:55.811678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87255adf2722'
down_revision = '4daaaa5413c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('salarys', sa.Column('base_funtion', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('basic_performance', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('fixed_overtime', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('housing_allowance', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('position_allowance', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('provident_fund', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('solid_result', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('traffic_allowance', sa.Float(), nullable=True))
    op.add_column('salarys', sa.Column('union_due', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('salarys', 'union_due')
    op.drop_column('salarys', 'traffic_allowance')
    op.drop_column('salarys', 'solid_result')
    op.drop_column('salarys', 'provident_fund')
    op.drop_column('salarys', 'position_allowance')
    op.drop_column('salarys', 'housing_allowance')
    op.drop_column('salarys', 'fixed_overtime')
    op.drop_column('salarys', 'basic_performance')
    op.drop_column('salarys', 'base_funtion')
    # ### end Alembic commands ###