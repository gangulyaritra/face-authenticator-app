# Face Authentication System using GitHub Actions and Azure Cloud Services.

The problem statement is to design a two-stage Face Authentication System to install at high-security places. The solution offers a modern Facial Authentication System using state-of-art **DeepFace** [[Blog]](https://viso.ai/computer-vision/deepface/) [[GitHub]](https://github.com/serengil/deepface) algorithms (**FaceNet** and **MTCNN**) to detect faces and generate facial embeddings. This system contains endpoints that can be integrated into any device depending on the requirements.

## Project Architecture.
<img width="844" alt="image" src="https://user-images.githubusercontent.com/57321948/195135349-9888d9ea-af5d-4ee2-8aa4-1e57342add05.png">

## Application Setup.
Before running the project, install MongoDB Compass in the local system for data storage. We also need an Azure account to access ACS and App services for deployment.

### Step 1: Install Project Requirements.
```
pip install -r requirements.txt
```

### Step 2: Export the Environment Variables.
```
export SECRET_KEY=KlgH6AzYDeZeGwD288to79I3vTHT8wp7
export ALGORITHM=HS256
export MONGODB_URL_KEY="mongodb+srv://root:root@faceapp.xnby9rw.mongodb.net/?retryWrites=true&w=majority"
export DATABASE_NAME=faceapp
export USER_COLLECTION_NAME=users
export EMBEDDING_COLLECTION_NAME=embeddings
```

### Step 3: Run the Application Server.
```
python app.py
```

### Step 4: Build and Run the Docker Image.
```
docker build -t faceapp --build-arg SECRET_KEY=<SECRET_KEY> --build-arg ALGORITHM=<ALGORITHM> --build-arg MONGODB_URL_KEY=<MONGODB_URL_KEY> --build-arg DATABASE_NAME=<DATABASE_NAME> --build-arg USER_COLLECTION_NAME=<USER_COLLECTION_NAME> --build-arg EMBEDDING_COLLECTION_NAME=<EMBEDDING_COLLECTION_NAME> .

docker run -d -p 8080:8080 <IMAGEID OR IMAGENAME>
```

## Services for Deployment.
- Azure Container Registry (ACR) to store Docker Images.
- Azure App Services to deploy the application.
- GitHub Actions for CI/CD Pipeline.
- Terraform for Infrastructure.

## Authors

- [Aritra Ganguly](https://in.linkedin.com/in/gangulyaritra)

## License & Copyright

© 2022 Aritra Ganguly, iNeuron.ai

Licensed under the [MIT License](LICENSE).