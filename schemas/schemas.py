from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.models import (
    Applications, Configurations, Datacenters, Deployments, Incidents,
    MaintenanceWindows, MonitoringConfigs, SloTracking, Teams,
    EntityOwnership, Servers, Vips, DatabaseServers, Microservices,
    VipServerMappings, ApplicationDbMappings, DbServerIpMappings
)


class ApplicationsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Applications
        load_instance = True


class ConfigurationsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Configurations
        load_instance = True


class DatacentersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Datacenters
        load_instance = True


class DeploymentsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Deployments
        load_instance = True


class IncidentsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incidents
        load_instance = True


class MaintenanceWindowsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MaintenanceWindows
        load_instance = True


class MonitoringConfigsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MonitoringConfigs
        load_instance = True


class SloTrackingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SloTracking
        load_instance = True


class TeamsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teams
        load_instance = True


class EntityOwnershipSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EntityOwnership
        load_instance = True


class ServersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Servers
        load_instance = True


class VipsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vips
        load_instance = True


class DatabaseServersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DatabaseServers
        load_instance = True


class MicroservicesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Microservices
        load_instance = True


class VipServerMappingsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VipServerMappings
        load_instance = True


class ApplicationDbMappingsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApplicationDbMappings
        load_instance = True


class DbServerIpMappingsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DbServerIpMappings
        load_instance = True
