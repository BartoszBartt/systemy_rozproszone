document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("send-button").addEventListener("click", sendMessage);
    document.getElementById("user-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Load chat history when the page is loaded
    loadChatHistory();
});

function loadChatHistory() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/chat_history", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var history = JSON.parse(xhr.responseText);
            displayChatHistory(history);
        }
    };
    xhr.send();
}

function displayChatHistory(history) {
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = ""; // Clear previous messages

    history.forEach(function(message) {
        var messageElement = document.createElement("p");
        messageElement.textContent = message.sender + ": " + message.text;
        chatBox.appendChild(messageElement);
    });

    // Scroll to the bottom after displaying chat history
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    sendMessageToChat(userInput);
}

function sendMessageToChat(message) {
    if (message.trim() === "") {
        return; // Prevent sending empty messages
    }

    var chatBox = document.getElementById("chat-box");
    var messageElement = document.createElement("p");
    messageElement.textContent = "You: " + message;
    chatBox.appendChild(messageElement);
    document.getElementById("user-input").value = "";

    // Send the message to the server using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_message", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var botMessageElement = document.createElement("p");
            botMessageElement.textContent = "Bot: " + response.message;
            chatBox.appendChild(botMessageElement);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }
    };
    xhr.send("message=" + message);
}
