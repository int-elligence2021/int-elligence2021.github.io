var button_add = document.getElementById("enteringredients");
var input_add = document.getElementById("typeingredient");
var ul_add = document.querySelector("#add_ingredients_list");

button_add.addEventListener("click", function() {
  var li_add = document.createElement("li");
  li_add.className = 'list-group-item';
  li_add.textContent = input_add.value;
  ul_add.appendChild(li_add);
})


var button_rem = document.getElementById("remingredient");
var input_rem = document.getElementById("typerem");
var ul_rem = document.querySelector("#rem_ingredients_list");

button_rem.addEventListener("click", function() {
  var li_rem = document.createElement("li");
  li_rem.className = 'list-group-item';
  li_rem.textContent = input_rem.value;
  ul_rem.appendChild(li_rem);
})