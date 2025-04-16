from database import db
from flask import Blueprint, request, jsonify
from models.models import (
    Applications, Configurations, Datacenters, Deployments, Incidents,
    MaintenanceWindows, MonitoringConfigs, SloTracking, Teams,
    EntityOwnership, Servers, Vips, DatabaseServers, Microservices,
    VipServerMappings, ApplicationDbMappings, DbServerIpMappings
)
from schemas.schemas import (
    ApplicationsSchema, ConfigurationsSchema, DatacentersSchema, DeploymentsSchema, IncidentsSchema,
    MaintenanceWindowsSchema, MonitoringConfigsSchema, SloTrackingSchema, TeamsSchema,
    EntityOwnershipSchema, ServersSchema, VipsSchema, DatabaseServersSchema, MicroservicesSchema,
    VipServerMappingsSchema, ApplicationDbMappingsSchema, DbServerIpMappingsSchema
)


# Setup Blueprint
api = Blueprint("api", __name__)

# Helper function to generate routes dynamically
from flask import jsonify

# Helper function to generate routes dynamically
def register_crud_routes(model, schema_class, name):
    schema = schema_class()
    schema_many = schema_class(many=True)

    def list_items():
        items = db.session.query(model).all()
        return jsonify(schema_many.dump(items))
    list_items.__name__ = f"list_{name}"
    api.route(f"/{name}", methods=["GET"])(list_items)
    print(f"Registered GET /{name}")

    def get_item(item_id):
        item = db.session.get(model, item_id)
        if not item:
            return jsonify({"message": f"{name[:-1].capitalize()} not found"}), 404
        return jsonify(schema.dump(item))
    get_item.__name__ = f"get_{name}"
    api.route(f"/{name}/<int:item_id>", methods=["GET"])(get_item)
    print(f"Registered GET /{name}/<id>")

    def create_item():
        item = schema.load(request.json, session=db.session)
        db.session.add(item)
        db.session.commit()
        return jsonify(schema.dump(item)), 201
    create_item.__name__ = f"create_{name}"
    api.route(f"/{name}", methods=["POST"])(create_item)
    print(f"Registered POST /{name}")

    def update_item(item_id):
        item = db.session.get(model, item_id)
        if not item:
            return jsonify({"message": f"{name[:-1].capitalize()} not found"}), 404
        updated = schema.load(request.json, instance=item, session=db.session)
        db.session.commit()
        return jsonify(schema.dump(updated))
    update_item.__name__ = f"update_{name}"
    api.route(f"/{name}/<int:item_id>", methods=["PUT"])(update_item)
    print(f"Registered PUT /{name}/<id>")

    def delete_item(item_id):
        item = db.session.get(model, item_id)
        if not item:
            return jsonify({"message": f"{name[:-1].capitalize()} not found"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": f"{name[:-1].capitalize()} deleted"})
    delete_item.__name__ = f"delete_{name}"
    api.route(f"/{name}/<int:item_id>", methods=["DELETE"])(delete_item)
    print(f"Registered DELETE /{name}/<id>")




# Register all routes
register_crud_routes(Applications, ApplicationsSchema, "applications")
register_crud_routes(Configurations, ConfigurationsSchema, "configurations")
register_crud_routes(Datacenters, DatacentersSchema, "datacenters")
register_crud_routes(Deployments, DeploymentsSchema, "deployments")
register_crud_routes(Incidents, IncidentsSchema, "incidents")
register_crud_routes(MaintenanceWindows, MaintenanceWindowsSchema, "maintenance_windows")
register_crud_routes(MonitoringConfigs, MonitoringConfigsSchema, "monitoring_configs")
register_crud_routes(SloTracking, SloTrackingSchema, "slo_tracking")
register_crud_routes(Teams, TeamsSchema, "teams")
register_crud_routes(EntityOwnership, EntityOwnershipSchema, "entity_ownership")
register_crud_routes(Servers, ServersSchema, "servers")
register_crud_routes(Vips, VipsSchema, "vips")
register_crud_routes(DatabaseServers, DatabaseServersSchema, "database_servers")
register_crud_routes(Microservices, MicroservicesSchema, "microservices")
register_crud_routes(VipServerMappings, VipServerMappingsSchema, "vip_server_mappings")
register_crud_routes(ApplicationDbMappings, ApplicationDbMappingsSchema, "application_db_mappings")
register_crud_routes(DbServerIpMappings, DbServerIpMappingsSchema, "db_server_ip_mappings")
