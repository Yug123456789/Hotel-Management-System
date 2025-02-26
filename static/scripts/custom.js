$(document).ready(function () {
  // Add to Selection
  $(".add-to-selection").on("click", function () {
    let button = $(this); //<button class="btn  add-to-selection" data-index="{{r.id}}">📋 Select</button>
    let id = button.attr("data-index");

    let hotel_id = $("#id").val();
    let room_id = $(`.room_id_${id}`).val();
    let room_number = $(`.room_number_${id}`).val();
    let hotel_name = $("#hotel_name").val();
    let room_name = $("#room_name").val();
    let room_price = $("#room_price").val();
    let number_of_beds = $("#number_of_beds").val();
    let room_type = $("#room_type").val();
    let checkin = $("#checkin").val();
    let checkout = $("#checkout").val();

    console.log(hotel_id);
    console.log(room_id);
    console.log(room_number);
    console.log(room_name);
    console.log(hotel_name);
    console.log(room_price);
    console.log(number_of_beds);
    console.log(room_type);
    console.log(checkin);
    console.log(checkout);

    $.ajax({
      url: "/booking/add_to_selection/",
      data: {
        id: id,
        hotel_id: hotel_id,
        room_id: room_id,
        room_number: room_number,
        room_name: room_name,
        hotel_name: hotel_name,
        room_price: room_price,
        number_of_beds: number_of_beds,
        room_type: room_type,
        checkin: checkin,
        checkout: checkout,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Sending the data to server..");
      },
      success: function (response) {
        console.log(response);
      },
    });
  });
});

//Deleting the selected rooms from the cart
$(document).on("click", ".remove-room, .remove-room i", function () { // In here the remove-room class is taken from the frontend part of rooms_selected.html section.
  console.log("Deleted");
});
