const titleInput = document.getElementById("title-input");
const descInput = document.getElementById("desc-input");
const addButton = document.getElementById("add-btn");
const list = document.getElementById("todo-list");
const template = document.getElementById("todo-template");

function createTodo(title, description) {
  const fragment = template.content.cloneNode(true);
  const item = fragment.querySelector(".todo-item");
  const titleEl = fragment.querySelector(".title");
  const descEl = fragment.querySelector(".desc");
  const checkbox = fragment.querySelector("input[type=checkbox]");
  const deleteBtn = fragment.querySelector(".delete");

  titleEl.textContent = title;
  descEl.textContent = description || "";
  descEl.style.display = description ? "block" : "none";

  checkbox.addEventListener("change", () => {
    item.classList.toggle("completed", checkbox.checked);
  });

  deleteBtn.addEventListener("click", () => {
    item.remove();
  });

  return fragment;
}

function handleAdd() {
  const title = titleInput.value.trim();
  const description = descInput.value.trim();
  if (!title) {
    titleInput.focus();
    return;
  }

  list.appendChild(createTodo(title, description));
  titleInput.value = "";
  descInput.value = "";
  titleInput.focus();
}

addButton.addEventListener("click", handleAdd);

titleInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    handleAdd();
  }
});

// Demo items to match the reference image.
list.appendChild(createTodo("todo 1", ""));
list.appendChild(createTodo("todo 2", ""));
