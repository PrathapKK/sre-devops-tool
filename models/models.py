import datetime
import decimal
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.orm import  Mapped, relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional


Base = declarative_base()  # ✅ call it, don't subclass it

 


class Applications(Base):
    __tablename__ = 'applications'
    __table_args__ = (
        Index('idx_appID', 'appID'),
        Index('idx_app_type', 'app_type'),
        Index('idx_appname', 'appname')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    appname: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    app_type: Mapped[str] = Column(ENUM('vm_based', 'docker_service', 'kubernetes_service'))
    shortname: Mapped[Optional[str]] = Column(String(30, 'utf8mb4_unicode_ci'))
    appID: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    appsecret: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    app_logs_path: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    error_logs_path: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    port_number: Mapped[Optional[int]] = Column(Integer)
    VIPs: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    wiki_links: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    app_owner_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    app_owner_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    app_owner_contact: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    app_dev_team_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    special_deployment_instructions: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    related_apps_inbound: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    related_apps_outbound: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    associated_dbs: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    application_db_mappings: Mapped[List['ApplicationDbMappings']] = relationship('ApplicationDbMappings', back_populates='application')


class Configurations(Base):
    __tablename__ = 'configurations'
    __table_args__ = (
        Index('idx_config_entity_env', 'config_name', 'entity_type', 'entity_id', 'environment', unique=True),
        Index('idx_config_key', 'config_key'),
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_environment', 'environment')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    config_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    entity_type: Mapped[str] = Column(ENUM('application', 'server', 'database', 'vip', 'microservice'))
    entity_id: Mapped[int] = Column(Integer)
    environment: Mapped[str] = Column(ENUM('DEV', 'SIT', 'QA', 'UAT', 'PROD', 'STAGING'))
    config_type: Mapped[str] = Column(ENUM('environment_var', 'config_file', 'secret', 'system_param', 'feature_flag'))
    config_key: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    config_value: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    is_encrypted: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    is_active: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'1'"))
    version: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    source_path: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    description: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    last_modified_date: Mapped[Optional[datetime.datetime]] = Column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))


class Datacenters(Base):
    __tablename__ = 'datacenters'
    __table_args__ = (
        Index('idx_datacenter_code', 'datacenter_code', unique=True),
        Index('idx_datacenter_name', 'datacenter_name')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    datacenter_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    datacenter_code: Mapped[str] = Column(String(20, 'utf8mb4_unicode_ci'))
    location: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    address: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    contact_person: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    contact_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    contact_phone: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    is_active: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'1'"))
    notes: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    servers: Mapped[List['Servers']] = relationship('Servers', back_populates='datacenter')
    vips: Mapped[List['Vips']] = relationship('Vips', back_populates='datacenter')
    database_servers: Mapped[List['DatabaseServers']] = relationship('DatabaseServers', back_populates='datacenter')
    microservices: Mapped[List['Microservices']] = relationship('Microservices', back_populates='datacenter')


class Deployments(Base):
    __tablename__ = 'deployments'
    __table_args__ = (
        Index('idx_deployment_id', 'deployment_id', unique=True),
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_environment', 'environment'),
        Index('idx_status', 'status')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    deployment_id: Mapped[str] = Column(String(50, 'utf8mb4_unicode_ci'))
    entity_type: Mapped[str] = Column(ENUM('application', 'microservice', 'database'))
    entity_id: Mapped[int] = Column(Integer)
    version: Mapped[str] = Column(String(50, 'utf8mb4_unicode_ci'))
    environment: Mapped[str] = Column(ENUM('DEV', 'SIT', 'QA', 'UAT', 'PROD', 'STAGING'))
    deployment_type: Mapped[str] = Column(ENUM('full', 'rolling', 'blue_green', 'canary', 'hotfix'))
    status: Mapped[Optional[str]] = Column(ENUM('scheduled', 'in_progress', 'completed', 'failed', 'rolled_back'), server_default=text("'scheduled'"))
    start_time: Mapped[Optional[datetime.datetime]] = Column(DateTime)
    end_time: Mapped[Optional[datetime.datetime]] = Column(DateTime)
    duration: Mapped[Optional[int]] = Column(Integer)
    change_ticket: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    build_id: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    pipeline_url: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    performed_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    approved_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    rollback_plan: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    notes: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))


class Incidents(Base):
    __tablename__ = 'incidents'
    __table_args__ = (
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_incident_id', 'incident_id', unique=True),
        Index('idx_severity', 'severity'),
        Index('idx_status', 'status')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    incident_id: Mapped[str] = Column(String(50, 'utf8mb4_unicode_ci'))
    title: Mapped[str] = Column(String(255, 'utf8mb4_unicode_ci'))
    severity: Mapped[str] = Column(ENUM('critical', 'high', 'medium', 'low'))
    entity_type: Mapped[str] = Column(ENUM('application', 'server', 'database', 'vip', 'microservice', 'infrastructure'))
    start_time: Mapped[datetime.datetime] = Column(DateTime)
    description: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    status: Mapped[Optional[str]] = Column(ENUM('open', 'investigating', 'mitigated', 'resolved', 'closed'), server_default=text("'open'"))
    entity_id: Mapped[Optional[int]] = Column(Integer)
    detected_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    end_time: Mapped[Optional[datetime.datetime]] = Column(DateTime)
    resolution_time: Mapped[Optional[int]] = Column(Integer)
    root_cause: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    resolution: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    impact: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    postmortem_link: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))


class MaintenanceWindows(Base):
    __tablename__ = 'maintenance_windows'
    __table_args__ = (
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_status', 'status'),
        Index('idx_time_range', 'start_time', 'end_time')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    window_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    entity_type: Mapped[str] = Column(ENUM('application', 'server', 'database', 'vip', 'microservice', 'datacenter'))
    entity_id: Mapped[int] = Column(Integer)
    start_time: Mapped[datetime.datetime] = Column(DateTime)
    end_time: Mapped[datetime.datetime] = Column(DateTime)
    maintenance_type: Mapped[str] = Column(ENUM('patching', 'upgrade', 'hardware', 'network', 'other'))
    status: Mapped[Optional[str]] = Column(ENUM('scheduled', 'in_progress', 'completed', 'cancelled'), server_default=text("'scheduled'"))
    description: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    impact: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    notification_sent: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    notification_date: Mapped[Optional[datetime.datetime]] = Column(DateTime)
    approved_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    performed_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    change_ticket: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))


class MonitoringConfigs(Base):
    __tablename__ = 'monitoring_configs'
    __table_args__ = (
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_monitor_name', 'monitor_name')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    monitor_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    entity_type: Mapped[str] = Column(ENUM('application', 'server', 'database', 'vip', 'microservice'))
    entity_id: Mapped[int] = Column(Integer)
    monitor_type: Mapped[str] = Column(ENUM('availability', 'performance', 'error_rate', 'latency', 'custom'))
    check_interval: Mapped[Optional[int]] = Column(Integer, server_default=text("'60'"))
    tool_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    metric_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    metric_query: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    threshold_warning: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    threshold_critical: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    notification_channel: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    is_active: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'1'"))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))


class SloTracking(Base):
    __tablename__ = 'slo_tracking'
    __table_args__ = (
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_period', 'period_start_date', 'period_end_date'),
        Index('idx_slo_name', 'slo_name'),
        Index('idx_status', 'status')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    slo_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    entity_type: Mapped[str] = Column(ENUM('application', 'microservice', 'vip'))
    entity_id: Mapped[int] = Column(Integer)
    slo_type: Mapped[str] = Column(ENUM('availability', 'latency', 'error_rate', 'throughput', 'custom'))
    target_percentage: Mapped[decimal.Decimal] = Column(DECIMAL(5, 2))
    measurement_period: Mapped[str] = Column(ENUM('hourly', 'daily', 'weekly', 'monthly', 'quarterly'))
    period_start_date: Mapped[datetime.date] = Column(Date)
    period_end_date: Mapped[datetime.date] = Column(Date)
    current_percentage: Mapped[Optional[decimal.Decimal]] = Column(DECIMAL(5, 2))
    status: Mapped[Optional[str]] = Column(ENUM('met', 'at_risk', 'breached'), server_default=text("'met'"))
    metric_query: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    dashboard_url: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    alert_threshold: Mapped[Optional[decimal.Decimal]] = Column(DECIMAL(5, 2))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))


class Teams(Base):
    __tablename__ = 'teams'
    __table_args__ = (
        Index('idx_manager', 'manager_name'),
        Index('idx_team_name', 'team_name', unique=True)
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    team_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    team_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    team_channel: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    manager_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    manager_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    on_call_rotation: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    pager_duty_id: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    description: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    entity_ownership: Mapped[List['EntityOwnership']] = relationship('EntityOwnership', back_populates='team')


class EntityOwnership(Base):
    __tablename__ = 'entity_ownership'
    __table_args__ = (
        ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_ownership_team'),
        Index('idx_entity', 'entity_type', 'entity_id'),
        Index('idx_entity_team_resp', 'entity_type', 'entity_id', 'team_id', 'responsibility_type', unique=True),
        Index('idx_team', 'team_id')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    entity_type: Mapped[str] = Column(ENUM('application', 'server', 'database', 'vip', 'microservice', 'datacenter'))
    entity_id: Mapped[int] = Column(Integer)
    team_id: Mapped[int] = Column(Integer)
    responsibility_type: Mapped[str] = Column(ENUM('primary', 'secondary', 'development', 'operations', 'security', 'database', 'network'))
    start_date: Mapped[Optional[datetime.date]] = Column(Date)
    end_date: Mapped[Optional[datetime.date]] = Column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    team: Mapped['Teams'] = relationship('Teams', back_populates='entity_ownership')


class Servers(Base):
    __tablename__ = 'servers'
    __table_args__ = (
        ForeignKeyConstraint(['datacenter_id'], ['datacenters.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_server_datacenter'),
        Index('idx_app_id', 'app_id'),
        Index('idx_datacenter', 'datacenter_id'),
        Index('idx_environment', 'environment'),
        Index('idx_server_id', 'server_id', unique=True),
        Index('idx_server_name', 'server_name')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    server_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    server_id: Mapped[str] = Column(String(50, 'utf8mb4_unicode_ci'))
    environment: Mapped[str] = Column(ENUM('DEV', 'SIT', 'QA', 'UAT', 'PROD', 'STAGING'))
    datacenter_id: Mapped[Optional[int]] = Column(Integer)
    datacenter_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    ip_address: Mapped[Optional[str]] = Column(String(45, 'utf8mb4_unicode_ci'))
    os_type: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    os_version: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    cpu_cores: Mapped[Optional[int]] = Column(Integer)
    ram_gb: Mapped[Optional[int]] = Column(Integer)
    storage_gb: Mapped[Optional[int]] = Column(Integer)
    is_virtual: Mapped[Optional[int]] = Column(TINYINT(1))
    status: Mapped[Optional[str]] = Column(ENUM('active', 'maintenance', 'decommissioned', 'reserved'), server_default=text("'active'"))
    provisioned_date: Mapped[Optional[datetime.date]] = Column(Date)
    last_patched_date: Mapped[Optional[datetime.date]] = Column(Date)
    app_id: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    app_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    notes: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    datacenter: Mapped[Optional['Datacenters']] = relationship('Datacenters', back_populates='servers')
    vip_server_mappings: Mapped[List['VipServerMappings']] = relationship('VipServerMappings', back_populates='server')


class Vips(Base):
    __tablename__ = 'vips'
    __table_args__ = (
        ForeignKeyConstraint(['datacenter_id'], ['datacenters.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_vip_datacenter'),
        Index('idx_app_id', 'app_id'),
        Index('idx_datacenter', 'datacenter_id'),
        Index('idx_environment', 'environment'),
        Index('idx_vip_name_address_port', 'vip_name', 'vip_address', 'vip_port', unique=True),
        Index('idx_vip_type', 'vip_type')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    vip_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    vip_address: Mapped[str] = Column(String(45, 'utf8mb4_unicode_ci'))
    vip_type: Mapped[str] = Column(ENUM('LTM', 'GTM'))
    protocol: Mapped[str] = Column(ENUM('HTTP', 'HTTPS', 'TCP', 'UDP', 'FTP', 'OTHER'))
    environment: Mapped[str] = Column(ENUM('DEV', 'SIT', 'QA', 'UAT', 'PROD', 'STAGING'))
    vip_port: Mapped[Optional[int]] = Column(Integer)
    datacenter_id: Mapped[Optional[int]] = Column(Integer)
    persistence_type: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    ssl_profile: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    health_monitor: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    app_id: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    app_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    description: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    is_active: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'1'"))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    datacenter: Mapped[Optional['Datacenters']] = relationship('Datacenters', back_populates='vips')
    database_servers: Mapped[List['DatabaseServers']] = relationship('DatabaseServers', back_populates='vip')
    microservices: Mapped[List['Microservices']] = relationship('Microservices', back_populates='vip')
    vip_server_mappings: Mapped[List['VipServerMappings']] = relationship('VipServerMappings', back_populates='vip')


class DatabaseServers(Base):
    __tablename__ = 'database_servers'
    __table_args__ = (
        ForeignKeyConstraint(['datacenter_id'], ['datacenters.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_db_server_datacenter'),
        ForeignKeyConstraint(['replica_of'], ['database_servers.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_db_server_replica'),
        ForeignKeyConstraint(['vip_id'], ['vips.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_db_server_vip'),
        Index('fk_db_server_replica', 'replica_of'),
        Index('idx_cluster_name', 'cluster_name'),
        Index('idx_datacenter', 'datacenter_id'),
        Index('idx_db_server_id', 'db_server_id', unique=True),
        Index('idx_db_server_name', 'db_server_name'),
        Index('idx_db_type', 'db_type'),
        Index('idx_environment', 'environment'),
        Index('idx_vip', 'vip_id')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    db_server_name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    db_server_id: Mapped[str] = Column(String(50, 'utf8mb4_unicode_ci'))
    db_type: Mapped[str] = Column(ENUM('MySQL', 'PostgreSQL', 'Oracle', 'SQL Server', 'MongoDB', 'Redis', 'Cassandra', 'DynamoDB', 'Other'))
    environment: Mapped[str] = Column(ENUM('DEV', 'SIT', 'QA', 'UAT', 'PROD', 'STAGING'))
    db_version: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    db_port: Mapped[Optional[int]] = Column(Integer)
    datacenter_id: Mapped[Optional[int]] = Column(Integer)
    ip_address: Mapped[Optional[str]] = Column(String(45, 'utf8mb4_unicode_ci'))
    vip_id: Mapped[Optional[int]] = Column(Integer)
    is_primary: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    is_replica: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    replica_of: Mapped[Optional[int]] = Column(Integer)
    is_clustered: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    cluster_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    storage_gb: Mapped[Optional[int]] = Column(Integer)
    backup_schedule: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    backup_retention_days: Mapped[Optional[int]] = Column(Integer)
    maintenance_window: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    status: Mapped[Optional[str]] = Column(ENUM('active', 'maintenance', 'decommissioned', 'reserved'), server_default=text("'active'"))
    owner_team: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    owner_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    datacenter: Mapped[Optional['Datacenters']] = relationship('Datacenters', back_populates='database_servers')
    database_servers: Mapped[Optional['DatabaseServers']] = relationship('DatabaseServers', remote_side=[id], back_populates='database_servers_reverse')
    database_servers_reverse: Mapped[List['DatabaseServers']] = relationship('DatabaseServers', remote_side=[replica_of], back_populates='database_servers')
    vip: Mapped[Optional['Vips']] = relationship('Vips', back_populates='database_servers')
    application_db_mappings: Mapped[List['ApplicationDbMappings']] = relationship('ApplicationDbMappings', back_populates='db_server')
    db_server_ip_mappings: Mapped[List['DbServerIpMappings']] = relationship('DbServerIpMappings', back_populates='db_server')


class Microservices(Base):
    __tablename__ = 'microservices'
    __table_args__ = (
        ForeignKeyConstraint(['datacenter_id'], ['datacenters.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_microservice_datacenter'),
        ForeignKeyConstraint(['vip_id'], ['vips.id'], ondelete='SET NULL', onupdate='CASCADE', name='fk_microservice_vip'),
        Index('idx_app_id', 'app_id'),
        Index('idx_cluster_type', 'cluster_type'),
        Index('idx_datacenter', 'datacenter_id'),
        Index('idx_environment', 'environment'),
        Index('idx_name_environment', 'name', 'environment', unique=True),
        Index('idx_vip', 'vip_id')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(100, 'utf8mb4_unicode_ci'))
    cluster_type: Mapped[str] = Column(ENUM('Docker', 'Kubernetes'))
    environment: Mapped[str] = Column(ENUM('DEV', 'SIT', 'QA', 'UAT', 'PROD', 'STAGING'))
    app_id: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    service_version: Mapped[Optional[str]] = Column(String(50, 'utf8mb4_unicode_ci'))
    vip_id: Mapped[Optional[int]] = Column(Integer)
    cluster_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    namespace: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    datacenter_id: Mapped[Optional[int]] = Column(Integer)
    service_port: Mapped[Optional[int]] = Column(Integer)
    health_endpoint: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    image_repository: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    image_tag: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    replica_count: Mapped[Optional[int]] = Column(Integer, server_default=text("'1'"))
    cpu_limit: Mapped[Optional[str]] = Column(String(20, 'utf8mb4_unicode_ci'))
    memory_limit: Mapped[Optional[str]] = Column(String(20, 'utf8mb4_unicode_ci'))
    config_map: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    secrets: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    service_dependencies: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    api_docs_url: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    owner_team: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    owner_email: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    repo_url: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    ci_cd_pipeline: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    status: Mapped[Optional[str]] = Column(ENUM('active', 'deprecated', 'development', 'maintenance'), server_default=text("'active'"))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    datacenter: Mapped[Optional['Datacenters']] = relationship('Datacenters', back_populates='microservices')
    vip: Mapped[Optional['Vips']] = relationship('Vips', back_populates='microservices')


class VipServerMappings(Base):
    __tablename__ = 'vip_server_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['server_id'], ['servers.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_mapping_server'),
        ForeignKeyConstraint(['vip_id'], ['vips.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_mapping_vip'),
        Index('idx_server', 'server_id'),
        Index('idx_vip', 'vip_id'),
        Index('idx_vip_server', 'vip_id', 'server_id', 'server_port', unique=True)
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    vip_id: Mapped[int] = Column(Integer)
    server_id: Mapped[int] = Column(Integer)
    server_port: Mapped[Optional[int]] = Column(Integer)
    weight: Mapped[Optional[int]] = Column(Integer, server_default=text("'1'"))
    is_active: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'1'"))
    pool_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    node_status: Mapped[Optional[str]] = Column(ENUM('enabled', 'disabled', 'forced_offline'), server_default=text("'enabled'"))
    priority: Mapped[Optional[int]] = Column(Integer, server_default=text("'1'"))
    notes: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    server: Mapped['Servers'] = relationship('Servers', back_populates='vip_server_mappings')
    vip: Mapped['Vips'] = relationship('Vips', back_populates='vip_server_mappings')


class ApplicationDbMappings(Base):
    __tablename__ = 'application_db_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_mapping_application'),
        ForeignKeyConstraint(['db_server_id'], ['database_servers.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_mapping_db_server'),
        Index('idx_app_db', 'application_id', 'db_server_id', 'db_name', unique=True),
        Index('idx_application', 'application_id'),
        Index('idx_db_server', 'db_server_id')
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    application_id: Mapped[int] = Column(Integer)
    db_server_id: Mapped[int] = Column(Integer)
    access_type: Mapped[Optional[str]] = Column(ENUM('read', 'write', 'read_write'), server_default=text("'read_write'"))
    db_name: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    db_schema: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    connection_string: Mapped[Optional[str]] = Column(String(255, 'utf8mb4_unicode_ci'))
    is_primary: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    notes: Mapped[Optional[str]] = Column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    application: Mapped['Applications'] = relationship('Applications', back_populates='application_db_mappings')
    db_server: Mapped['DatabaseServers'] = relationship('DatabaseServers', back_populates='application_db_mappings')


class DbServerIpMappings(Base):
    __tablename__ = 'db_server_ip_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['db_server_id'], ['database_servers.id'], ondelete='CASCADE', onupdate='CASCADE', name='fk_ip_mapping_db_server'),
        Index('idx_db_server', 'db_server_id'),
        Index('idx_db_server_ip', 'db_server_id', 'ip_address', unique=True)
    )

    id: Mapped[int] = Column(Integer, primary_key=True)
    db_server_id: Mapped[int] = Column(Integer)
    ip_address: Mapped[str] = Column(String(45, 'utf8mb4_unicode_ci'))
    is_primary: Mapped[Optional[int]] = Column(TINYINT(1), server_default=text("'0'"))
    purpose: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    created_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))
    updated_by: Mapped[Optional[str]] = Column(String(100, 'utf8mb4_unicode_ci'))

    db_server: Mapped['DatabaseServers'] = relationship('DatabaseServers', back_populates='db_server_ip_mappings')
