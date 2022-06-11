let photo = document.getElementById('imgPhoto')
let file = document.getElementById('fullimage')

let firstPhoto = document.getElementById('firstPhoto')
let firstLittleImage = document.getElementById('f1_littleimage')


photo.addEventListener('click', (e) => {
    file.click();
});

file.addEventListener('change', (e) => {

    if (file.files.length <= 0){
        return
    }

    let reader = new FileReader();

    reader.onload = () => {
        photo.src = reader.result;
    }

    reader.readAsDataURL(file.files[0])
})

firstPhoto.addEventListener('click', (e) => {
    firstLittleImage.click();
})

firstLittleImage.addEventListener('change', (e) => {
    if (file.files.length <= 0){
        return
    }
    console.log(file.files)

    let reader = new FileReader();

    reader.onload = () => {
        firstPhoto.src = reader.result;
    }

    reader.readAsDataURL(file.files[0])
})
