from flask import Blueprint, request, jsonify, render_template
from database import db
import schemas.schemas as all_schemas
import models.models as all_models

import inspect
import logging
import uuid  # Add this import

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Blueprint
api = Blueprint("api", __name__)

# Step 1: Get all SQLAlchemy model classes
model_classes = {
    name: cls for name, cls in inspect.getmembers(all_models)
    if inspect.isclass(cls) and hasattr(cls, "__tablename__")
}

# Step 2: Get all Marshmallow schema classes
schema_classes = {
    name: cls for name, cls in inspect.getmembers(all_schemas)
    if inspect.isclass(cls) and name.endswith("Schema")
}

# Step 3: Build schema_map automatically
schema_map = {}
for model_name, model_class in model_classes.items():
    schema_name = f"{model_name}Schema"
    schema_class = schema_classes.get(schema_name)
    if schema_class:
        schema_map[model_class] = schema_class
        logger.info(f"Registered model <{model_name}> with schema <{schema_name}>")
    else:
        logger.warning(f"Schema not found for model: {model_name}")

# --- Register CRUD Routes ---
def register_crud_routes(model, schema_class, table_name):
    """
    Dynamically create route handler functions with unique names
    """
    schema = schema_class()
    schema_many = schema_class(many=True)

    logger.info(f"Registering routes for: {table_name}")

    def generate_unique_view_name(prefix):
        """
        Generate a unique view function name to prevent endpoint conflicts
        """
        return f"{prefix}_{table_name}_{str(uuid.uuid4()).replace('-', '_')}"

    # List items route
    list_func_name = generate_unique_view_name('list')
    list_view_func = lambda: jsonify(schema_many.dump(db.session.query(model).all()))
    list_view_func.__name__ = list_func_name
    api.add_url_rule(f"/{table_name}", methods=["GET"], view_func=list_view_func, endpoint=list_func_name)

    # Get single item route
    get_func_name = generate_unique_view_name('get')
    def get_view_func(item_id):
        item = db.session.get(model, item_id)
        if not item:
            return jsonify({"message": f"{table_name[:-1].capitalize()} not found"}), 404
        return jsonify(schema.dump(item))
    get_view_func.__name__ = get_func_name
    api.add_url_rule(f"/{table_name}/<int:item_id>", methods=["GET"], view_func=get_view_func, endpoint=get_func_name)

    # Create item route
    create_func_name = generate_unique_view_name('create')
    def create_view_func():
        item = schema.load(request.json, session=db.session)
        db.session.add(item)
        db.session.commit()
        return jsonify(schema.dump(item)), 201
    create_view_func.__name__ = create_func_name
    api.add_url_rule(f"/{table_name}", methods=["POST"], view_func=create_view_func, endpoint=create_func_name)

    # Update item route
    update_func_name = generate_unique_view_name('update')
    def update_view_func(item_id):
        item = db.session.get(model, item_id)
        if not item:
            return jsonify({"message": f"{table_name[:-1].capitalize()} not found"}), 404
        updated = schema.load(request.json, instance=item, session=db.session)
        db.session.commit()
        return jsonify(schema.dump(updated))
    update_view_func.__name__ = update_func_name
    api.add_url_rule(f"/{table_name}/<int:item_id>", methods=["PUT"], view_func=update_view_func, endpoint=update_func_name)

    # Delete item route
    delete_func_name = generate_unique_view_name('delete')
    def delete_view_func(item_id):
        item = db.session.get(model, item_id)
        if not item:
            return jsonify({"message": f"{table_name[:-1].capitalize()} not found"}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": f"{table_name[:-1].capitalize()} deleted"})
    delete_view_func.__name__ = delete_func_name
    api.add_url_rule(f"/{table_name}/<int:item_id>", methods=["DELETE"], view_func=delete_view_func, endpoint=delete_func_name)

# Dynamically register all schemas in the schema_map
for model_class, schema_class in schema_map.items():
    table_name = model_class.__tablename__
    register_crud_routes(model_class, schema_class, table_name)

# --- UI Route ---
@api.route("/ui/<entity_name>")
def crud_ui(entity_name):
    schema_class = schema_map.get(entity_name)
    if not schema_class:
        return f"Unknown entity: {entity_name}", 404

    schema = schema_class()
    return render_template("crud.html", schema=schema, entity_name=entity_name)