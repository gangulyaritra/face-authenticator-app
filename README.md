# Face Authentication System using GitHub Actions and Azure Cloud Services.

The problem statement is to design a Face Authentication System to install at high-security places. The solution offers a modern Facial Authentication System using state-of-art **DeepFace** [[Blog]](https://viso.ai/computer-vision/deepface/) [[GitHub]](https://github.com/serengil/deepface) algorithms to detect faces and generate facial embeddings. This system contains endpoints that can be integrated into any device depending on the requirements.

## Project Architecture.
<img width="844" alt="image" src="https://user-images.githubusercontent.com/57321948/195135349-9888d9ea-af5d-4ee2-8aa4-1e57342add05.png">

### Run the Application Server.
Before running the project, install MongoDB Compass in the local system for data storage, export the environment variables, and install the project requirements.
```
python app.py
```

### Build and Run the Docker Image.
```
docker build -t faceapp --build-arg SECRET_KEY=<SECRET_KEY> --build-arg ALGORITHM=<ALGORITHM> --build-arg MONGODB_URL_KEY=<MONGODB_URL_KEY> --build-arg DATABASE_NAME=<DATABASE_NAME> --build-arg USER_COLLECTION_NAME=<USER_COLLECTION_NAME> --build-arg EMBEDDING_COLLECTION_NAME=<EMBEDDING_COLLECTION_NAME> .

docker run -d -p 8080:8080 <IMAGEID OR IMAGENAME>
```

### Services for Deployment.
- Azure Container Registry (ACR) to store Docker Image.
- Azure App Services to deploy the application.
- GitHub Actions for CI/CD Pipeline.

## Authors

- [Aritra Ganguly](https://in.linkedin.com/in/gangulyaritra)

## License & Copyright

© 2022 Aritra Ganguly, iNeuron.ai

Licensed under the [MIT License](LICENSE).