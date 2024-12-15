# Project Name

Benzin Preis App

---

## Description

The Benzin Preis App is a user-friendly application designed to help users track and compare fuel prices in Germany. By leveraging Tankerkoenig data and providing a simple interface, the app empowers users to make informed decisions about where to refuel and save money.

---

## Documentation

For detailed documentation and additional information about the project, please visit our [OneDrive documentation](https://1drv.ms/u/s!AqU7MuLun5rPg0LTbiYL1BFk-EWM?e=dZpJ6o).

---

## Setup

Follow these steps to set up and run the project:

### Prerequisites

loadUi("resources/ui/mainWindow.ui", self)

Ensure you have the following installed on your machine:

- **Python ^3.9+**
- **Poetry** (installation instructions included below)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Osamaiqji89/Benzinpreis-App.git
   cd Benzinpreis-App
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:

   - On **Linux/Mac**:
     ```bash
     source .venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     .venv\Scripts\activate
     ```

4. Install Poetry (if not already installed):
   ```bash
   pip install poetry
   ```

5. Use Poetry to install project dependencies:
   ```bash
   poetry install
   ```

6. Run the application or script as needed:
   ```bash
   poetry run python main.py
   ```
   or 
   ```bash
   python main.py
   ```

---

## License

This project is licensed under the [MIT License](LICENSE) – feel free to use, modify, and distribute this software as per the license terms.

---

## Contribution

Contributions are welcome! Please feel free to open issues or submit pull requests.

---

## Author

Donald, Osama, Frank, Moahamed, Asfour

---

## Acknowledgments

- Thanks to the amazing open-source community for tools like **Poetry** and **Python**.
- [Any other acknowledgments or mentions]