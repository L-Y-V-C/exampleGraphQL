from ariadne import QueryType, gql, make_executable_schema, MutationType
from ariadne.asgi import GraphQL

type_defs = gql("""
    type Query {
        student(id: ID!): student
        students: [student]
    }
    type student {
        id: ID!
        name: String!
        surname: String!
        career: String!
        isActive: Boolean!
        averageGrade: Float!
    }
    input inputStudent {
        name: String!
        surname: String!
        career: String!
        isActive: Boolean!
        averageGrade: Float!
    }
    type Mutation {
        addStudent(input: inputStudent!): student
        updateStudent(id: ID!, input: inputStudent!): student
    }
""")

#Datos
students = [
    {
        "id": "1",
        "name": "Luigi",
        "surname": "Valenzuela",
        "career": "CCOMP",
        "isActive": True,
        "averageGrade": 0.1
    },
    {
        "id": "2",
        "name": "Yamil",
        "surname": "Calderon",
        "career": "CCOMP",
        "isActive": False,
        "averageGrade": 0.2
    }
]

query = QueryType()
mutation = MutationType()

@query.field("student")
def resolver_student(_, info, id):
    for student in students:
        if student["id"] == id:
            return student
    return None

@query.field("students")
def resolver_students(_, info):
    return students

@mutation.field("addStudent")
def resolver_add_student(_, info, input):
    new_id = str(len(students) + 1)
    new_student = {
        "id": new_id,
        "name": input["name"],
        "surname": input["surname"],
        "career": input["career"],
        "isActive": input["isActive"],
        "averageGrade": input["averageGrade"]
    }
    students.append(new_student)
    return new_student

@mutation.field("updateStudent")
def resolver_update_student(_, info, id, input):
    for student in students:
        if student["id"] == id:
            student["name"] = input["name"]
            student["surname"] = input["surname"]
            student["career"] = input["career"]
            student["isActive"] = input["isActive"]
            student["averageGrade"] = input["averageGrade"]
    return student

schema = make_executable_schema(type_defs, query, mutation)
app = GraphQL(schema, debug=True)