function loginFacebook() {
    FB.login(function(){
        // Note: The call will only work if you accept the permission request
        FB.getLoginStatus(function(response){
            if(response.status === 'connected'){
                saveKeyToStorage('facebook',response.authResponse.accessToken);
            }
        })
        FB.api(
            '/me',
            'GET',
            {"fields":"name,first_name,last_name,email"},
            function(response) {
                console.log(JSON.stringify(response));
                saveUserToStorage(
                    response['id'],
                    response['name'],
                    response['first_name'],
                    response['last_name'],
                    response['email'],
                    'http://graph.facebook.com/' + response['id'] + '/picture?type=normal'
                );
                window.location="dashboard.html";
            }
        );
    }, {scope: 'email,publish_actions'});
}