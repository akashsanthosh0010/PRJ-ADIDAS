$(".add-to-cart-btn").on('click',function(){
    let this_val = $(this)
    let index = this_val.attr('data-index')

    let quantity = $('.product-quantity-' + index ).val()
    let product_title = $('.product-title-' + index).val()
    let product_id = $('.product-id-' + index).val()
    let product_stock_count = $('.product-stock-count-' + index).val()
    let product_price = $('.current-product-price-' + index).text()
    let product_pid = $('.product-pid-' + index).val()
    let product_image = $('.product-image-' + index).val()
    



    
    

    console.log('Quantity:', quantity)
    console.log('Title:', product_title)
    console.log('Product id:', product_id)
    console.log('Product pid:', product_pid)
    console.log('Product stock:', product_stock_count)
    console.log('Product image:', product_image)
    console.log('Index:', index)
    console.log('Product price:', product_price)
    console.log('Current Element:', this_val)

    $.ajax({
        url: '/product_cart', 
        data:{
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
            'stock_count': product_stock_count,

        }, 
        dataType : 'json',
        beforeSend : function(){
            console.log('Adding product to cart')
        },
        success : function(response){
            this_val.html('<i class="fa-solid fa-check"></i>')
            console.log('Added product to cart')
            $('.cart-items-count').text(response.totalcartitems)


        }
    })


    
    



})


$(".delete-product").on('click', function(){
    
    let product_id = $(this).attr('data-product')
    let this_val = $(this)


    console.log('product id:', product_id);

    $.ajax({
        url: '/delete-from-cart',
        data : {
                'id': product_id
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide()
        }, 
        success: function(response){
            this_val.show()
            $('.cart-items-count').text(response.totalcartitems)
            $('#cart-list').html(response.data)
        }

        
        })


})



// $(".update-product").on('click', function(){
    
//     let product_id = $(this).attr('data-product')
//     let this_val = $(this)
//     let product_quantity = $('.product-qty-' + product_id).val()


//     console.log('product id:', product_id)
//     console.log('product qty:', product_quantity)


//     $.ajax({
//         url: '/update-cart',
//         data : {
//                 'id': product_id, 
//                 'qty': product_quantity,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             this_val.hide()
//         }, 
//         success: function(response){
//             this_val.show()
//             $('.cart-items-count').text(response.totalcartitems)
//             $('#cart-list').html(response.data)
//         }

        
//         })


// })

// Assuming you have buttons with classes 'increment-button' and 'decrement-button'
function decrementValue(p_id) {
    var quantityInput = document.querySelector('.product-qty-' + p_id);
    var value = Number(quantityInput.value);
    value = isNaN(value) ? 0 : value;
    console.log('Before decrement: ' + value);
    if (value > 0) {
        value--;
        console.log('after decrement: ' + value);
        quantityInput.value = value;
        console.log('after decrement: ' + value);
        
    }
    updateCart(p_id, value)
}



function incrementValue(p_id) {
    var quantityInput = document.querySelector('.product-qty-' + p_id);
    var value = parseInt(quantityInput.value, 10);
    value = isNaN(value) ? 0 : value;
    console.log(document.getElementById('product-stock-' + p_id));
    var stockCount = parseInt(document.getElementById('product-stock-' + p_id).value, 10);


    
    console.log('Before increment: ' + value);
    console.log('Before stock: ' + stockCount);


    if (stockCount != value) {
        value++;
        quantityInput.value = value;
        console.log('After increment: ' + value);
        console.log('After stock: ' + stockCount);


        // Update the total price and make the AJAX call
        
        updateCart(p_id, value);
    } else {
        alert("This product is out of stock")
        console.log('Stock count is insufficient. Cannot increment.');
        // You can display an error message to the user here
    }
}


function updateCart(product_id, new_quantity) {
    console.log("product id :" , product_id);
    console.log("product qty :" , new_quantity);
    $.ajax({
        url: '/update-cart',
        data: {
            'id': product_id,
            'qty': new_quantity,
        },
        dataType: 'json',
        beforeSend: function () {
            // You can add loading indicators or disable buttons during the request
        },
        success: function (response) {
            // Update other elements on the page after successful update
            $('.cart-items-count').text(response.totalcartitems);
            console.log(response.data);
            $('#cart-list').html(response.data);
        },
        error: function () {
            // Handle errors if needed
            alert('Error updating quantity. Please try again.');
        }
    });
}





$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox has been clicked");

        let filter_object = {}

        let min_price = $('#max_price').attr('min')
        let max_price = $('#max_price').val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;


        $('.filter-checkbox').each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data('filter')

            // console.log('filter value is:', filter_value);
            // console.log('filter key is:', filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key +']:checked')).map(function(element){
                return element.value
            })
        })
        console.log('Filter object is :', filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('Trying to filter product...');
            },
            success: function(response){
                console.log(response);
                console.log('Data filtered successfully...');
                $('#filtered-product').html(response.data)


            }
        })
    })

    $('#max_price').on('blur', function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()


        // console.log('current price is: ', current_price);
        // console.log('min price is: ', min_price);
        // console.log('max price is: ', max_price);


        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            // console.log('Error Occured');

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            // console.log('max price is: ', max_Price);
            // console.log('min price is: ', min_Price);


            alert('Price must be between $' +min_price + ' and $' +max_price)
            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()

            return false
            


            
        } 
    })
})


$(document).on('click', '.make-default-address', function(){
    let id = $(this).attr('data-address-id')
    let this_val = $(this)

    console.log('ID is :', id);
    console.log('element is :', this_val);


    $.ajax({
        url : '/make_default_address',
        data : {
            'id': id
        },
        dataType : 'json',
        success : function(response){
            console.log('Address Made Default...');
            if (response.boolean == true){
                    
                $('.check').hide()
                $('.action_btn').show()

                $('.check'+id).show()
                $('.button'+id).hide()
            }
        }
    })

})


// $( function() {
//     $( "#product" ).autocomplete({
//         source: ['js', 'php', 'python']
//     });
// } );







