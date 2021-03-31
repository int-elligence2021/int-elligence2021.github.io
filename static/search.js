/* Adding search items to a list.. */

/* Add ingredients after typing them to the list" */
var button_add = document.getElementById("enteringredients");
var input_add = document.getElementById("typeingredient");
var ul_add = document.querySelector("#add_ingredients_list");

button_add.addEventListener("click", function() {
  var li_add = document.createElement("li");
  var input = document.createElement("input");

  li_add.className = 'list-group-item';
  li_add.textContent = input_add.value;
  li_add.setAttribute('onclick','remove_list_item(this)');
  li_add.setAttribute('data-toggle','tooltip');
  li_add.setAttribute('data-placement','top');
  li_add.title = 'Click to remove';

  input.type = 'hidden';
  input.name = 'addIngred';
  input.value = input_add.value;

  li_add.appendChild(input);

  ul_add.appendChild(li_add);
})


/* Add ingredients to negative search list after typing them */
var button_rem = document.getElementById("remingredient");
var input_rem = document.getElementById("typerem");
var ul_rem = document.querySelector("#rem_ingredients_list");

button_rem.addEventListener("click", function() {
  var li_rem = document.createElement("li");
  var input = document.createElement("input");

  li_rem.className = 'list-group-item';
  li_rem.textContent = input_rem.value;
  li_rem.setAttribute('onclick','remove_list_item(this)');
  li_rem.setAttribute('data-toggle','tooltip');
  li_rem.setAttribute('data-placement','top');
  li_rem.title = 'Click to remove';
  
  input.type = 'hidden';
  input.name = 'negSearch';
  input.value = input_rem.value;

  li_rem.appendChild(input);

  ul_rem.appendChild(li_rem);
})


/* removes current item from the parent node */
function remove_list_item(item) {
  item.parentNode.removeChild(item)
}
