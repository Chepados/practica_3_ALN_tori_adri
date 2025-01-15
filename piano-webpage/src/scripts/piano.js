// Define los acordes para todas las tonalidades
const tonalities = {
    C: ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
    Db: ["Db", "Ebm", "Fm", "Gb", "Ab", "Bbm", "Cdim"],
    D: ["D", "Em", "Gbm", "G", "A", "Bm", "Ddim"],
    Eb: ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Edim"],
    E: ["E", "Gbm", "Abm", "A", "B", "Dbm", "Edim"],
    F: ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
    Gb: ["Gb", "Abm", "Bbm", "B", "Db", "Ebm", "Fdim"],
    G: ["G", "Am", "Bm", "C", "D", "Em", "Gdim"],
    Ab: ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Adim"],
    A: ["A", "Bm", "Dbm", "D", "E", "Gbm", "Bbdim"],
    Bb: ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
    B: ["B", "Dbm", "Ebm", "E", "Gb", "Abm", "Bdim"]
};

// Define las notas de cada acorde
const chordNotes = {
    // Mayores
    C: ["C1", "E1", "G1"],
    Db: ["Db1", "F1", "Ab1"],
    D: ["D1", "Gb1", "A1"],
    Eb: ["Eb1", "G1", "Bb1"],
    E: ["E1", "Ab1", "B1"],
    F: ["F1", "A1", "C2"],
    Gb: ["Gb1", "Bb1", "Db2"],
    G: ["G1", "B1", "D2"],
    Ab: ["Ab1", "C2", "Eb2"],
    A: ["A1", "Db2", "E2"],
    Bb: ["Bb1", "D2", "F2"],
    B: ["B1", "Eb2", "Gb2"],

    // Menores
    Cm: ["C1", "Eb1", "G1"],
    Dbm: ["Db1", "E1", "Ab1"],
    Dm: ["D1", "F1", "A1"],
    Ebm: ["Eb1", "Gb1", "Bb1"],
    Em: ["E1", "G1", "B1"],
    Fm: ["F1", "Ab1", "C2"],
    Gbm: ["Gb1", "A1", "Db2"],
    Gm: ["G1", "Bb1", "D2"],
    Abm: ["Ab1", "B1", "Eb2"],
    Am: ["A1", "C2", "E2"],
    Bbm: ["Bb1", "Db2", "F2"],
    Bm: ["B1", "D2", "Gb2"],

    // Disminuidos
    Cdim: ["C1", "Eb1", "Gb1"],
    Dbdim: ["Db1", "E1", "G1"], 
    Ddim: ["D1", "F1", "Ab1"],
    Ebdim: ["Eb1", "Gb1", "A1"],
    Edim: ["E1", "G1", "Bb1"],
    Fdim: ["F1", "Ab1", "B2"],
    Gbdim: ["Gb1", "A1", "C2"], 
    Gdim: ["G1", "Bb1", "Db2"],
    Abdim: ["Ab1", "B2", "D2"],
    Adim: ["A1", "C2", "Eb2"],
    Bbdim: ["Bb1", "Db2", "E2"],
    Bdim: ["B1", "D1", "F1"]
};

// Escuchar eventos DOM
document.addEventListener('DOMContentLoaded', () => {
    const keys = document.querySelectorAll('.key');
    const tonalitySelector = document.getElementById('tonality-selector');
    const playButton = document.getElementById('play-button');

    // Añade eventos a las teclas para reproducir sonidos individuales
    keys.forEach(key => {
        key.addEventListener('click', () => playSound(key));
    });

    // Evento para el botón de Play
    playButton.addEventListener('click', async () => {
        const selectedTonality = tonalitySelector.value; // Tonalidad seleccionada
        const progression = await fetchProgression(); // Simula la obtención de la progresión
        console.log(`Reproduciendo progresión en ${selectedTonality}: ${progression}`);
        playProgression(progression, selectedTonality); // Toca la progresión
    });
});

// Función para reproducir el sonido de una tecla
function playSound(key) {
    const note = key.dataset.note; // Obtiene la nota desde el atributo data-note
    const audio = new Audio(`../sounds/${note}.mp3`);
    audio.play();
    console.log(`Reproduciendo nota: ${note}`);
}

// Función para reproducir las notas de un acorde
function playChord(chord) {
    const notes = chordNotes[chord]; // Obtiene las notas del acorde

    if (!notes) {
        console.error(`Acorde no encontrado: ${chord}`);
        return;
    }

    // Duración en milisegundos que las teclas estarán activas
    const activeDuration = 1800; // 1 segundo

    // Reproduce cada nota del acorde
    notes.forEach(note => {
        const audio = new Audio(`../sounds/${note}.mp3`);
        audio.play();

        // Encuentra la tecla correspondiente en el DOM
        const key = document.querySelector(`.key[data-note="${note}"]`);
        if (key) {
            // Aplica la clase activa directamente
            key.classList.add('active');

            // Retira la clase activa después de la duración especificada
            setTimeout(() => {
                key.classList.remove('active');
            }, activeDuration);
        } else {
            console.warn(`Tecla no encontrada para la nota: ${note}`);
        }
    });

    console.log(`Reproduciendo acorde: ${chord} con notas: ${notes.join(", ")}`);
}


// Función para mapear grados a acordes
function getChordsFromProgression(progression, tonality) {
    const chords = tonalities[tonality];
    return progression.map(degree => chords[degree - 1]);
}

// Función para tocar una progresión de acordes
function playProgression(progression, tonality) {
    const chords = getChordsFromProgression(progression, tonality);

    chords.forEach((chord, index) => {
        setTimeout(() => {
            playChord(chord);
        }, index * 2000); // 2 segundos de retraso entre acordes
    });
}

// Simula la respuesta del backend
async function fetchProgression() {
    return [1, 6, 4, 1]; // Simula la progresión [1, 6, 4, 1]
}
