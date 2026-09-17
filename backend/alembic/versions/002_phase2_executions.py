"""phase2_executions

Revision ID: 002_phase2_executions
Revises: 001_initial_schema
Create Date: 2026-09-14 22:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '002_phase2_executions'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Campaign Executions Table
    op.create_table(
        'campaign_executions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('campaign_id', sa.String(length=36), nullable=False),
        sa.Column('workspace_id', sa.String(length=36), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('idempotency_key', sa.String(length=100), nullable=False),
        sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('max_retries', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('n8n_execution_id', sa.String(length=100), nullable=True),
        sa.Column('n8n_workflow_id', sa.String(length=100), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('agent_trace', sa.JSON(), nullable=False),
        sa.Column('trigger_source', sa.String(length=50), nullable=False, server_default='manual_ui'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaign_executions_campaign_id'), 'campaign_executions', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_campaign_executions_workspace_id'), 'campaign_executions', ['workspace_id'], unique=False)
    op.create_index(op.f('ix_campaign_executions_status'), 'campaign_executions', ['status'], unique=False)
    op.create_index(op.f('ix_campaign_executions_idempotency_key'), 'campaign_executions', ['idempotency_key'], unique=True)
    op.create_index(op.f('ix_campaign_executions_n8n_execution_id'), 'campaign_executions', ['n8n_execution_id'], unique=False)

    # 2. Execution Steps Table
    op.create_table(
        'execution_steps',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('execution_id', sa.String(length=36), nullable=False),
        sa.Column('step_name', sa.String(length=100), nullable=False),
        sa.Column('step_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('output_data', sa.JSON(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['execution_id'], ['campaign_executions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_execution_steps_execution_id'), 'execution_steps', ['execution_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_execution_steps_execution_id'), table_name='execution_steps')
    op.drop_table('execution_steps')

    op.drop_index(op.f('ix_campaign_executions_n8n_execution_id'), table_name='campaign_executions')
    op.drop_index(op.f('ix_campaign_executions_idempotency_key'), table_name='campaign_executions')
    op.drop_index(op.f('ix_campaign_executions_status'), table_name='campaign_executions')
    op.drop_index(op.f('ix_campaign_executions_workspace_id'), table_name='campaign_executions')
    op.drop_index(op.f('ix_campaign_executions_campaign_id'), table_name='campaign_executions')
    op.drop_table('campaign_executions')
