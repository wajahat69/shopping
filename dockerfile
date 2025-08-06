# ✅ Use official Lambda base image
FROM public.ecr.aws/lambda/python:3.9

# ✅ Set working directory (optional but fine)
WORKDIR /var/task

# ✅ Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# ✅ Copy all files (this includes app.py, templates/, model files, etc.)

COPY . .



# ✅ Set the Lambda handler
CMD ["app.app.handler"]
