### image_face_detector
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/grinat/image_face_detector)

Rest api for face recognitions libs

[Try](https://image-face-detector.herokuapp.com/static/webcam.html)

### Build, deploy, develop
#### Develop
If you havent python3 on your local machine
```
docker-compose up
```
Else
```
pip3 install -r requirements.txt
make dev
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