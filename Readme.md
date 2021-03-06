### image_face_detector
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/grinat/image_face_detector)

Rest api for face recognitions lib: [https://github.com/ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)

[Webcam example](https://image-face-detector.herokuapp.com/static/webcam.html) | [Compare example](https://image-face-detector.herokuapp.com/static/compare.html)

[Swagger Docs](https://image-face-detector.herokuapp.com/api/v1/docs/)

### Usage
Run api on http://localhost:5001
```
docker run -d -p 5001:5001 grinat0/image_face_detector
```
Open http://localhost:5001/api/v1/docs/ and see avalaible methods

Open http://localhost:5001/static/webcam.html or Open http://localhost:5001/static/compare.html and see examples

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

### Testing
```
make unittest
```
or
```
python -m unittest
```