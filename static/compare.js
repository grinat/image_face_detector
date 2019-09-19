const API_URL = ''
let images = []

imageHaystack.addEventListener('change', function (e) {
    const f = getFileFromEvt(e)
    if (!f) return

    uploadToHaystack(f)
})

imageNeedle.addEventListener('change', function (e) {
    const f = getFileFromEvt(e)
    if (!f) return

    uploadNeedle(f)
})

async function uploadToHaystack(blob) {
    if (uploading) {
        return
    }

    lockUploading()

    try {
        const fd = new FormData()
        fd.append('image', blob)

        const enc = await fetch(API_URL + '/api/v1/face-encodings', {
            method: 'POST',
            body: fd
        }).then(r => r.json())
        if (enc.message) {
            throw new Error(enc.message)
        }

        const img = await blobToBase64(blob)

        images.push({
            img: img,
            code: enc.face_encodings_list[0]
        })
        // reset same flag
        images = images.map(img => ({...img, isSame: false}))

        renderImages()
    } catch (e) {
        alert(e.toString())
    } finally {
        unLockUploading()
    }
}

async function uploadNeedle(blob) {
    if (uploading) {
        return
    }

    try {
        await uploadToHaystack(blob)
        const lastIndex = images.length - 1
        const haystack = []
        for (const {code} of images) {
            haystack.push(code)
        }

        lockUploading()

        const fd = new FormData()
        fd.append('image', blob)

        const comp = await fetch(API_URL + '/api/v1/compare-faces', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                haystack: haystack,
                needle: images[lastIndex].code
            })
        }).then(r => r.json())
        if (comp.message) {
            throw new Error(comp.message)
        }

        comp.faces.forEach((isSame, i) => {
            images[i].isSame = isSame
        })

        renderImages()

    } catch (e) {
        alert(e.toString())
    } finally {
        unLockUploading()
    }
}

function renderImages() {
    let str = ''
    for (const {img, code, isSame} of images) {
        str += `
            <div class="image-container">
                <img src="${img}">
                <div>isSame: ${isSame}</div>
                <div>
                    <textarea>${code}</textarea>
                </div>
            </div>
            `
    }

    document.getElementById('images').innerHTML = str
}