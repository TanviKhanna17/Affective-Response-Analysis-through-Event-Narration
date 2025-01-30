let changeCounters = {}; // To store change counters for each question
let totalTimeSpent = 0; // To track total time spent
let startTime; // To track when the questions are generated

function generateQuestions() {
    const event = document.getElementById('event').value;
    const thoughts = document.getElementById('thoughts').value;
    
    fetch('/generate_questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ event, thoughts })
    })
    .then(response => response.json())
    .then(data => {
        const questionsContainer = document.getElementById('questions-container');
        questionsContainer.innerHTML = '';
        
        data.questions.forEach((question, index) => {
            // Initialize the change counter for each question
            changeCounters[index] = 0;

            const questionDiv = document.createElement('div');
            questionDiv.innerHTML = `<p>${question}</p>`;
            
            const options = ['A', 'B', 'C'];
            options.forEach(option => {
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = `question${index}`;
                radio.value = option;
                
                // Track changes for this specific question
                radio.addEventListener('change', () => trackChanges(index, option));

                const label = document.createElement('label');
                label.appendChild(radio);
                label.appendChild(document.createTextNode(` Option ${option}`));
                
                questionDiv.appendChild(label);
                questionDiv.appendChild(document.createElement('br'));
            });
            
            questionsContainer.appendChild(questionDiv);
        });
        
        document.getElementById('questions-section').style.display = 'block';

        // Start the timer when questions are generated
        startTime = new Date();
    });
}

function trackChanges(questionIndex, selectedOption) {
    // Check if the selected option has changed
    changeCounters[questionIndex] += 1; // Increment the change counter for this question

    if (changeCounters[questionIndex] > 3) {
        console.log(`Question ${questionIndex + 1} is indecisive due to too many changes.`);
    }
}

function submitDecision() {
    // Calculate total time spent in seconds
    totalTimeSpent = Math.floor((new Date() - startTime) / 1000);

    const indecisiveDueToTime = totalTimeSpent > 240; // 240 seconds = 4 minutes
    let indecisive = false;

    // Check if any question is indecisive
    for (let index in changeCounters) {
        if (changeCounters[index] > 3) {
            indecisive = true;
            break; // Exit the loop if any question is indecisive
        }
    }

    // Combine indecisiveness due to changes and time spent
    indecisive = indecisive || indecisiveDueToTime;

    fetch('/submit_decision', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ changes: changeCounters, indecisive: indecisive })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.indecisive) {
            console.log("User was indecisive");
        }
    });
}
