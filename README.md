# Automating System Analysis with Python, Selenium, SSH, and SFTP

## Introduction

In today's dynamic IT environments, system administrators regularly analyze server data, including Garbage Collection (GC) logs and System Activity Reports (SAR). Doing this manually can be time-consuming and error-prone. The Python-based automation suite we've developed significantly simplifies these tasks using Selenium, SSH, and SFTP. In this blog, we'll explore how this powerful combination of technologies efficiently automates system analysis, making administrative tasks seamless.

## Overview of the Automation Suite

The automation script performs the following core tasks:

### 1. Remote Server Interaction (SSH & SFTP)

Using the `paramiko` and `pysftp` libraries, the script securely connects to remote servers, executes predefined commands, and retrieves log files for analysis. This process is handled by dedicated controllers (`SSHController.py`, `sftpController.py`), providing clear and structured operations.

### 2. Automated Analysis with Selenium

- **GC Log Analysis (`GC_analyze.py`):** Automates uploading GC log files to `gceasy.io`, captures screenshots of analysis reports, and extracts critical data points such as memory usage, GC duration, throughput, and pause times. This helps administrators quickly identify memory leaks, inefficiencies, and areas requiring optimization.

- **SAR Analysis (`Sar_analyzer.py`):** Automates the analysis of SAR files using browser automation. It simplifies the extraction of crucial system metrics such as CPU usage, memory consumption, disk activity, network traffic, and load averages. The automated workflow organizes the downloaded SAR analysis reports systematically, allowing rapid issue diagnosis and resolution.

### 3. Configuration Management

All settings, including server details, paths, and credentials, are managed through a cleanly structured configuration parser (`ConfigurationParser.py`). This approach ensures flexibility and adaptability to different environments without changing the source code.

### 4. Main Script Orchestration

The `main.py` script serves as the central orchestrator. It invokes SSH/SFTP controllers, manages log retrieval, triggers automated analyses, and ensures outputs are systematically recorded and stored.

### Detailed Logging

The script uses detailed logging mechanisms to provide comprehensive insights into each step of the execution process. Logs include:

- Connection statuses (success/failure) for SSH and SFTP sessions.
- Execution timestamps and durations for each analysis step.
- File download and upload activities, including filenames and sizes.
- Errors and exceptions captured during the process for easy troubleshooting.
- Analysis results with metadata clearly logged to ensure transparency and auditability.

## Benefits

- **Efficiency:** Reduces manual tasks, saving valuable time.
- **Consistency:** Ensures uniform analysis every time.
- **Scalability:** Easily adapts to multiple servers and environments.
- **Security:** Secure file transfers and connections via SSH/SFTP.

## Conclusion

By leveraging Python's automation capabilities alongside Selenium, SSH, and SFTP, this automation suite provides a powerful toolset for modern system administration. Its modular design and clear structure make it not only efficient but also highly maintainable and adaptable for future needs.

---

# Execution Guide

## Requirements
- Python 3.7 or higher
- Selenium
- Paramiko
- PySFTP
- Pandas
- ChromeDriver (compatible with your Chrome browser version)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
```

2. **Navigate to the script directory:**
```bash
cd <script-directory>
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up ChromeDriver:**
- Download ChromeDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads).
- Place `chromedriver.exe` in the `chrome` directory.

## Configuration

- Update `Configuration/config.cfg` with your environment-specific settings such as:
  - Server IP, username, password
  - File paths

## Execution

- Run the automation script:
```bash
python main.py sf1
```

- Alternatively, use the provided batch file (Windows):
```bash
execute.bat
```

## Outputs
- Analysis reports and screenshots are saved in predefined directories (`GcReports`, `SarReports`).
- Detailed execution logs are stored, providing comprehensive insights into the script execution flow and aiding quick troubleshooting.

---

With this setup guide, you should easily get your automation suite up and running efficiently.

