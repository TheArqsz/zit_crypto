function logOut() {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = '/in/logout';
	form.submit();
}

function hashDecode() {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'get';
    form.action = '/in/hash/decode';
	form.submit();
}

function hashEncode() {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'get';
    form.action = '/in/hash/encode';
	form.submit();
}

function archCrack() {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'get';
    form.action = '/in/arch';
	form.submit();
}

function mainPage() {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'get';
    form.action = '/in/home';
	form.submit();
}

Filevalidation = () => { 
    const fi = document.getElementById('file'); 
    if (fi.files.length > 0) { 
        for (const i = 0; i <= fi.files.length - 1; i++) { 
            const fsize = fi.files.item(i).size; 
            const file = Math.round((fsize / 1024)); 
            const maxSizeMb = 15
            const maxSizeKb = maxSizeMb * 1024;
            if (file >= maxSizeKb) { 
                alert( 
                  "Your file is too big, please select a file less than " + maxSizeMb + "Mb"); 
                fi.value = ''
            } else { 
                continue; 
            } 
        } 
    } 
} 

function checkUser(){
    if(confirm('Do you want to continue deleting your account?')){
        var form = document.createElement('form');
        document.body.appendChild(form);
        form.method = 'delete';
        form.action = '/in/deleteUser';
        form.submit();
    }
}

function settings(){
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'get';
    form.action = '/in/settings';
	form.submit();
}

// function Filevalidation(elem) {
//     document.cookie = `filesize=${elem.files[0].size}`;
// }