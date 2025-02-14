# ✅ Use the AWS Lambda Python 3.10 base image
FROM public.ecr.aws/lambda/python:3.10

# ✅ Set the working directory inside Lambda
WORKDIR ${LAMBDA_TASK_ROOT}

# ✅ Copy only requirements.txt first (for caching efficiency)
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# ✅ Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# ✅ Copy the entire Django project
COPY . ${LAMBDA_TASK_ROOT}/

# ✅ Set up Lambda handler (correctly reference `django_lambda.py`)
CMD ["django_lambda.lambda_handler"]

