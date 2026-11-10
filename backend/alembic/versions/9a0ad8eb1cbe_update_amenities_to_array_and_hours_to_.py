"""update_amenities_to_array_and_hours_to_jsonb

Revision ID: 9a0ad8eb1cbe
Revises: 971a34d3c54f
Create Date: 2026-11-02 06:37:37.834791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9a0ad8eb1cbe'
down_revision: Union[str, Sequence[str], None] = '971a34d3c54f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Convert hours from String(255) to JSONB
    op.alter_column(
        'stores',
        'hours',
        type_=postgresql.JSONB(astext_type=sa.Text()),
        existing_type=sa.String(length=255),
        existing_nullable=True,
        postgresql_using="CASE WHEN hours IS NULL THEN NULL WHEN hours ~ '^\\s*\\{' THEN hours::jsonb ELSE NULL END",
    )
    # Convert amenities from JSON to ARRAY(String)
    op.alter_column(
        'stores',
        'amenities',
        type_=postgresql.ARRAY(sa.String()),
        existing_type=postgresql.JSON(astext_type=sa.Text()),
        existing_nullable=False,
        postgresql_using="translate(amenities::text, '[]', '{}')::text[]",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert amenities from ARRAY(String) to JSON
    op.alter_column(
        'stores',
        'amenities',
        type_=postgresql.JSON(astext_type=sa.Text()),
        existing_type=postgresql.ARRAY(sa.String()),
        existing_nullable=False,
        postgresql_using="to_json(amenities)",
    )
    # Revert hours from JSONB to String(255)
    op.alter_column(
        'stores',
        'hours',
        type_=sa.String(length=255),
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        existing_nullable=True,
        postgresql_using="hours::text",
    )
