function logOut() {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = '/logout';
	form.submit();
	log('test')
}
