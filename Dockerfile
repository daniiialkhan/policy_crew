#setting the python version
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages that you put in requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt
RUN crewai install
# RUN export AZURE_OPENAI_API_KEY=0e9ed2d9da074270bb01aaea2b18f2b1
# RUN export AZURE_OPENAI_ENDPOINT=https://ragresume.openai.azure.com/
# RUN export model=azure/gpt-35-turbo
# RUN export MODEL=azure/gpt-35-turbo
# RUN export AZURE_API_KEY=0e9ed2d9da074270bb01aaea2b18f2b1
# RUN export AZURE_API_BASE=https://ragresume.openai.azure.com/ 
# RUN export AZURE_API_VERSION=2024-08-01-preview
# RUN export OPENAI_API_BASE=https://ragresume.openai.azure.com/ 

# Expose port 8501 for the Streamlit app
EXPOSE 8501

ENV model=azure/gpt-35-turbo
ENV MODEL=azure/gpt-35-turbo
ENV AZURE_API_KEY=0e9ed2d9da074270bb01aaea2b18f2b1
ENV AZURE_API_BASE=https://ragresume.openai.azure.com/ 
ENV AZURE_API_VERSION=2024-08-01-preview
ENV OPENAI_API_BASE=https://ragresume.openai.azure.com/ 
ENV AZURE_ENDPOINT=https://ragresume.openai.azure.com/ 
ENV AZURE_OPENAI_API_KEY=0e9ed2d9da074270bb01aaea2b18f2b1
ENV API_KEY=0e9ed2d9da074270bb01aaea2b18f2b1

# Define the command to run the app (this will run inside the container)
CMD ["streamlit", "run", "streamlit_app.py"]
