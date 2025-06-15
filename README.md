# Instagram Bot

This bot is created to post automated content on Instagram. The account it uses is: @circumferencedividedbydiameter

## 📖 Table of Contents
- [About](#about)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🌟 About

This project came about due to the lack of official Instagram APIs suitable for this type of automation. As such, it relies on reverse-engineered methods to interact with Instagram. This means that while functional, it may be sensitive to changes made by Instagram to their private API or web interface.

## ✨ Features

*   **Post Count Retrieval:** Can fetch the exact number of posts for the configured account.
*   **Automated Posting:** Allows placing new posts with captions to the Instagram account.

## 🛠 Prerequisites

To use this bot, you'll likely need:
*   Python 3.8+ (or the specific version used in the `dev` branch)
*   An active Instagram account (the one you intend to automate, e.g., `@circumferencedividedbydiameter`)
*   Pip (Python package installer)

## ⚙️ Installation

Follow these steps to set up the bot, focusing on the `dev` branch:

1.  **Clone the repository (dev branch):**
    ```bash
    git clone -b dev https://github.com/verynewusername/instagrambot.git
    cd instagrambot
    ```
2.  **Install dependencies:**
    This project likely uses a `requirements.txt` file to manage Python dependencies. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
    *(If your project uses a different dependency manager like Poetry or Pipenv, please update this section accordingly.)*

3.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project. This file will store your Instagram credentials securely. You can often create this by copying an example file if one is provided (e.g., `cp .env.example .env`).

    Add the following variables to your `.env` file:
    ```env
    INSTAGRAM_USERNAME="your_instagram_username"
    INSTAGRAM_ENCRYPTED_PASSWORD="your_captured_encrypted_password"
    ```
    **Important Note on `INSTAGRAM_ENCRYPTED_PASSWORD`:**
    This is **not** your plain text Instagram password. You need to capture this encrypted password string from a legitimate login request made through a web browser. You can do this using your browser's developer tools (usually by pressing F12) and inspecting the network requests made during the Instagram login process. Look for the request that sends your credentials, and you should find the encrypted password in the payload. The specific encryption method is handled by Instagram, and this bot utilizes that already encrypted form. Once captured, this encrypted password should remain valid as long as your actual Instagram password does not change.

## 🚀 Usage

After installation and configuration, you can typically run the bot using its main script.

If the main script is `main.py` (a common convention), you would run it like this:
```bash
python main.py
```
*(Please update this command if your main script has a different name or if there are specific command-line arguments required to perform certain actions, like posting content vs. getting post count.)*

## 🔧 Configuration

The primary configuration for this bot is handled through environment variables, which should be placed in a `.env` file in the project's root directory, as described in the Installation section.

**Required Environment Variables:**

*   `INSTAGRAM_USERNAME`: The username of the Instagram account the bot will control.
    *   Example: `INSTAGRAM_USERNAME="circumferencedividedbydiameter"`

*   `INSTAGRAM_ENCRYPTED_PASSWORD`: Your Instagram password, but in its encrypted form as captured from a browser session.
    *   **How to obtain:** As detailed in the Installation section, this encrypted string must be captured from a web UI HTTP request during a successful login to Instagram.
    *   **Persistence:** Once obtained, this encrypted password can be reused as long as your actual Instagram password remains unchanged.
    *   Example Format (your actual captured password will vary): `INSTAGRAM_ENCRYPTED_PASSWORD="'#PWD_INSTAGRAM_BROWSER:11:1111111111:..."` (The string will be much longer and contain a mix of characters).

*(If there are other optional environment variables for things like post frequency, content sources, or specific bot behaviors, list and describe them here.)*

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the bot or add features, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or fix (`git checkout -b feature/your-amazing-feature` or `git checkout -b fix/some-bug`).
3. Make your changes and commit them with clear messages (`git commit -m 'Add amazing feature'`).
4. Push your changes to your forked repository (`git push origin feature/your-amazing-feature`).
5. Open a Pull Request back to the `dev` branch of the `verynewusername/instagrambot` repository.

*(Consider adding notes on coding style, running tests, or any specific contribution guidelines if you have them.)*

## 📄 License

This project is currently not licensed. Please choose an appropriate open-source license (e.g., MIT, Apache 2.0, GPL) and add a `LICENSE.md` file to the repository. Update this section to reflect your choice.

Example:
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

Built with ❤️ by @verynewusername