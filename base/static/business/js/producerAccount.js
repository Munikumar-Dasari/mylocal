const deletePencilIconEl = document.getElementById("deletePencilIcon");
const deleteDescriptionEl = document.getElementById("deleteDescription");
const deleteTextEl = document.getElementById("deleteText")



let updateText;
function functionDeleteText(event){
     updateText = event.target.value;
}


function functionDeleteIcon(){
     deleteDescriptionEl.style.display = "none";
     deletePencilIconEl.style.display = "none";
     deleteTextEl.style.display = "block";
     deleteTextEl.textContent = deleteDescriptionEl.textContent;
}


function functionDeleteTextBlur(){
     deleteDescriptionEl.style.display = "block";
     deletePencilIconEl.style.display = "block";
     deleteTextEl.style.display = "none";
     deleteDescriptionEl.textContent = updateText;
}


deletePencilIconEl.addEventListener("click", functionDeleteIcon);

deleteTextEl.addEventListener("keydown", functionDeleteText);
deleteTextEl.addEventListener("blur", functionDeleteTextBlur);