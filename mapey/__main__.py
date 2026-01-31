"""
Main CLI entry point for Mapey.
Usage: python -m mapey [command]
"""
import sys
import os
import subprocess
import shutil
import platform
from pathlib import Path


class MapeyManager:
    """Manager for Mapey project setup and execution."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.absolute()
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.venv_dir = self.project_root / "venv"
        self.python_version = sys.version_info
        
    def print_header(self, text):
        """Print a formatted header."""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def print_step(self, text):
        """Print a step with formatting."""
        print(f"\n> {text}")
    
    def print_success(self, text):
        """Print success message."""
        print(f"[OK] {text}")
    
    def print_error(self, text):
        """Print error message."""
        print(f"[ERROR] {text}")
    
    def check_command(self, command):
        """Check if a command is available."""
        return shutil.which(command) is not None
    
    def run_command(self, cmd, cwd=None, check=True, capture=False):
        """Run a shell command."""
        if isinstance(cmd, list):
            cmd_str = " ".join(cmd)
        else:
            cmd_str = cmd
            
        if capture:
            result = subprocess.run(
                cmd_str, 
                shell=True, 
                cwd=cwd, 
                capture_output=True, 
                text=True
            )
            if check and result.returncode != 0:
                self.print_error(f"Command failed: {cmd_str}")
                print(result.stderr)
                sys.exit(1)
            return result
        else:
            result = subprocess.run(cmd_str, shell=True, cwd=cwd)
            if check and result.returncode != 0:
                self.print_error(f"Command failed: {cmd_str}")
                sys.exit(1)
            return result
    
    def get_venv_python(self):
        """Get the path to the venv Python executable."""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def get_venv_pip(self):
        """Get the path to the venv pip executable."""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"
    
    def check_venv(self):
        """Check if venv exists and is valid."""
        python_path = self.get_venv_python()
        return self.venv_dir.exists() and python_path.exists()
    
    def create_venv(self):
        """Create a new virtual environment."""
        self.print_step("Creating virtual environment...")
        
        # Use the current Python interpreter to create venv
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(self.venv_dir)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            self.print_error("Failed to create virtual environment")
            print(result.stderr)
            sys.exit(1)
        
        self.print_success("Virtual environment created")
    
    def check_requirements_installed(self):
        """Check if core requirements are installed in venv."""
        python_path = self.get_venv_python()
        
        # Try importing core dependencies
        test_code = """
import sys
try:
    import fastapi
    import uvicorn
    import langchain_ollama
    sys.exit(0)
except ImportError:
    sys.exit(1)
"""
        
        result = subprocess.run(
            [str(python_path), "-c", test_code],
            capture_output=True
        )
        
        return result.returncode == 0
    
    def get_requirements_file(self):
        """Determine which requirements file to use based on Python version."""
        # Always prioritize clean requirements (no torch)
        req_clean = self.backend_dir / "requirements-clean.txt"
        if req_clean.exists():
            return "requirements-clean.txt"
        
        if self.python_version.major == 3 and self.python_version.minor >= 12:
            # Use modern requirements for Python 3.12+
            return "requirements-314.txt"
        else:
            # Use older requirements for Python < 3.12
            return "requirements.txt"
    
    def create_modern_requirements(self):
        """Create requirements-314.txt with unpinned versions."""
        self.print_step("Creating modern requirements file for Python 3.12+...")
        
        modern_requirements = """# FastAPI and server
fastapi
uvicorn[standard]
python-multipart

# Configuration and validation
pydantic
pydantic-settings
python-dotenv

# LangChain and LLM
langchain-ollama
langchain-core
langgraph

# Vector store and embeddings
faiss-cpu
sentence-transformers

# PyTorch and dependencies
torch
torchvision
numpy
packaging

pypdf

# Web search
tavily-python

# HTTP client
httpx

# Authentication
PyJWT
"""
        
        req_file = self.backend_dir / "requirements-314.txt"
        req_file.write_text(modern_requirements)
        self.print_success("Created requirements-314.txt")
    
    def install_requirements(self):
        """Install Python requirements."""
        pip_path = self.get_venv_pip()
        req_file = self.get_requirements_file()
        req_path = self.backend_dir / req_file
        
        # Create modern requirements if using Python 3.12+ and file doesn't exist
        if req_file == "requirements-314.txt" and not req_path.exists():
            self.create_modern_requirements()
        
        self.print_step(f"Installing Python dependencies from {req_file}...")
        
        # Upgrade pip first using python -m pip
        python_path = self.get_venv_python()
        self.run_command([str(python_path), "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        self.run_command([str(pip_path), "install", "-r", str(req_path)])
        
        self.print_success("Python dependencies installed")
        
        # If using modern requirements, freeze to create versioned file
        if req_file == "requirements-314.txt":
            self.print_step("Freezing installed versions...")
            result = self.run_command(
                [str(pip_path), "freeze"],
                capture=True
            )
            
            # Save frozen requirements
            frozen_file = self.backend_dir / "requirements-314.txt"
            frozen_file.write_text(result.stdout)
            self.print_success("Saved frozen requirements to requirements-314.txt")
    
    def check_node_modules(self):
        """Check if node_modules exists in frontend."""
        node_modules = self.frontend_dir / "node_modules"
        return node_modules.exists()
    
    def install_frontend_deps(self):
        """Install frontend dependencies."""
        self.print_step("Installing frontend dependencies...")
        
        if not self.check_command("npm"):
            self.print_error("npm is not installed. Please install Node.js and npm.")
            sys.exit(1)
        
        self.run_command("npm install", cwd=self.frontend_dir)
        self.print_success("Frontend dependencies installed")
    
    def setup_env_files(self):
        """Set up environment files."""
        self.print_step("Setting up environment files...")
        
        # Backend: rename env.example to .env.example, then copy to .env
        backend_env_example_old = self.backend_dir / "env.example"
        backend_env_example_new = self.backend_dir / ".env.example"
        backend_env = self.backend_dir / ".env"
        
        # Rename env.example to .env.example if it exists
        if backend_env_example_old.exists():
            backend_env_example_old.rename(backend_env_example_new)
            self.print_success("Renamed backend/env.example to backend/.env.example")
        
        # Copy .env.example to .env if .env doesn't exist
        if not backend_env.exists():
            if backend_env_example_new.exists():
                shutil.copy(backend_env_example_new, backend_env)
                self.print_success("Created backend/.env from .env.example")
            else:
                self.print_error("backend/.env.example not found")
        else:
            self.print_success("backend/.env already exists")
        
        # Frontend: copy .env.example to .env.local
        frontend_env_example = self.frontend_dir / ".env.example"
        frontend_env = self.frontend_dir / ".env.local"
        
        if not frontend_env.exists():
            if frontend_env_example.exists():
                shutil.copy(frontend_env_example, frontend_env)
                self.print_success("Created frontend/.env.local from .env.example")
            else:
                self.print_error("frontend/.env.example not found")
        else:
            self.print_success("frontend/.env.local already exists")
    
    def check_docker(self):
        """Check if Docker is installed and running."""
        if not self.check_command("docker"):
            self.print_error("Docker is not installed")
            return False
        
        # Check if Docker daemon is running
        result = subprocess.run(
            "docker info",
            shell=True,
            capture_output=True
        )
        
        if result.returncode != 0:
            self.print_error("Docker daemon is not running")
            return False
        
        return True
    
    def setup(self):
        """Run full setup process."""
        self.print_header("Mapey Project Setup")
        
        print(f"\nPython Version: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"Project Root: {self.project_root}")
        
        # Check prerequisites
        self.print_step("Checking prerequisites...")
        
        if not self.check_command("docker"):
            self.print_error("Docker is not installed. Please install Docker Desktop.")
            sys.exit(1)
        
        self.print_success("Docker is installed")
        
        # Check/create venv
        if self.check_venv():
            self.print_success("Virtual environment exists")
            
            # Check if requirements are installed
            if not self.check_requirements_installed():
                self.print_step("Core requirements not found, installing...")
                self.install_requirements()
            else:
                self.print_success("Core requirements already installed")
        else:
            self.create_venv()
            self.install_requirements()
        
        # Check/install frontend dependencies
        if self.check_node_modules():
            self.print_success("Frontend node_modules exists")
        else:
            self.install_frontend_deps()
        
        # Setup environment files
        self.setup_env_files()
        
        self.print_header("Setup Complete!")
        print("\nYou can now run: python -m mapey start")
    
    def check_ollama_models(self):
        """Check and pull required Ollama models."""
        self.print_step("Checking Ollama models...")
        
        models = ["llama3.2:1b", "nomic-embed-text"]
        
        # Parse backend/.env for overrides
        backend_env = self.backend_dir / ".env"
        if backend_env.exists():
            try:
                content = backend_env.read_text(encoding='utf-8')
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if line.startswith("OLLAMA_MODEL="):
                        val = line.split("=", 1)[1].strip().strip("'").strip('"')
                        if val: models[0] = val
                    elif line.startswith("EMBED_MODEL_NAME="):
                        val = line.split("=", 1)[1].strip().strip("'").strip('"')
                        if val: models[1] = val
            except Exception as e:
                self.print_error(f"Error reading .env file: {e}")

        self.print_step("Waiting for Ollama service to be ready...")
        import time
        max_retries = 30
        for i in range(max_retries):
            # Check if ollama is responding
            result = subprocess.run(
                "docker-compose exec -T ollama ollama list",
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                break
            if i % 5 == 0:
                print(f"  Waiting... ({i+1}/{max_retries})")
            time.sleep(2)
        else:
            self.print_error("Ollama service is not responding after waiting. Please check logs.")
            return

        # List models again to get current state
        result = subprocess.run(
            "docker-compose exec -T ollama ollama list",
            shell=True,
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        installed_models = result.stdout
        
        for model in models:
            # Simple check if model name (or part of it) is in output
            if model not in installed_models:
                self.print_step(f"Pulling model: {model} (this may take a while)...")
                subprocess.run(
                    f"docker-compose exec ollama ollama pull {model}",
                    shell=True,
                    cwd=self.project_root
                )
                self.print_success(f"Model {model} pulled")
            else:
                print(f"  - Model {model} is already installed")

    def start(self):
        """Start the application using Docker Compose (no rebuild by default)."""
        self.print_header("Starting Mapey Application")
        
        # Check if Docker is available
        if not self.check_docker():
            self.print_error("Please start Docker Desktop and try again")
            sys.exit(1)
        
        self.print_success("Docker is running")
        
        # Check if setup was run
        if not self.check_venv():
            self.print_error("Setup not complete. Please run: python -m mapey setup")
            sys.exit(1)
        
        # Check if env files exist
        backend_env = self.backend_dir / ".env"
        frontend_env = self.frontend_dir / ".env.local"
        
        if not backend_env.exists() or not frontend_env.exists():
            self.print_error("Environment files missing. Please run: python -m mapey setup")
            sys.exit(1)
        
        self.print_step("Starting Docker containers...")
        
        # Check if containers already exist
        result = subprocess.run(
            "docker-compose ps -q",
            shell=True,
            cwd=self.project_root,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            self.print_error("Failed to query docker-compose. Ensure Docker Compose is available.")
            sys.exit(1)

        container_ids = result.stdout.strip()

        if not container_ids:
            # No containers have been created yet; create them (no forced rebuild)
            self.print_step("No containers found - creating containers (no rebuild).")
            self.run_command(
                "docker-compose up -d",
                cwd=self.project_root
            )
        else:
            # Containers exist; just start them (won't rebuild images)
            self.print_step("Containers found - starting existing containers.")
            self.run_command(
                "docker-compose start",
                cwd=self.project_root
            )

        # Show status
        status = subprocess.run(
            "docker-compose ps",
            shell=True,
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        if status.returncode == 0:
            print(status.stdout)

        # Check and pull Ollama models
        self.check_ollama_models()

        self.print_success("Docker containers are running (detached). Use 'python -m mapey rebuild' to rebuild images with no cache, or 'docker-compose logs -f' to follow logs.")

    def rebuild(self):
        """Force rebuild of Docker images with no cache and restart containers."""
        self.print_header("Rebuilding Docker images (no cache) and restarting containers")

        # Check if Docker is available
        if not self.check_docker():
            self.print_error("Please start Docker Desktop and try again")
            sys.exit(1)

        self.print_step("Stopping and removing existing containers...")
        subprocess.run(
            "docker-compose down",
            shell=True,
            cwd=self.project_root,
            capture_output=True
        )

        self.print_step("Building images with --no-cache...")
        self.run_command(
            "docker-compose build --no-cache",
            cwd=self.project_root
        )

        self.print_step("Starting containers (detached)...")
        self.run_command(
            "docker-compose up -d",
            cwd=self.project_root
        )

        # Show status
        status = subprocess.run(
            "docker-compose ps",
            shell=True,
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        if status.returncode == 0:
            print(status.stdout)

        # Check and pull Ollama models
        self.check_ollama_models()

        self.print_success("Rebuild complete and containers started (detached).")

    def stop(self):
        """Stop all Docker containers."""
        self.print_header("Stopping Mapey")
        
        # Check if Docker is available
        if not self.check_docker():
            self.print_error("Docker is not running")
            sys.exit(1)
        
        self.print_step("Stopping Docker containers...")
        self.run_command("docker-compose stop", cwd=self.project_root)
        
        self.print_success("All containers stopped!")
        print("\nTo start again, run: python -m mapey start")

    def dev(self):
        """Start local development: Ollama in Docker, Backend/Frontend locally."""
        self.print_header("Starting Local Development Environment")
        
        # 1. Start Ollama in Docker
        if not self.check_docker():
            self.print_error("Docker is not running. Please start Docker Desktop.")
            sys.exit(1)
            
        self.print_step("Starting Ollama in Docker...")
        self.run_command("docker-compose up -d ollama", cwd=self.project_root)
        
        # 2. Check Models
        self.check_ollama_models()
        self.print_success("Ollama is ready")
        
        # 3. Launch local services
        if platform.system() == "Windows":
            start_bat = self.project_root / "start.bat"
            if start_bat.exists():
                self.print_step("Launching start.bat for Backend and Frontend...")
                subprocess.run(f'cmd /c "{str(start_bat)}"', shell=True)
            else:
                self.print_error("start.bat not found")
        else:
            self.print_step("Please run the backend and frontend in separate terminals:")
            print("  Backend:  cd backend && ../venv/bin/uvicorn app.main:app --reload")
            print("  Frontend: cd frontend && npm run dev")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m mapey [setup|start|rebuild|dev]")
        print("\nCommands:")
        print("  setup   - Set up the project (venv, dependencies, env files)")
        print("  start   - Start the application with Docker Compose (does not rebuild images)")
        print("  stop    - Stop all Docker containers")
        print("  rebuild - Force rebuild Docker images with no cache and restart containers")
        print("  dev     - Run locally: Ollama (Docker) + Backend/Frontend (Local)")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    manager = MapeyManager()
    
    if command == "setup":
        manager.setup()
    elif command == "start":
        manager.start()
    elif command == "stop":
        manager.stop()
    elif command == "rebuild":
        manager.rebuild()
    elif command == "dev":
        manager.dev()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: setup, start, stop, rebuild, dev")
        sys.exit(1)


if __name__ == "__main__":
    main()
