import os
import json
import psycopg2
from datetime import datetime
from django.core.wsgi import get_wsgi_application

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adaptive_learning.settings")

# Load Django application
application = get_wsgi_application()

def lambda_handler(event, context):
    print("🚀 Lambda function invoked!")
    print(f"📩 Received Event: {json.dumps(event)}")

    try:
        http_method = event.get("requestContext", {}).get("http", {}).get("method", "")
        if http_method == "OPTIONS":
            print("🔹 Handling OPTIONS request for CORS")
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization"
                },
                "body": json.dumps({"message": "CORS Preflight Successful!"})
            }

        required_env_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Missing environment variables: {', '.join(missing_vars)}")
            }

        print("🛠️ Connecting to the database...")
        with psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"]
        ) as conn:
            with conn.cursor() as cursor:

                if http_method == "POST":
                    print("📡 Processing POST request...")
                    body = json.loads(event.get("body", "{}"))  
                    print(f"📜 Parsed Request Body: {body}")

                    first_name = body.get("first_name")
                    last_name = body.get("last_name")
                    username = body.get("username")
                    email = body.get("email")
                    role = body.get("role")
                    password = body.get("password") 
                    is_superuser = body.get("is_superuser", False) 
                    is_staff = body.get("is_staff", False) 
                    auth0_id = body.get("auth0_id", None)
                    is_active = body.get("is_active", True)  
                    last_login = body.get("last_login", None)  
                    date_joined = body.get("date_joined", datetime.utcnow())  
                    created_at = body.get("created_at", datetime.utcnow())  
                    updated_at = body.get("updated_at", datetime.utcnow())  
                    deleted_at = body.get("deleted_at", None)

                    if not all([first_name, last_name, username, email, role, password]):
                        print("⚠️ Missing required fields!")
                        return {
                            'statusCode': 400,
                            'body': json.dumps("Missing required fields.")
                        }

                    try:
                        print("📝 Preparing to insert data into the database...")
                        cursor.execute(
                            """
                            INSERT INTO users (username, first_name, last_name, email, role, password, is_superuser, is_staff, auth0_id, is_active, last_login, date_joined, created_at, updated_at, deleted_at) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (username, first_name, last_name, email, role, password, is_superuser, is_staff, auth0_id, is_active, last_login, date_joined, created_at, updated_at, deleted_at)
                        )
                        conn.commit()  
                        print("✅ User created successfully in the database!")

                    except psycopg2.Error as insert_err:
                        print(f"💥 Database Insert Error: {str(insert_err)}")
                        return {
                            'statusCode': 500,
                            'body': json.dumps(f"Database Insert Error: {str(insert_err)}")
                        }

                    return {
                        'statusCode': 201,
                        'body': json.dumps("User created successfully.")
                    }

        print("🎉 Lambda function completed successfully!")
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            'body': json.dumps('Hello from AWS Lambda! Django DB Connection Successful. 🚀')
        }
    
    except psycopg2.Error as db_err:
        print(f"💥 Database Error: {str(db_err)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Database Error: {str(db_err)}")
        }
    
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON payload!")
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON payload.")
        }
    
    except Exception as e:
        print(f"🚨 Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Unexpected error: {str(e)}")
        }
