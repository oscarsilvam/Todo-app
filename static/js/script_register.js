const emptyField = "Veuillez remplir ce champ avant de soummetre le formulaire";

function resetMsgError() {
    document.querySelectorAll(".error").forEach(err => err.textContent = "");
}

function valFirstName() {
    const firstName = document.getElementById("first_name").value.trim();

    //Input first name empty
    if (!firstName) {
        document.getElementById("err_first_name").textContent = emptyField;
        return false;
    }

    if (firstName.length > 30) {
        document.getElementById("err_first_name").textContent = "Votre prénom ne "
            + "doit pas dépasser de 30 caractères";
        return false;
    }
    return true;
}

function valLastName() {
    const lastName = document.getElementById("last_name").value.trim();

    if (!lastName) {
        document.getElementById("err_last_name").textContent = emptyField;
        return false;
    }
    //Last name to long
    if (lastName.length > 30) {
        document.getElementById("err_last_name").textContent = "Votre nom famille "
            + "ne doit pas dépasser de 30 caractères"
        return false;
    }
    return true;
}

function valEmail() {
    const email = document.getElementById("email").value.trim();

    if (!email) {
        document.getElementById("err_email").textContent = emptyField;
        return false;
    }
    //Model
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    //email test
    if (!regexEmail.test(email)) {
        document.getElementById("err_email").textContent = "Courriel non valide! "
            + "Ex : info@gmail.com";
        return false;
    }
    return true;
}

function valUsername() {
    const username = document.getElementById("username").value.trim();

    if (!username) {
        document.getElementById("err_username").textContent = emptyField;
        return false;
    }

    if (username.length > 30) {
        document.getElementById("err_username").textContent = "Votre nom utilisateur"
            + "ne doit pas dépasser de 30 caractères";
        return false
    }
    return true;
}

function valPassword() {
    const password = document.getElementById("password").value;

    if (!password) {
        document.getElementById("err_password").textContent = emptyField;
        return false;
    }

    if (password.length < 8 || password.length > 30) {
        document.getElementById("err_password").textContent = "Votre mot de passe"
        + " doit contenir entre 9 et 30 caractères";
        return false;
    }
    return true;
}

document.getElementById("formulaire_register").addEventListener("submit", function (event) {

    resetMsgError();
    //Call to all of functions
    const firstNameCheck = valFirstName();
    const lastNameCheck = valLastName();
    const emailCheck = valEmail();
    const usernameCheck = valUsername();
    const passwordCheck = valPassword();

    if (!firstNameCheck || !lastNameCheck || !emailCheck || !usernameCheck
        || !passwordCheck) {
            event.preventDefault();
        }
})
