"""add_notification_models

Revision ID: add_notification_models
Revises: 
Create Date: 2026-02-07 18:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_notification_models'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create contact_messages table
    op.create_table(
        'contact_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('phone', sa.String(20), default=''),
        sa.Column('company', sa.String(150), default=''),
        sa.Column('subject', sa.String(200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('newsletter', sa.Boolean(), default=False),
        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index(op.f('ix_contact_messages_email'), 'contact_messages', ['email'], unique=False)
    op.create_index(op.f('ix_contact_messages_is_read'), 'contact_messages', ['is_read'], unique=False)
    op.create_index(op.f('ix_contact_messages_created_at'), 'contact_messages', ['created_at'], unique=False)
    
    # Create consultation_requests table
    op.create_table(
        'consultation_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('company', sa.String(150), default=''),
        sa.Column('subject', sa.String(200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('preferred_date', sa.String(20), nullable=False),
        sa.Column('preferred_time', sa.String(20), nullable=False),
        sa.Column('newsletter', sa.Boolean(), default=False),
        sa.Column('cart_items', sa.Text()),
        sa.Column('is_read', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index(op.f('ix_consultation_requests_email'), 'consultation_requests', ['email'], unique=False)
    op.create_index(op.f('ix_consultation_requests_is_read'), 'consultation_requests', ['is_read'], unique=False)
    op.create_index(op.f('ix_consultation_requests_created_at'), 'consultation_requests', ['created_at'], unique=False)


def downgrade():
    op.drop_table('consultation_requests')
    op.drop_table('contact_messages')
