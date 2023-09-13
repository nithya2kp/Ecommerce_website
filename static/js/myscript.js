

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity;
            var amountElement = document.getElementById("amount");
            amountElement.innerText = "Rs." + data.amount.toFixed(1);

            var totalAmountElement = document.getElementById("totalamount");
            totalAmountElement.innerHTML = "<strong>Rs." + data.totalamount.toFixed(1) + "</strong>";
        }
    })
})
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.innerText = data.quantity;
            var amountElement = document.getElementById("amount");
            amountElement.innerText = "Rs." + data.amount.toFixed(1);

            var totalAmountElement = document.getElementById("totalamount");
            totalAmountElement.innerHTML = "<strong>Rs." + data.totalamount.toFixed(1) + "</strong>";

            if (data.quantity === 0) {
                // If quantity becomes 0, remove the item from the cart
                $(eml).closest('.row').remove();
            }
        }
    });
});

$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            var amountElement = document.getElementById("amount");
            amountElement.innerText = "Rs." + data.amount.toFixed(1);

            var totalAmountElement = document.getElementById("totalamount");
            totalAmountElement.innerHTML = "<strong>Rs." + data.totalamount.toFixed(1) + "</strong>";
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})