"""test_data

Revision ID: 93eff9737391
Revises: b47503f77cba
Create Date: 2025-11-26 11:40:37.889994

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.models import Source

# revision identifiers, used by Alembic.
revision: str = '93eff9737391'
down_revision: Union[str, Sequence[str], None] = 'b47503f77cba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Вставляем источники
    op.bulk_insert(
        sa.table('sources',
                 sa.column('name', sa.String),
                 sa.column('is_active', sa.Boolean)
                 ),
        [
            {'name': 'Telegram Bot', 'is_active': True},
            {'name': 'ВКонтакте', 'is_active': True},
            {'name': 'WhatsApp Business', 'is_active': True},
            {'name': 'Сайт форма', 'is_active': True},
        ]
    )

    # Вставляем операторов
    op.bulk_insert(
        sa.table('operators',
                 sa.column('name', sa.String),
                 sa.column('is_active', sa.Boolean),
                 sa.column('max_load_limit', sa.Integer),
                 sa.column('current_load', sa.Integer),
                 sa.column('competencies', sa.JSON)
                 ),
        [
            {
                "name": "Анна",
                "is_active": True,
                "max_load_limit": 10,
                "current_load": 0,
                "competencies": {"1": 1.5, "2": 1.2}
            },
            {
                "name": "Иван",
                "is_active": True,
                "max_load_limit": 8,
                "current_load": 0,
                "competencies": {"3": 1.8, "4": 1.0}
            },
            {
                "name": "Мария",
                "is_active": True,
                "max_load_limit": 12,
                "current_load": 0,
                "competencies": {"1": 1.0, "2": 1.0, "3": 1.0, "4": 1.0}
            },
        ]
    )

    # Вставляем лидов
    op.bulk_insert(
        sa.table('leads',
                 sa.column('email', sa.String)
                 ),
        [
            {
                'email': 'dmitry.volkov@example.com'
            },
            {
                'email': 'olga.smirnova@example.com'
            },
            {
                'email': 'alexey.novikov@example.com'
            },
        ]
    )

    # Вставляем обращения
    op.bulk_insert(
        sa.table('contacts',
                 sa.column('lead_id', sa.Integer),
                 sa.column('source_id', sa.Integer),
                 sa.column('status', sa.String),
                 sa.column('is_distributed', sa.Boolean),
                 ),
        [
            {
                'lead_id': 1,
                'source_id': 1,
                'status': 'new',
                'is_distributed': False
            },
            {
                'lead_id': 2,
                'source_id': 2,
                'status': 'new',
                'is_distributed': False
            },
            {
                'lead_id': 3,
                'source_id': 3,
                'status': 'new',
                'is_distributed': False
            },
        ]
    )


def downgrade() -> None:
    # Удаляем тестовые данные
    conn = op.get_bind()

    # Удаляем обращения
    op.execute("DELETE FROM contacts")

    # Удаляем лидов
    op.execute("DELETE FROM leads")

    # Удаляем операторов
    op.execute("DELETE FROM operators")

    # Удаляем источники
    op.execute("DELETE FROM sources")