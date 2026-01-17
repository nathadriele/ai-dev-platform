from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('repository_url', sa.String(), nullable=False),
        sa.Column('tech_stack', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_projects_id', 'projects', ['id'])
    op.create_foreign_key('fk_projects_created_by', 'projects', 'users', ['created_by'], ['id'])

    # Create ai_activities table
    op.create_table(
        'ai_activities',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tool_used', sa.String(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('response', sa.Text(), nullable=True),
        sa.Column('code_changes', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
    )
    op.create_index('ix_ai_activities_id', 'ai_activities', ['id'])
    op.create_index('ix_ai_activities_project_id', 'ai_activities', ['project_id'])
    op.create_index('ix_ai_activities_user_id', 'ai_activities', ['user_id'])
    op.create_foreign_key('fk_ai_activities_project', 'ai_activities', 'projects', ['project_id'], ['id'])
    op.create_foreign_key('fk_ai_activities_user', 'ai_activities', 'users', ['user_id'], ['id'])

    # Create agent_executions table
    op.create_table(
        'agent_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('agent_type', sa.String(), nullable=False),
        sa.Column('task_description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('input_data', postgresql.JSON(), nullable=True),
        sa.Column('output_data', postgresql.JSON(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
    )
    op.create_index('ix_agent_executions_id', 'agent_executions', ['id'])
    op.create_index('ix_agent_executions_project_id', 'agent_executions', ['project_id'])
    op.create_foreign_key('fk_agent_executions_project', 'agent_executions', 'projects', ['project_id'], ['id'])

    # Create pipeline_executions table
    op.create_table(
        'pipeline_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pipeline_name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('commit_sha', sa.String(), nullable=False),
        sa.Column('branch', sa.String(), nullable=False),
        sa.Column('triggered_by', sa.String(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('test_results', postgresql.JSON(), nullable=True),
        sa.Column('deployment_url', sa.String(), nullable=True),
    )
    op.create_index('ix_pipeline_executions_id', 'pipeline_executions', ['id'])
    op.create_index('ix_pipeline_executions_project_id', 'pipeline_executions', ['project_id'])
    op.create_foreign_key('fk_pipeline_executions_project', 'pipeline_executions', 'projects', ['project_id'], ['id'])

    # Create mcp_servers table
    op.create_table(
        'mcp_servers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('server_type', sa.String(), nullable=False),
        sa.Column('endpoint', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('capabilities', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('last_health_check', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_mcp_servers_id', 'mcp_servers', ['id'])


def downgrade() -> None:
    op.drop_table('mcp_servers')
    op.drop_table('pipeline_executions')
    op.drop_table('agent_executions')
    op.drop_table('ai_activities')
    op.drop_table('projects')
    op.drop_table('users')
