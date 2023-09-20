'use strict';
var notify = $.notify('<i class="fa fa-bell-o"></i>Загрузка данных...', {
    type: 'theme',
    allow_dismiss: true,
    delay: 2000,
    showProgressbar: true,
    timer: 300,
    animate:{
        enter:'animated fadeInDown',
        exit:'animated fadeOutUp'
    }
});

setTimeout(function() {
    notify.update('message', `<i class="fa fa-bell-o"></i>Добро пожаловать, ${user.first_name}!`);
}, 1000);
