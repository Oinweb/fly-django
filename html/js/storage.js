function saveKeyToStorage(login_type, token){
    if(typeof(Storage) !== "undefined"){
        localStorage.setItem("network",login_type);
        localStorage.setItem("token",token);
    } else {
        alert('No local storage');
    }
}

function saveUserToStorage(acc_id,name,fname,lname,email,img_url){
    localStorage.setItem('acc_id',acc_id);
    localStorage.setItem('name',name);
    localStorage.setItem('fname',fname);
    localStorage.setItem('lname',lname);
    localStorage.setItem('email',email);
    localStorage.setItem('img_url',img_url);
}

function loadUserData(){
    var name = localStorage.getItem('name');
    var img_url = localStorage.getItem('img_url');

    $('.user-image').attr('src',img_url);
    $('.greeting').text('Hello, ' + name);
}

function getXP(){
    var xp = localStorage.getItem("xp");
    var level = localStorage.getItem("level");
}