// we first get all of our buttons
// we will create a loop now

var updateBtns = document.getElementsByClassName("update-cart");
//loop through all of our buttons
for (i = 0; i < updateBtns.length; i++) {
  //add an event listener, on click we will set a function
  //the function will activate each time we click
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product; //this is how we can query those custom attributes
    var action = this.dataset.action;
    
    //console them out to see if we have the correct id and action
    console.log("productId:", productId, "Action:", action);
    //check to see user
    console.log("USER:", user);

    if (user == "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log("Not logged in..");

  // cart = {
  //   1: { quantity: 4 },
  //   4: { quantity: 1 },
  //   6: { quantity: 2 },
  // };

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }
  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[product]["quantity"] <= 0) {
      console.log("Remove Item");
      delete cart[productId];
    }
  }
  console.log("Cart:", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain='path=/";
  location.reload();
}

function updateUserOrder(productId, action) {
  console.log("User is authenticated, sending data...");
  // send the data to our url of update_item
  var url = "/update_item/";
  // to send our post data we will use fetch
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    // body is the data we send to the backend
    // we need to send this data as a string so we will use JSON.stringify
    body: JSON.stringify({ productId: productId, action: action }),
  })
    // once we send data we also want to return a promise
    // we first need to turn this data inso a json data so we will say response
    // and we're going to say return response.json
    .then((response) => {
      return response.json();
    })
    // console the data out -> console.log('data:',data)
    .then((data) => {
      // make sure our page reloads to see the new data
      location.reload();
    });
}
