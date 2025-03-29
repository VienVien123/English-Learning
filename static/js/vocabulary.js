import { getAuthHeaders } from './auth.js';

// API endpoints
const API_URL = '/api';

// Get all topics
async function getTopics() {
    try {
        const response = await fetch(`${API_URL}/topics/`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching topics:', error);
        throw error;
    }
}

// Get all words
async function getWords() {
    try {
        const response = await fetch(`${API_URL}/words/`, {
            headers: getAuthHeaders()
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching words:', error);
        throw error;
    }
}

// Add new word
async function addWord(wordData) {
    try {
        const response = await fetch(`${API_URL}/words/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(wordData)
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error adding word:', error);
        throw error;
    }
}

// Update word
async function updateWord(wordId, wordData) {
    try {
        const response = await fetch(`${API_URL}/words/${wordId}/`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(wordData)
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating word:', error);
        throw error;
    }
}

// Delete word
async function deleteWord(wordId) {
    try {
        const response = await fetch(`${API_URL}/words/${wordId}/`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        return response.ok;
    } catch (error) {
        console.error('Error deleting word:', error);
        throw error;
    }
}

// Mark word as learned
async function markWordLearned(wordId) {
    try {
        const response = await fetch(`${API_URL}/words/${wordId}/`, {
            method: 'PATCH',
            headers: getAuthHeaders(),
            body: JSON.stringify({ is_learned: true })
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error marking word as learned:', error);
        throw error;
    }
}

// Create word card HTML
function createWordCard(word) {
    return `
        <div class="col-md-4 mb-4">
            <div class="card h-100 ${word.is_learned ? 'bg-light' : ''}">
                <div class="card-body">
                    <h5 class="card-title">${word.word}</h5>
                    <p class="card-text">${word.definition}</p>
                    <p class="card-text"><small class="text-muted">Example: ${word.example}</small></p>
                    <p class="card-text"><small class="text-muted">Topic: ${word.topic}</small></p>
                    <div class="btn-group">
                        <button type="button" class="btn btn-sm btn-outline-primary edit-word" data-word-id="${word.id}">
                            Edit
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger delete-word" data-word-id="${word.id}">
                            Delete
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-success mark-learned ${word.is_learned ? 'active' : ''}" data-word-id="${word.id}">
                            ${word.is_learned ? 'Learned' : 'Mark as Learned'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Initialize the vocabulary page
export async function initVocabularyPage() {
    try {
        // Load topics
        const topics = await getTopics();
        const topicsList = document.getElementById('topicsList');
        const topicSelect = document.getElementById('topic');
        const editTopicSelect = document.getElementById('editTopic');
        
        // Populate topics list
        topics.forEach(topic => {
            // Add to sidebar
            const li = document.createElement('li');
            li.className = 'nav-item';
            li.innerHTML = `
                <a class="nav-link" href="#" data-topic-id="${topic.id}">
                    ${topic.name}
                </a>
            `;
            topicsList.appendChild(li);
            
            // Add to select options
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = topic.name;
            topicSelect.appendChild(option);
            editTopicSelect.appendChild(option.cloneNode(true));
        });
        
        // Load words
        const words = await getWords();
        const wordGrid = document.getElementById('wordGrid');
        wordGrid.innerHTML = '';
        words.forEach(word => {
            wordGrid.appendChild(createWordCard(word));
        });
        
        // Add event listeners
        addEventListeners();
    } catch (error) {
        console.error('Error initializing vocabulary page:', error);
        alert('Error loading vocabulary data');
    }
}

// Add event listeners
function addEventListeners() {
    // Add word form
    const addWordForm = document.getElementById('addWordForm');
    if (addWordForm) {
        addWordForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(addWordForm);
            const wordData = {
                word: formData.get('word'),
                definition: formData.get('definition'),
                example: formData.get('example'),
                topic: formData.get('topic')
            };

            try {
                const newWord = await addWord(wordData);
                const wordGrid = document.getElementById('wordGrid');
                wordGrid.insertAdjacentHTML('afterbegin', createWordCard(newWord));
                bootstrap.Modal.getInstance(document.getElementById('addWordModal')).hide();
                addWordForm.reset();
            } catch (error) {
                alert('Error adding word');
            }
        });
    }

    // Edit word form
    const editWordForm = document.getElementById('editWordForm');
    if (editWordForm) {
        editWordForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(editWordForm);
            const wordId = formData.get('word_id');
            const wordData = {
                word: formData.get('word'),
                definition: formData.get('definition'),
                example: formData.get('example'),
                topic: formData.get('topic')
            };

            try {
                const updatedWord = await updateWord(wordId, wordData);
                const wordCard = document.querySelector(`[data-word-id="${wordId}"]`).closest('.col-md-4');
                wordCard.outerHTML = createWordCard(updatedWord);
                bootstrap.Modal.getInstance(document.getElementById('editWordModal')).hide();
            } catch (error) {
                alert('Error updating word');
            }
        });
    }

    // Delete word buttons
    document.querySelectorAll('.delete-word').forEach(button => {
        button.addEventListener('click', async () => {
            if (confirm('Are you sure you want to delete this word?')) {
                const wordId = button.dataset.wordId;
                try {
                    const success = await deleteWord(wordId);
                    if (success) {
                        button.closest('.col-md-4').remove();
                    }
                } catch (error) {
                    alert('Error deleting word');
                }
            }
        });
    });

    // Mark word as learned buttons
    document.querySelectorAll('.mark-learned').forEach(button => {
        button.addEventListener('click', async () => {
            const wordId = button.dataset.wordId;
            try {
                const updatedWord = await markWordLearned(wordId);
                const wordCard = button.closest('.col-md-4');
                wordCard.outerHTML = createWordCard(updatedWord);
            } catch (error) {
                alert('Error marking word as learned');
            }
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initVocabularyPage); 