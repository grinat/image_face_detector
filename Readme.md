### image_face_detector
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/grinat/image_face_detector)

Rest api for face recognitions libs

[Try](https://image-face-detector.herokuapp.com/static/webcam.html)

[Swagger Docs](https://image-face-detector.herokuapp.com/api/v1/docs/)

### Build, deploy, develop
#### Develop
```
pip3 install -r requirements.txt
make dev
```
Or with docker-compose
```
docker-compose up
```

#### Build docker image
```
make build-docker-image
make run-docker-image # run image
```

#### Without docker
```
pip3 install -r requirements.txt
make prod
```