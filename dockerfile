FROM public.ecr.aws/lambda/python:3.11

# Copy your requirements and app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your FastAPI app code
COPY . .

# Install required packages for FastAPI + Jinja
RUN pip install fastapi uvicorn jinja2 joblib numpy pandas

# Set handler (AWS Lambda expects a handler format file.function)
CMD ["main.handler"]
