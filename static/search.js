/* Adding search items to a list.. */

///////////////////////////////////////////////////////////////////////////
/* ADD INGREDIENTS */

/* Add ingredients when enter key pressed inside input field */
$("#typeingredient").keyup(function(event) {
  if (event.keyCode === 13) {
    $("#enteringredients").click();
  }
});

/* Add ingredients after typing them to the list */
$("#enteringredients").click(function() {
  var input_add = document.getElementById("typeingredient");
  var ul_add = document.querySelector("#add_ingredients_list");

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

  input_add.value = ''; // Removes search term from input field
  li_add.appendChild(input);
  ul_add.appendChild(li_add);
});


////////////////////////////////////////////////////////////////////////////
/* NEGATIVE SEARCH */


/* Add ingredients to negative search when enter key pressed inside input field */
$("#typerem").keyup(function(event) {
  if (event.keyCode === 13) {
    $("#remingredient").click();
  }
});

/* Add ingredients to negative search list after typing them */
$("#remingredient").click(function() {
  var input_rem = document.getElementById("typerem");
  var ul_rem = document.querySelector("#rem_ingredients_list");

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

  input_rem.value = '';
  li_rem.appendChild(input);
  ul_rem.appendChild(li_rem);
});


/* removes current item from the parent node */
function remove_list_item(item) {
  item.parentNode.removeChild(item)
}

/* Clear List button in add ingredients */
clearIngred.onclick = () => {
  const ingList = document.getElementById('add_ingredients_list');
  ingList.innerHTML = '';
}
