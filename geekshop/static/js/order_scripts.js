"use strict";

let _quantity, _price, orderitemNum, deltaQuantity, orderitemQuantity, deltaCost;
let quantityArr = [];
let priceArr = [];
let $orderTotalQuantityDOM;

// $('.order_total_quantity').html(''); TODO: переделать все под чистый JS.
// document.querySelector('.order_total_quantity').innerHTML = '';

let totalForms;
let orderTotalQuantity;
let orderTotalCost;
let $orderForm;


function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
//        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _quantity = parseInt(document.querySelector('input[name="orderitems-' + i + '-quantity"]').value);
//        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        if (document.querySelector('.orderitems-' + i + '-price')) {
            _price = parseFloat(document.querySelector('.orderitems-' + i + '-price').outerText.replace(',', '.')); // or innerText
        }
        quantityArr[i] = _quantity;
        priceArr[i] = (_price) ? _price : 0;
    }
}

function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
    deltaCost = orderitemPrice * deltaQuantity;
    orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
    orderTotalQuantity = orderTotalQuantity + deltaQuantity;

    $('.order_total_cost').html(orderTotalCost.toString());
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
}

function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;
    orderitemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderitemNum];
    orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
}

function updateTotalQuantity() {
    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $('.order_total_cost').html(Number(orderTotalCost.toFixed(2)).toString());
}

window.onload = function () {
    $orderTotalQuantityDOM = $('.order_total_quantity');
    totalForms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text()) || 0;
    orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;
    $orderForm = $('.order_form');

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm.on('change', 'input[type="number"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (priceArr[orderitemNum]) {
            orderitemQuantity = parseInt(event.target.value);
            deltaQuantity = orderitemQuantity - quantityArr[orderitemNum];
            quantityArr[orderitemNum] = orderitemQuantity;
            orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
        }
    });

    $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderitemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderitemNum];
        } else {
            deltaQuantity = quantityArr[orderitemNum];
        }
        orderSummaryUpdate(priceArr[orderitemNum], deltaQuantity);
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    // $orderForm.on('change', 'select', function (event) {
    //     let target = event.target;
    //     console.log(target);
    // console.log(event.target.parentNode.parentNode.childNodes[5]);
    // });

    $orderForm.on('change', 'select', function (event) {
        let oderItemIndex = parseInt(event.target.name.replace('orderitems-', '').replace('-product'));
        let productPk = event.target.value;
        $.ajax({
            url: '/product/detail/' + productPk + '/async/',
            success: function (data) {
                priceArr[oderItemIndex] = parseFloat(data.product_price);
                if (isNaN(quantityArr[oderItemIndex])) {
                    quantityArr[oderItemIndex] = 1;
                }
                let priceHtml = '<span>' +
                    data.product_price.toString().replace('.', ',') +
                    '</span> руб';
                let currentTR = $('.order_form table').find('tr:eq(' + (oderItemIndex + 1) + ')');
                currentTR.find('td:eq(2)').html(priceHtml);
                let $productQuantity = currentTR.find('input[type="number"]');
                if (!$productQuantity.val() || isNaN($productQuantity.val()) || $productQuantity.val(0)) {
                    $productQuantity.val(1);
                }
                orderSummaryUpdate(
                    priceArr[oderItemIndex],
                    parseInt($productQuantity.val()));
            }
        });
    });
};
