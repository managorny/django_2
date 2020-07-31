window.onload = function () {
    $('.basket_list').on('change', 'input[type=number]', function (event) {
//        console.log(event.target);
        $.ajax({
            url: '/basket/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                $('.basket_list').html(data.result);
                console.log(data.result);
//                $('.total_q')[0].innerHTML = data['total_quantity'];
//                $('.total_c')[0].innerHTML = data['total_cost'];
//                console.log($('.basket_record')[0].childNodes);
            }
        });
    })
};
