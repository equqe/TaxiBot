'use strict';
$('.clockpicker').clockpicker()
            .find('input').change(function(){
        console.log(this.value);
    });
    $('.timeinput1').clockpicker({
        placement: 'bottom',
        align: 'right',
        autoclose: true,
        'default': '20:48'
    });
    $('.timeinput').clockpicker({
    placement: 'bottom',
    align: 'left',
    autoclose: true,
    // 'default': 'now'
});