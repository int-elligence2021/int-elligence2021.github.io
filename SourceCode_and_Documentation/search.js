/**
 * Adding search items to a list..
 * Source:
 * Adel Elkhodary at https://stackoverflow.com/questions/50308538/dynamically-add-a-bootstrap-4-list-item-on-button-click
*/


/* Add ingredients after typing them to the list" */
var button_add = document.getElementById("enteringredients");
var input_add = document.getElementById("typeingredient");
var ul_add = document.querySelector("#add_ingredients_list");

button_add.addEventListener("click", function() {
  var li_add = document.createElement("li");
  li_add.className = 'list-group-item';
  li_add.textContent = input_add.value;
  li_add.setAttribute('onclick','remove_list_item(this)');
  ul_add.appendChild(li_add);
})


/* Add ingredients to negative search list after typing them */
var button_rem = document.getElementById("remingredient");
var input_rem = document.getElementById("typerem");
var ul_rem = document.querySelector("#rem_ingredients_list");

button_rem.addEventListener("click", function() {
  var li_rem = document.createElement("li");
  li_rem.className = 'list-group-item';
  li_rem.textContent = input_rem.value;
  li_rem.setAttribute('onclick','remove_list_item(this)');
  ul_rem.appendChild(li_rem);
})


/* removes current item from the parent node */
function remove_list_item(item) {
  item.parentNode.removeChild(item)
}
