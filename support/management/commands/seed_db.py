from django.core.management.base import BaseCommand
from support.models import KnowledgeArticle

class Command(BaseCommand):
    help = 'Seeds the database with initial technical support knowledge articles.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Knowledge Base articles...')
        
        sample_articles = [
            {
                'title': 'Wi-Fi Connected But No Internet Access',
                'category': 'Network & Wi-Fi',
                'keywords': 'wifi, internet, connection, network, router, wireless, ip address, dns',
                'problem': 'The Wi-Fi status indicator shows "Connected, no internet". Websites fail to load and network requests time out despite being connected to the router.',
                'solution': (
                    "1. Open Command Prompt as Administrator.\n"
                    "2. Run DNS flush command: `ipconfig /flushdns`\n"
                    "3. Reset TCP/IP stack: `netsh int ip reset`\n"
                    "4. Release and renew IP: `ipconfig /release` followed by `ipconfig /renew`\n"
                    "5. Restart your wireless router by unplugging power for 30 seconds.\n"
                    "6. Reconnect to your Wi-Fi network."
                )
            },
            {
                'title': 'Windows Update Installation Error & Stuck Updates',
                'category': 'Operating System',
                'keywords': 'windows, update, error, stuck, 0x80070002, windows update, restart',
                'problem': 'Windows Update gets stuck at a certain percentage (e.g. 99%) or fails with error code 0x80070002 or 0x800f081f when installing system patches.',
                'solution': (
                    "1. Press Win + R, type `services.msc`, and press Enter.\n"
                    "2. Locate 'Windows Update' service, right-click, and choose 'Stop'.\n"
                    "3. Open File Explorer and navigate to `C:\\Windows\\SoftwareDistribution\\Download`.\n"
                    "4. Delete all files inside the Download folder.\n"
                    "5. Return to Services window and click 'Start' on Windows Update service.\n"
                    "6. Go to Settings > Update & Security > Run Windows Update Troubleshooter."
                )
            },
            {
                'title': 'Printer Offline or Not Responding Error',
                'category': 'Software & Hardware',
                'keywords': 'printer, offline, print queue, paper jam, spooler, driver, hardware',
                'problem': 'Printer status displays "Offline" or document jobs remain stuck in the print queue without printing.',
                'solution': (
                    "1. Ensure printer is powered on and connected via USB or same Wi-Fi network.\n"
                    "2. Open Settings > Devices > Printers & Scanners.\n"
                    "3. Click your printer > Open Queue > Cancel all pending documents.\n"
                    "4. Open `services.msc`, locate 'Print Spooler', and click 'Restart'.\n"
                    "5. Uncheck 'Use Printer Offline' option in Printer Properties window."
                )
            },
            {
                'title': 'Domain / Email Account Password Reset Procedure',
                'category': 'Account & Security',
                'keywords': 'password, reset, account, login, locked, authentication, security, credentials',
                'problem': 'User is unable to log in to system account due to forgotten password or account lock after multiple failed attempts.',
                'solution': (
                    "1. Navigate to the self-service portal at `https://account.company.com/reset`.\n"
                    "2. Enter registered username or employee email ID.\n"
                    "3. Select verification method (SMS OTP or Authenticator app code).\n"
                    "4. Enter received verification code and set new password adhering to policy (min 12 chars, numbers, symbols).\n"
                    "5. Wait 2 minutes for domain controller synchronization before logging in."
                )
            },
            {
                'title': 'Python "FileNotFoundError: [Errno 2]" Fix',
                'category': 'Programming & Development',
                'keywords': 'python, file not found, FileNotFoundError, path, directory, script, error',
                'problem': 'Python script crashes with `FileNotFoundError: [Errno 2] No such file or directory` when trying to open or read a file using `open()`.',
                'solution': (
                    "1. Check relative vs absolute path: Python evaluates relative paths based on Current Working Directory (`os.getcwd()`), not script location.\n"
                    "2. Convert path to absolute path using `os.path.abspath(__file__)` or `pathlib.Path`.\n"
                    "3. Example fix:\n"
                    "   ```python\n"
                    "   from pathlib import Path\n"
                    "   BASE_DIR = Path(__file__).resolve().parent\n"
                    "   file_path = BASE_DIR / 'data.txt'\n"
                    "   ```\n"
                    "4. Ensure correct file extensions (e.g. `data.txt` instead of `data.txt.txt`)."
                )
            },
            {
                'title': 'Python Package Installation Error (pip command failure)',
                'category': 'Programming & Development',
                'keywords': 'python, pip, install, error, package, virtualenv, ssl, permissions',
                'problem': 'Running `pip install <package>` fails with SSL certificate error, permission denied, or command not found.',
                'solution': (
                    "1. Always use python module execution to prevent environment conflicts:\n"
                    "   `python -m pip install <package_name>`\n"
                    "2. If virtual environment is not active, create one:\n"
                    "   `python -m venv .venv`\n"
                    "   Activation (Windows): `.\\.venv\\Scripts\\activate`\n"
                    "3. Upgrade pip to latest version: `python -m pip install --upgrade pip`\n"
                    "4. For SSL certificate errors, run: `python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package_name>`"
                )
            },
            {
                'title': 'VS Code Extension Crashes or High CPU Usage',
                'category': 'Programming & Development',
                'keywords': 'vs code, vscode, editor, crash, extension, slow, freeze, lag, syntax',
                'problem': 'Visual Studio Code editor runs slowly, freezes during typing, or extensions fail to load properly.',
                'solution': (
                    "1. Run VS Code with extensions disabled to verify root cause: `code --disable-extensions`\n"
                    "2. Open VS Code Process Explorer via `Help > Open Process Explorer` to identify CPU-heavy extension.\n"
                    "3. Clear editor cache: Delete folder at `%APPDATA%\\Code\\User\\workspaceStorage`.\n"
                    "4. Update VS Code to latest version via `Help > Check for Updates`."
                )
            },
            {
                'title': 'Git "Permission denied (publickey)" SSH Key Error',
                'category': 'Programming & Development',
                'keywords': 'git, ssh, permission denied, publickey, github, repository, push, clone',
                'problem': 'Git clone, fetch, or push operation fails with `git@github.com: Permission denied (publickey). fatal: Could not read from remote repository.`',
                'solution': (
                    "1. Generate a new SSH keypair: `ssh-keygen -t ed25519 -C \"your_email@example.com\"`\n"
                    "2. Start SSH agent in PowerShell: `eval $(ssh-agent -s)` or `Start-Service ssh-agent`\n"
                    "3. Add key to agent: `ssh-add ~/.ssh/id_ed25519`\n"
                    "4. Copy public key content: `cat ~/.ssh/id_ed25519.pub`\n"
                    "5. Paste key into GitHub/GitLab settings under SSH and GPG keys."
                )
            },
            {
                'title': 'General Internet Connection Dropping Frequently',
                'category': 'Network & Wi-Fi',
                'keywords': 'internet, network, connection drops, disconnections, router, ethernet',
                'problem': 'Internet connection drops intermittently every few minutes during web browsing or video calls.',
                'solution': (
                    "1. Disable Power Saving mode on network adapter: Device Manager > Network Adapters > Properties > Power Management > Uncheck 'Allow computer to turn off this device'.\n"
                    "2. Change DNS Servers to Google DNS (8.8.8.8 and 8.8.4.4) or Cloudflare (1.1.1.1).\n"
                    "3. Replace damaged Ethernet cable or move closer to Wi-Fi access point."
                )
            }
        ]

        count = 0
        for data in sample_articles:
            obj, created = KnowledgeArticle.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new knowledge base articles! Total articles in DB: {KnowledgeArticle.objects.count()}'))
