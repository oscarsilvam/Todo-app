const emptyField = "Veuillez remplir ce champ avant de sauvegarder votre tâche";

function resetMsgError() {
    document.querySelectorAll(".error").forEach(err => err.textContent = "");
}

function valTodo() {
    const todo = document.getElementById("title").value.trim();

    if (!todo) {
        document.getElementById("err_title").textContent = emptyField;
        return false;
    }
    if (todo.length > 50) {
        document.getElementById("err_title").textContent = 
        "Le titre de votre tâche ne dois pas dépasser de 50 caractères";
        return false;
    }
    return true;
}

document.getElementById("form_todo").addEventListener("submit", function (event) {

    resetMsgError();
    const todoCheck = valTodo();

    if (!todoCheck) {
        event.preventDefault();
    } else {
        document.getElementById("add_todo").textContent = 
        "La tâche a été ajoutée";
    }
})
