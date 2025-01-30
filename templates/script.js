// The story array contains 10 parts
const story = [
    "Part 1: On a rainy evening, Alex finds an old letter from a childhood friend. It brings back bittersweet memories.",
    "Part 2: The letter contains an invitation to meet at their favorite childhood spot after a decade of silence.",
    "Part 3: Alex is hesitant but decides to visit, remembering the bond they once shared.",
    "Part 4: At the spot, Alex finds a small, weathered box left behind with a familiar locket inside.",
    "Part 5: Memories of laughter and tears flood back as Alex clutches the locket tightly.",
    "Part 6: Alex wonders why the friend left the box there and what it could mean.",
    "Part 7: Later that night, Alex receives an unexpected phone call with no voice on the other end.",
    "Part 8: Haunted by the silence, Alex starts recalling moments when they parted ways abruptly.",
    "Part 9: Determined to find answers, Alex decides to follow the clues from the letter.",
    "Part 10: Alex reaches a final revelation, learning about the sacrifices their friend made to protect them."
];

let currentPart = 0;

// Function to display the next part of the story
function displayStoryPart() {
    const storyPartElement = document.getElementById("story-part");

    if (currentPart < story.length) {
        storyPartElement.textContent = story[currentPart];
    } else {
        alert("The story has ended.");
    }
}

// Function to send event and thoughts to the server
async function submitThoughts() {
    const event = story[currentPart];
    const thoughts = document.getElementById("thoughts").value;

    if (!thoughts.trim()) {
        alert("Please enter your thoughts.");
        return;
    }

    try {


        // First, analyze the emotional content of the thoughts
        const emotionalResponse = await fetch('/detect_emotions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: thoughts }),
        });

        if (!emotionalResponse.ok) {
            throw new Error(`Emotional analysis failed: ${emotionalResponse.status}`);
        }

        const emotionalData = await emotionalResponse.json();

        // Store emotional analysis for later use
        const emotionalContext = {
            emotions: emotionalData.emotions,
            dominantEmotion: emotionalData.emotions[0]?.emotion,
            emotionalIntensity: emotionalData.emotions[0]?.score
        };



        const response = await fetch('/generate_questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ event, thoughts }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.questions && data.questions.length > 0) {
                currentPart++; // Move to the next part of the story
                displayQuestions(data.questions);
                displayStoryPart();
            } else {
                alert("No questions generated. Please try again later.");
            }
        } else {
            console.error("Response Error:", response.status, await response.text());
            alert("Error generating questions. Please try again.");
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Server error. Please try again later.");
    }
}

// Function to display questions with options as buttons
function displayQuestions(questions) {
    const questionsSection = document.getElementById('questions-section');
    const questionsContainer = document.getElementById('questions-container');

    questionsContainer.innerHTML = ''; // Clear previous questions

    questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.innerHTML = `
        <p>${q.question}</p>
        <button onclick="selectAnswer(${index}, 'A')">A) ${q.options.A}</button>
        <button onclick="selectAnswer(${index}, 'B')">B) ${q.options.B}</button>
        <button onclick="selectAnswer(${index}, 'C')">C) ${q.options.C}</button>
    `;
        questionsContainer.appendChild(questionDiv);
    });



    questionsSection.style.display = 'block';
}

// Function to handle answer selection
function selectAnswer(questionIndex, answer) {
    console.log(`Question ${questionIndex + 1}: Selected ${answer}`);
}

// Initialize the first part of the story
displayStoryPart();
document.addEventListener("DOMContentLoaded", displayStoryPart);
