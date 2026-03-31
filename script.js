const words = {
    easy: [
        'casa', 'perro', 'gato', 'sol', 'luna', 'mar', 'rio', 'pan', 'luz', 'paz',
        'amor', 'vida', 'mesa', 'silla', 'libro', 'agua', 'fuego', 'aire', 'tierra', 'cielo',
        'flor', 'arbol', 'nube', 'viento', 'lluvia', 'nieve', 'calor', 'frio', 'dia', 'noche'
    ],
    medium: [
        'ordenador', 'teclado', 'pantalla', 'ventana', 'puerta', 'jardin', 'escuela', 'profesor',
        'estudiante', 'biblioteca', 'hospital', 'medicina', 'telefono', 'mensaje', 'correo',
        'internet', 'musica', 'pelicula', 'television', 'radio', 'periodico', 'revista',
        'fotografia', 'pintura', 'escultura', 'arquitectura', 'ingenieria', 'matematicas'
    ],
    hard: [
        'extraordinario', 'magnifico', 'espectacular', 'impresionante', 'maravilloso',
        'tecnologia', 'programacion', 'desarrollo', 'aplicacion', 'configuracion',
        'comunicacion', 'informacion', 'organizacion', 'administracion', 'investigacion',
        'experimentacion', 'transformacion', 'implementacion', 'optimizacion', 'automatizacion',
        'caracteristica', 'funcionalidad', 'compatibilidad', 'responsabilidad', 'sostenibilidad'
    ]
};

const letters = {
    easy: ['a', 's', 'd', 'f', 'j', 'k', 'l'],
    medium: ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    hard: ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
};

let currentWord = '';
let currentLetter = '';
let score = 0;
let timeLeft = 60;
let gameActive = false;
let timerInterval = null;
let difficulty = 'easy';
let gameMode = 'words';
let wordsTyped = 0;
let startTime = null;

const targetWordEl = document.getElementById('target-word');
const userInputEl = document.getElementById('user-input');
const scoreEl = document.getElementById('score');
const timerEl = document.getElementById('timer');
const wpmEl = document.getElementById('wpm');
const levelEl = document.getElementById('level');
const feedbackEl = document.getElementById('feedback');
const startBtn = document.getElementById('start-btn');
const resetBtn = document.getElementById('reset-btn');
const difficultySelect = document.getElementById('difficulty');
const modeSelect = document.getElementById('mode');

function getRandomWord() {
    const wordList = words[difficulty];
    return wordList[Math.floor(Math.random() * wordList.length)];
}

function getRandomLetter() {
    const letterList = letters[difficulty];
    return letterList[Math.floor(Math.random() * letterList.length)];
}

function displayNewWord() {
    if (gameMode === 'words') {
        currentWord = getRandomWord();
        targetWordEl.textContent = currentWord;
        targetWordEl.className = '';
        userInputEl.value = '';
    } else {
        currentLetter = getRandomLetter();
        targetWordEl.textContent = currentLetter.toUpperCase();
        targetWordEl.className = 'letter-mode';
    }
    feedbackEl.textContent = '';
    feedbackEl.className = 'feedback';
}

function calculateWPM() {
    if (!startTime) return 0;
    const timeElapsed = (Date.now() - startTime) / 1000 / 60;
    return Math.round(wordsTyped / timeElapsed) || 0;
}

function updateWPM() {
    wpmEl.textContent = calculateWPM();
}

function showFeedback(isCorrect) {
    feedbackEl.textContent = isCorrect ? '¡Correcto! ✓' : '¡Incorrecto! ✗';
    feedbackEl.className = isCorrect ? 'feedback correct' : 'feedback incorrect';
    setTimeout(() => {
        feedbackEl.textContent = '';
        feedbackEl.className = 'feedback';
    }, 500);
}

function checkWord() {
    const userWord = userInputEl.value.trim().toLowerCase();
    
    if (userWord === currentWord.toLowerCase()) {
        score += difficulty === 'easy' ? 1 : difficulty === 'medium' ? 2 : 3;
        wordsTyped++;
        scoreEl.textContent = score;
        updateWPM();
        showFeedback(true);
        displayNewWord();
    }
}

function checkLetter(key) {
    if (key.toLowerCase() === currentLetter.toLowerCase()) {
        score += 1;
        wordsTyped++;
        scoreEl.textContent = score;
        updateWPM();
        showFeedback(true);
        displayNewWord();
    } else {
        showFeedback(false);
    }
}

function startTimer() {
    timerInterval = setInterval(() => {
        timeLeft--;
        timerEl.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function startGame() {
    gameActive = true;
    score = 0;
    timeLeft = 60;
    wordsTyped = 0;
    startTime = Date.now();
    
    scoreEl.textContent = score;
    timerEl.textContent = timeLeft;
    wpmEl.textContent = 0;
    
    if (gameMode === 'words') {
        userInputEl.disabled = false;
        userInputEl.focus();
    } else {
        userInputEl.disabled = true;
        document.body.focus();
    }
    
    startBtn.disabled = true;
    difficultySelect.disabled = true;
    modeSelect.disabled = true;
    
    displayNewWord();
    startTimer();
}

function endGame() {
    gameActive = false;
    clearInterval(timerInterval);
    
    userInputEl.disabled = true;
    startBtn.disabled = false;
    difficultySelect.disabled = false;
    modeSelect.disabled = false;
    
    const finalWPM = calculateWPM();
    targetWordEl.textContent = `¡Juego terminado! Puntuación: ${score} | PPM: ${finalWPM}`;
    targetWordEl.className = '';
    feedbackEl.textContent = '¡Buen trabajo!';
    feedbackEl.className = 'feedback correct';
}

function resetGame() {
    gameActive = false;
    clearInterval(timerInterval);
    
    score = 0;
    timeLeft = 60;
    wordsTyped = 0;
    startTime = null;
    
    scoreEl.textContent = score;
    timerEl.textContent = timeLeft;
    wpmEl.textContent = 0;
    
    userInputEl.value = '';
    userInputEl.disabled = true;
    startBtn.disabled = false;
    difficultySelect.disabled = false;
    modeSelect.disabled = false;
    
    targetWordEl.textContent = 'Pulsa INICIAR para empezar';
    targetWordEl.className = '';
    feedbackEl.textContent = '';
    feedbackEl.className = 'feedback';
}

userInputEl.addEventListener('input', () => {
    if (gameActive && gameMode === 'words') {
        checkWord();
    }
});

document.addEventListener('keydown', (e) => {
    if (gameActive && gameMode === 'letters') {
        if (e.key.length === 1 && e.key.match(/[a-z]/i)) {
            checkLetter(e.key);
        }
    }
});

startBtn.addEventListener('click', startGame);
resetBtn.addEventListener('click', resetGame);

modeSelect.addEventListener('change', (e) => {
    gameMode = e.target.value;
});

difficultySelect.addEventListener('change', (e) => {
    difficulty = e.target.value;
    const difficultyNames = {
        easy: 'Fácil',
        medium: 'Medio',
        hard: 'Difícil'
    };
    levelEl.textContent = difficultyNames[difficulty];
});
