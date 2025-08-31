# Base image
FROM genai-base:latest

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt /app/requirements.txt

# Install dependencies (cached if requirements.txt unchanged)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the project
COPY . /app

# Expose Gradio port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Start Gradio app
CMD ["python", "-m", "ui.gradio_app"]
