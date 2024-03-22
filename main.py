from fastapi import FastAPI
from ariadne import make_executable_schema,load_schema_from_path
from ariadne.asgi import GraphQL
from resolvers import query, mutation

app = FastAPI()
type_defs=load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, query, mutation)

graphql_app = GraphQL(schema, debug=True)

app.add_route("/graphql", graphql_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)