1. Deploy on Streamlit Cloud (RECOMMENDED)
Step-by-step

Push your latest code to GitHub.

Go to: https://share.streamlit.io/

Sign in with GitHub.

Click “New app”.

Fill the form:

Repository:
soumyamanjeti59/climatescope-project

Branch:
milestone-4

Main file:
app_prototype.py

Click Deploy.

Streamlit Cloud will:

Install dependencies from requirements.txt

Build your app

Give you a public URL to share

2. Deploy on Render (Alternative Free Option)

Go to https://render.com/

Create an account

Click New → Web Service

Connect your GitHub repo

Choose:

Branch: milestone-4

Build Command:

pip install -r requirements.txt


Start Command:

streamlit run app_prototype.py --server.port 10000 --server.address 0.0.0.0


Click Deploy

Render will give you a public link for your app.

3. Run Locally (for testing)
Install dependencies
pip install -r requirements.txt

Run the Streamlit app
streamlit run app_prototype.py


This opens your app at:

http://localhost:8501

🚀 4. Optional: Docker Deployment
Create a file named Dockerfile with this content:
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app_prototype.py", "--server.port=8080", "--server.address=0.0.0.0"]

Build the Docker image:
docker build -t climatescope .

Run the container:
docker run -p 8080:8080 climatescope

Deployment Complete!

You now know how to deploy your dashboard using:

Streamlit Cloud (recommended)

Render

Local machine

Docker (optional)