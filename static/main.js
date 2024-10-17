
function saveTodo(todoId) {
    // Get the form corresponding to the todo item
    var form = document.getElementById('edit-todo-form-' + todoId);

    if (!form) {
        console.error('Form element not found');
        return;
    }

    // Create a FormData object from the form data
    var formData = new FormData(form);

    // Send an AJAX request to the server to save the todo item
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle the response from the server
            if (data.success) {
                // Display a success message or perform any other actions
                alert(data.message);
            } else {
                // Display an error message or perform any other error handling
                alert('An error occurred while updating the record.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Display an error message or perform any other error handling
            alert('An error occurred while updating the record.');
        });
}


function deleteTodo(todoId) {
    if (confirm("Are you sure you want to delete this todo?")) {
        fetch(`/delete_todo/${todoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ todo_id: todoId })
        })
            .then(response => {
                if (response.ok) {
                    // Reload the page or update the todo list after successful deletion
                    location.reload(); // For reloading the page
                    // You can also remove the deleted todo from the DOM without reloading the page
                    // For example, remove the todo item from the DOM using JavaScript
                    // document.getElementById(`todo-${todoId}`).remove();
                } else {
                    throw new Error('Failed to delete todo');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the todo.');
            });
    }
}


function markAsComplete(todoId) {
    if (confirm("Are you sure you want to mark this todo as complete?")) {
        fetch(`/toggle_complete/${todoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const todoItem = document.getElementById(`todo-${todoId}`);
                    const completeButton = todoItem.querySelector('.complete-button');
                    completeButton.textContent = '❌ Mark Incomplete';
                    completeButton.setAttribute('onclick', `markAsIncomplete(${todoId})`);
                    todoItem.classList.add('completed');

                    // Show save and delete buttons
                    const saveButton = todoItem.querySelector('.save-button');
                    const deleteButton = todoItem.querySelector('.delete-button');
                    saveButton.style.display = 'inline-block';
                    deleteButton.style.display = 'inline-block';
                } else {
                    alert('An error occurred while marking the todo as complete.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while marking the todo as complete.');
            });
    }
}

function markAsIncomplete(todoId) {
    if (confirm("Are you sure you want to mark this todo as incomplete?")) {
        fetch(`/toggle_complete/${todoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const todoItem = document.getElementById(`todo-${todoId}`);
                    const completeButton = todoItem.querySelector('.complete-button');
                    completeButton.textContent = '✓';
                    completeButton.setAttribute('onclick', `markAsComplete(${todoId})`);
                    todoItem.classList.remove('completed');

                    // Hide save and delete buttons
                    const saveButton = todoItem.querySelector('.save-button');
                    const deleteButton = todoItem.querySelector('.delete-button');
                    saveButton.style.display = 'none';
                    deleteButton.style.display = 'none';
                } else {
                    alert('An error occurred while marking the todo as incomplete.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while marking the todo as incomplete.');
            });
    }
}


function toggleComplete(todoId) {
    if (confirm("Are you sure you want to mark this todo as complete?")) {
        fetch(`/toggle_complete/${todoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token // Assuming you have a CSRF token available
            },
            body: JSON.stringify({ todo_id: todoId })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to mark todo item as complete');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Update UI to reflect completion status
                    const todoItem = document.getElementById(`todo-${todoId}`);
                    if (todoItem) {
                        todoItem.classList.toggle('completed');
                    }
                } else {
                    throw new Error(data.message);
                }
            })
            .catch(error => {
                alert(error.message);
            });
    }
}
