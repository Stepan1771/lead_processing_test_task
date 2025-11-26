"""initial

Revision ID: b47503f77cba
Revises: 
Create Date: 2025-11-26 10:38:42.356420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b47503f77cba'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_leads'))
    )
    op.create_index(op.f('ix_leads_email'), 'leads', ['email'], unique=True)
    op.create_index(op.f('ix_leads_id'), 'leads', ['id'], unique=False)

    op.create_table('operators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('max_load_limit', sa.Integer(), nullable=False),
    sa.Column('current_load', sa.Integer(), nullable=False),
    sa.Column('competencies', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_operators'))
    )
    op.create_index(op.f('ix_operators_id'), 'operators', ['id'], unique=False)
    op.create_index(op.f('ix_operators_is_active'), 'operators', ['is_active'], unique=False)
    op.create_index(op.f('ix_operators_name'), 'operators', ['name'], unique=False)

    op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sources'))
    )
    op.create_index(op.f('ix_sources_id'), 'sources', ['id'], unique=False)
    op.create_index(op.f('ix_sources_name'), 'sources', ['name'], unique=True)

    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('operator_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('is_distributed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], name=op.f('fk_contacts_lead_id_leads')),
    sa.ForeignKeyConstraint(['operator_id'], ['operators.id'], name=op.f('fk_contacts_operator_id_operators')),
    sa.ForeignKeyConstraint(['source_id'], ['sources.id'], name=op.f('fk_contacts_source_id_sources')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_contacts'))
    )
    op.create_index(op.f('ix_contacts_id'), 'contacts', ['id'], unique=False)
    op.create_index(op.f('ix_contacts_lead_id'), 'contacts', ['lead_id'], unique=False)
    op.create_index(op.f('ix_contacts_operator_id'), 'contacts', ['operator_id'], unique=False)
    op.create_index(op.f('ix_contacts_source_id'), 'contacts', ['source_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_contacts_source_id'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_operator_id'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_lead_id'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_id'), table_name='contacts')
    op.drop_table('contacts')
    op.drop_index(op.f('ix_sources_name'), table_name='sources')
    op.drop_index(op.f('ix_sources_id'), table_name='sources')
    op.drop_table('sources')
    op.drop_index(op.f('ix_operators_name'), table_name='operators')
    op.drop_index(op.f('ix_operators_is_active'), table_name='operators')
    op.drop_index(op.f('ix_operators_id'), table_name='operators')
    op.drop_table('operators')
    op.drop_index(op.f('ix_leads_id'), table_name='leads')
    op.drop_index(op.f('ix_leads_email'), table_name='leads')
    op.drop_table('leads')
