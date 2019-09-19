const API_URL = ''

function onDeviceError() {
    webCamFallback.style.display = 'block'
    webCamBlock.style.display = 'none'
    imageInp.addEventListener('change', handleChange)
}

function handleChange(e) {
    const f = getFileFromEvt(e)
    if (!f) return

    uploadFile(f)
}

async function uploadFile(blob) {
    if (uploading) {
        return
    }

    lockUploading()

    try {
        const fd = new FormData()
        fd.append('image', blob)

        const land = await fetch(API_URL + '/api/v1/face-landmarks', {
            method: 'POST',
            body: fd
        }).then(r => r.json())
        if (land.message) {
            throw new Error(land.message)
        }
        imageLandmarks.src = land.image

        const locs = await fetch(API_URL + '/api/v1/face-locations', {
            method: 'POST',
            body: fd
        }).then(r => r.json())
        if (locs.message) {
            throw new Error(locs.message)
        }
        imageLocations.src = locs.images[0]

    } catch (e) {
        alert(e.toString())
    } finally {
        unLockUploading()
    }
}

function handleTakeScreen() {
    const canvas = document.createElement('canvas')
    canvas.height = video.videoHeight
    canvas.width = video.videoWidth
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
    canvas.toBlob(uploadFile)
}

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true})
        .then(stream => video.srcObject = stream)
        .catch(e => onDeviceError())
    takeScreen.addEventListener('click', handleTakeScreen)
} else {
    onDeviceError()
}