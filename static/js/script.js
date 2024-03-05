
let compressedBlob;

function compressImage(imgToCompress, quality, max_retries = 30) {
    let current_retries = 0;
    let div = document.createElement('div');

    function compressWithRetry() {
        return new Promise((resolve, reject) => {
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");



            const width = imgToCompress.width;
            const height = imgToCompress.height;
            canvas.width = width;
            canvas.height = height;

            context.drawImage(imgToCompress, 0, 0, width, height);

            canvas.toBlob(
                (blob) => {
                    if (blob) {
                        compressedBlob = blob;
                        imgToCompress.src = URL.createObjectURL(blob);
                        resolve();
                    } else {
                        current_retries++;
                        if (current_retries <= max_retries) {
                            console.log(`Retrying compression (attempt ${current_retries})...`);
                            // idk why this is necessary but it doesn't work on moblie without this line
                            document.getElementById('image-div').innerHTML += '';
                            compressWithRetry().then(resolve).catch(reject);
                        } else {
                            reject(`maximum retries (${max_retries}) exceeded.`);
                        }
                    }
                },
                "image/jpeg",
                quality
            );
        });
    }

    // Return the Promise from compressWithRetry
    return compressWithRetry();
}

function previewImage(event) {
    document.getElementById('submit-button').style.display = "none";
    document.getElementById('image-div').style.display = "block";
    document.getElementById('loading-image').style.display = 'block';
    var input = event.target;
    var preview = document.getElementById('recipe-image');

    var reader = new FileReader();
    reader.onload = function () {
        preview.src = reader.result;

        // Call compressImage and wait for it to complete before showing the image
        compressImage(preview, quality = .2)
            .then(() => {
                document.getElementById('loading-image').style.display = 'none';
                document.getElementById('recipe-image').style.display = "block";
                document.getElementById('submit-button').style.display = "block";
            })
            .catch(error => {
                console.error(error);
                document.getElementById('loading-image').style.display = 'none';
                document.getElementById('image-div').innerHTML = '<p>Error compressing image:' + error + '</p>';

                // Handle error, e.g., show an alert to the user
            });
    };
    reader.readAsDataURL(input.files[0]);
}

function MaybeGetProperty(property, json) {
    if (json.hasOwnProperty(property)) {
        return json[property]
    }
    return ''
}
function makeLink(url) {
    var div = document.createElement('div');
    var h2 = document.createElement('h2');
    h2.innerText = 'Link for mealie:';
    div.appendChild(h2);
    var container = document.createElement('container');
    container.style.display = 'flex';
    container.style.flexDirection = 'row';
    var p = document.createElement('p');
    p.textContent = url;
    p.id = 'recipe-page-link';

    var button = document.createElement('button');
    button.classList.add('copy-link-button');
    button.textContent = '\u2398';
    button.addEventListener('click', function (e) {
        e.preventDefault();
        var textToCopy = document.getElementById('recipe-page-link').innerText;
        var tempTextarea = document.createElement('textarea');
        tempTextarea.value = textToCopy;

        // Append the textarea to the body
        document.body.appendChild(tempTextarea);

        // Select and copy the text from the textarea
        tempTextarea.select();
        document.execCommand('copy');

        // Remove the temporary textarea
        document.body.removeChild(tempTextarea);

        // Inform the user that the text has been copied
        alert('Text has been copied to the clipboard: ' + textToCopy);
    });
    container.appendChild(p);
    container.appendChild(button);
    div.append(container);
    return div;
}

function makeSingleField(title, content) {
    var div = document.createElement('div');
    var strong = document.createElement('strong');
    strong.innerText = title;
    div.appendChild(strong);
    div.innerHTML += ': ' + content;
    return div;
}
function createListItem(content) {
    var item = document.createElement('li');
    var p = document.createElement('p');
    p.innerText = content;
    item.appendChild(p);
    return item;
}
function makeList(title, entries) {
    var list = document.createElement('ul');
    if (entries) {
        for (var entry of entries) {
            list.appendChild(createListItem(entry));
        }
    }
    var label = document.createElement('h2');
    label.textContent = title;
    var div = document.createElement('div');
    div.appendChild(label);
    div.appendChild(list);
    return div;
}
function makeRecipeDisplay(recipe, recipe_link) {
    var display = document.createElement('div');
    display.classList.add('recipe-display');
    display.appendChild(makeLink(recipe_link));
    var name = document.createElement('h2');
    name_str = MaybeGetProperty('name', recipe);
    name.innerText = name_str ? name_str : '<I> Couln\t find name </I>';
    display.appendChild(name);
    for (var field of ['description', 'total_time', 'servings']) {
        display.appendChild(makeSingleField(field, MaybeGetProperty(field, recipe)));
    }
    for (var field of ['ingredients', 'steps']) {
        display.appendChild(makeList(field, MaybeGetProperty(field, recipe)));
    }




    return display;
}

function showLoading() {
    document.getElementById('loading-recipe').style.display = 'block';
}
// TODO: Convert this to a function and on onSubmit so the js can go in the head
document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('result').innerHTML = '';
    document.getElementById('recipe-div').style.display = 'block';
    showLoading();

    var formData = new FormData();
    formData.append("image", compressedBlob);
    const advanced_options = {
        'fake_call': String(document.getElementById('fakeCallCheckbox').checked),
    };
    formData.append("advanced_options", JSON.stringify(advanced_options));


    fetch('http://fishpoopsoup.com/extract_recipe/process_image', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading-recipe').style.display = 'none';
            if (data.hasOwnProperty('error_message')) {
                document.getElementById('result').innerHTML = '<p><b>Error in python</b>: ' + data.error_message + '</p>';
                return;
            }
            document.getElementById('result').appendChild(makeRecipeDisplay(JSON.parse(data.recipe), data.recipe_link));
        })
        .catch(error => {
            document.getElementById('loading-recipe').style.display = 'none';
            console.error('Error parsing JSON:', error);
            document.getElementById('result').innerHTML = '<p>Error parsing JSON:' + error + '</p>';
        });
});


