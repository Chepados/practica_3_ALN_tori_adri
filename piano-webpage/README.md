# Piano Webpage

This project is a simple web-based piano application that allows users to play piano notes by clicking on the piano keys. Each key is independent and plays the corresponding sound for the note.

## Project Structure

```
piano-webpage
├── src
│   ├── index.html        # Main HTML document for the webpage
│   ├── styles
│   │   └── styles.css    # Styles for the webpage and piano layout
│   └── scripts
│       └── piano.js      # JavaScript functionality for the piano
├── sounds
│   └── [note-sounds].mp3  # Audio files for each piano note
├── package.json           # Configuration file for npm
└── README.md              # Project documentation
```

## Getting Started

To get started with the piano webpage, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd piano-webpage
   ```

2. **Install dependencies** (if any):
   ```
   npm install
   ```

3. **Open the webpage**:
   Open `src/index.html` in your web browser to view and interact with the piano.

## Usage

- Click on the piano keys to play the corresponding notes.
- Ensure that the audio files are correctly placed in the `sounds` directory and named according to the notes they represent (e.g., C.mp3, D.mp3, etc.).

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. 

## License

This project is open-source and available under the MIT License.