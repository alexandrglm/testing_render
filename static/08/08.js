document.addEventListener("DOMContentLoaded", function () {
    //////////////////////////////////////////////////////////
    //  Variables
    //////////////////
    const createButton = document.getElementById("createButton");
    const userPicker = document.getElementById("userPicker");
    const saveButton = document.getElementById("saveButton");
    const deleteButton = document.getElementById("deleteButton");
    const profileImage = document.getElementById("JS_IMG_PROFILE");
    const clientIdField = document.getElementById("editClientID");
    const firstNameField = document.getElementById("editFirstName");
    const lastNameField = document.getElementById("editLastName");
    const dobField = document.getElementById("editDOB");
    const idField = document.getElementById("editID");
    const viewer = document.getElementById("viewer");
    const editButton = document.createElement("button");
    editButton.textContent = "Edit Record";
    editButton.style.display = "none";
    viewer.appendChild(editButton);

    //////////////////////////////////////////////////////////
    //  Fetch Profiles
    //////////////////
    function fetchProfiles() {
        fetch("/08/profile")
            .then(response => response.json())
            .then(data => {
                userPicker.innerHTML = '<option value="">Choose a User</option>';
                data.forEach(user => {
                    let option = document.createElement("option");
                    option.value = user.client_id;
                    option.textContent = `#${user.client_id} - ${user.full_name}`;
                    userPicker.appendChild(option);
                });
            })
            .catch(error => console.error("Error loading profiles:", error));
    }

    //////////////////////////////////////////////////////////
    //  Reset Editor
    //////////////////
    function resetEditor() {
        clientIdField.value = "";
        firstNameField.value = "";
        lastNameField.value = "";
        dobField.value = "";
        idField.value = "";
        userPicker.value = "";
        profileImage.src = "/data/08/default.jpeg";
    }

    //////////////////////////////////////////////////////////
    //  Reset Viewer
    //////////////////
    function resetViewer() {
        document.getElementById("viewerClient").querySelector("span").textContent = "";
        document.getElementById("viewerFullName").querySelector("span").textContent = "";
        document.getElementById("viewerID").querySelector("span").textContent = "";
        document.getElementById("viewerDOB").querySelector("span").textContent = "";
        profileImage.src = "/data/08/default.jpeg";
        editButton.style.display = "none";
    }

    //////////////////////////////////////////////////////////
    //  Update Viewer
    //////////////////
    function updateViewer(user) {
        let nameParts = user.full_name.split(",").map(s => s.trim());

        document.getElementById("viewerClient").querySelector("span").textContent = user.client_id || "N/A";
        document.getElementById("viewerFullName").querySelector("span").textContent = user.full_name || "N/A";
        document.getElementById("viewerID").querySelector("span").textContent = user.ident_id || "N/A";
        document.getElementById("viewerDOB").querySelector("span").textContent = user.dob.replace("Born on ", "") || "N/A";

        profileImage.src = user.img_profile || "/data/08/default.jpeg";
        editButton.style.display = "block";

        editButton.onclick = function () {
            clientIdField.value = user.client_id || "";
            firstNameField.value = nameParts[1] || "";
            lastNameField.value = nameParts[0] || "";
            dobField.value = user.dob.replace("Born on ", "") || "";
            idField.value = user.ident_id || "";
        };
    }

    //////////////////////////////////////////////////////////
    //  User Picker Change
    //////////////////
    userPicker.addEventListener("change", function () {
        let clientId = userPicker.value;

        if (!clientId) {
            resetViewer();
            return;
        }

        fetch("/08/profile")
            .then(response => response.json())
            .then(data => {
                let user = data.find(user => user.client_id == clientId);
                if (user) {
                    updateViewer(user);
                }
            })
            .catch(error => console.error("Error fetching user details:", error));
    });

    //////////////////////////////////////////////////////////
    //  Create New Profile
    //////////////////
    createButton.addEventListener("click", function () {
        resetViewer();
        resetEditor();

        fetch("/08/profile")
            .then(response => response.json())
            .then(data => {
                let newId = data.length > 0 ? Math.max(...data.map(user => parseInt(user.client_id))) + 1 : 1;
                clientIdField.value = newId;
                fetch(`/08/profile/new/${newId}`)
                    .then(response => response.json())
                    .then(data => {
                        profileImage.src = data.img_profile || "";
                    })
                    .catch(error => console.error("Error generating new profile image:", error));
            })
            .catch(error => console.error("Error fetching profiles:", error));
    });

    //////////////////////////////////////////////////////////
    //  Save Profile
    //////////////////
    saveButton.addEventListener("click", function () {
        let clientId = clientIdField.value;
        let profileData = {
            client_id: clientId,
            JS_FIRSTNAME: firstNameField.value,
            JS_LASTNAME: lastNameField.value,
            JS_DOB: dobField.value,
            JS_ID: idField.value
        };
    
        let url = `/08/profile`;
        let method = "POST";
    
        if (clientId) {
            url = `/08/profile/${clientId}`;
            method = "PUT";
        }
    
        fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(profileData)
        })
        .then(response => response.json())
        .then(data => {
            alert(clientId ? "Profile successfully updated." : "Profile successfully created.");
            
            if (!clientId) {
                let newClientId = data.client_id;
                fetch(`/08/profile/rename_image/${newClientId}`, { method: "PUT" })
                    .catch(error => console.error("Error renaming image:", error));
            }
    
            fetchProfiles();
            resetEditor();
            resetViewer();
        })
        .catch(error => console.error("Error:", error));
    });

    //////////////////////////////////////////////////////////
    //  Delete Profile
    //////////////////
    deleteButton.addEventListener("click", function () {
        let clientId = clientIdField.value;

        fetch(`/08/profile/${clientId}`, { method: "DELETE" })
        .then(response => response.json())
        .then(data => {
            alert("Profile successfully deleted.");
            fetchProfiles();
            resetEditor();
            resetViewer();
        })
        .catch(error => console.error("Error:", error));
    });

    //////////////////////////////////////////////////////////
    //  Init
    //////////////////
    fetchProfiles();
});
