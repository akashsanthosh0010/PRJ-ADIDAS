$(".add-to-cart-btn").on('click',function(){
    let this_val = $(this)
    let index = this_val.attr('data-index')

    let quantity = $('.product-quantity-' + index ).val()
    let product_title = $('.product-title-' + index).val()
    let product_id = $('.product-id-' + index).val()
    let product_price = $('.current-product-price-' + index).text()
    let product_pid = $('.product-pid-' + index).val()
    let product_image = $('.product-image-' + index).val()


    
    




    console.log('Quantity:', quantity)
    console.log('Title:', product_title)
    console.log('Product id:', product_id)
    console.log('Product pid:', product_pid)
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



$(".update-product").on('click', function(){
    
    let product_id = $(this).attr('data-product')
    let this_val = $(this)
    let product_quantity = $('.product-qty-' + product_id).val()


    console.log('product id:', product_id)
    console.log('product qty:', product_quantity)


    $.ajax({
        url: '/update-cart',
        data : {
                'id': product_id, 
                'qty': product_quantity,
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
    
    







