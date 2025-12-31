$(document).ready(function () {
  // Add to Selection
  $(".add-to-selection").on("click", function () {
    let button = $(this); //<button class="btn  add-to-selection" data-index="{{r.id}}">📋 Select</button> from room_type_detail.html
    let id = button.attr("data-index");

    // Get room and booking details from hidden inputs
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
        button.html("Selected");
        $(".room-count").text(response.total_selected_items);
      },
    });
  });
});

//Deleting the selected rooms from the cart
$(document).on("click", ".remove-room", function () {
  // In here the remove-room class is taken from the frontend part of rooms_selected.html section.

  let id = $(this).attr("data-item");
  let button = $(this);

  $.ajax({
    url: "/booking/remove_selection/",
    data: {
      id: id,
    },
    dataType: "json",
    beforeSend: function () {
      button.text("...");
    },
    success: function (res) {
      $(".room-count").text(res.total_selected_item);
      $(".selection-list").html(res.data); // In here the selection-list is from the rooms_selected.html (top div) class name
    },
  });
});

$(document).ready(function () {
  // Add to Selection
  $(".add-to-resturant-selection").on("click", function () {
    let button = $(this);
    let id = button.attr("data-index");

    let hotel_id = $("#hotel_id").val();
    let restaurant_id = $(`.restaurant_id_${id}`).val();
    let table_number = $(`.table_number_${id}`).val(); // ✅ Get table number
    let hotel_name = $("#hotel_name").val();
    let checkin = $("#checkin").val();
    let checkin_time = $("#checkin_time").val();
    let checkout_time = $("#checkout_time").val();

    // ✅ Debug output
    console.log("Hotel ID:", hotel_id);
    console.log("Restaurant ID:", restaurant_id);
    console.log("Hotel Name:", hotel_name);
    console.log("Table Number:", table_number); // ✅ Log table number
    console.log("Check-in:", checkin);
    console.log("Check-in Time:", checkin_time);
    console.log("Check-out Time:", checkout_time);

    $.ajax({
      url: "/booking/add_to_resturant_selection/",
      data: {
        hotel_id: hotel_id,
        restaurant_id: restaurant_id,
        table_number: table_number, // ✅ Optional: Send to backend if needed
        hotel_name: hotel_name,
        checkin: checkin,
        checkintime: checkin_time,
        checkouttime: checkout_time,
        number_of_seats: $("#number_of_seats").val(),
        table_capacity: $("#table_capacity").val(),
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Sending restaurant selection data to server...");
      },
      success: function (response) {
        console.log(response);
        button.html("Booked");
        $(".resturant-count").text(response.total_selected_items);
      },
      error: function (xhr, status, error) {
        console.error("Error selecting restaurant:", error);
      },
    });
  });
});
