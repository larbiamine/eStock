
$(function () {
    console.log("Hello!");
    $(".js-create-order").click(function () {
      $.ajax({
        url: '/norderc/create/',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-order").modal("show");
        },
        success: function (data) {
          $("#modal-order .modal-content").html(data.html_form);
        }
      });
    });
  
  });
  $("#modal-order").on("submit", ".js-order-create-form", function () {
    var form = $(this);
    $.ajax({
      url: "form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          alert("order created!");  // <-- This is just a placeholder for now for testing
        }
        else {
          $("#modal-order .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });