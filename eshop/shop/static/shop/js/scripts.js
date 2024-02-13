$(document).ready(function () {
  $(".navbar .dropdown").hover(
    function () {
      $(this)
        .find(".dropdown-menu")
        .first()
        .stop(true, true)
        .delay(250)
        .slideDown();
    },
    function () {
      $(this)
        .find(".dropdown-menu")
        .first()
        .stop(true, true)
        .delay(100)
        .slideUp();
    }
  );

  $(".navbar .dropdown > a").click(function (e) {
    location.href = this.href;
  });

  function updateCartCount() {
    $.ajax({
      url: "{% url 'cart_count' %}",
      dataType: "json",
      success: function (data) {
        $("#cart-badge").text(data.cart_count);
      },
    });
  }
  updateCartCount();

  function updateWishlistCount() {
    $.ajax({
      url: "#",
      dataType: "json",
      success: function (data) {
        $("#wishlist-badge").text(data.wishlist_count);
      },
    });
  }
  updateWishlistCount();
});

$(document).ready(function () {
  $("input[name='query']").on("input", function () {
    var query = $(this).val();
    if (query.length > 0) {
      $.getJSON(
        "{% url 'product-autocomplete' %}",
        { term: query },
        function (data) {
          if (data.length > 0) {
            var dropdownContent = "";
            $.each(data, function (index, product) {
              dropdownContent += '<div class="card">';
              dropdownContent +=
                '<img src="' +
                product.image_url +
                '" class="card-img-top" alt="' +
                product.name +
                '">';
              dropdownContent += '<div class="card-body">';
              dropdownContent +=
                '<h5 class="card-title">' + product.name + "</h5>";
              dropdownContent +=
                '<p class="card-text">' + product.price + "</p>";
              dropdownContent += "</div></div>";
            });
            $(".autocomplete-dropdown").html(dropdownContent);
            $(".autocomplete-dropdown").show();
          } else {
            $(".autocomplete-dropdown").hide();
          }
        }
      );
    } else {
      $(".autocomplete-dropdown").hide();
    }
  });

  $(document).on("click", function (event) {
    if (
      !$(event.target).closest(".autocomplete-dropdown").length &&
      !$(event.target).closest('input[name="query"]').length
    ) {
      $(".autocomplete-dropdown").hide();
    }
  });
});
